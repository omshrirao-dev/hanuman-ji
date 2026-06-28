"""
The core retrieval-augmented generation engine. Kept as a single object with an
.invoke(query) method so it stays trivially wrappable later by the Kavacha SDK:

    import kavacha
    kavacha.init("kv_...", "hanuman-ji-project-id")
    kavacha.watch(rag_pipeline)
"""
import json
import os
import re

from groq import Groq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.documents import gita_to_document
from app.language import detect_language
from app.prompts import SYSTEM_PROMPT
from app.query_understanding import rewrite_query_for_retrieval

EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
CANDIDATE_K = 15    # per-collection candidates pulled by raw semantic similarity
FINAL_TOP_N = 3      # passed to the LLM after metadata re-ranking

EMOTION_BONUS = 0.05
PRIORITY_BONUS = 0.02
# Non-priority gita verses only carry generic chapter-level tags (see
# documents.py). A chapter that talks about a negative quality at length
# (e.g. ch16 on anger/greed) packs many verses with that vocabulary, which
# let it out-rank specific, hand-tagged katha entries on word overlap alone
# — even though reciting "anger is a gate to hell" 3 times isn't actually
# the helpful response. This penalty means non-priority verses only win a
# slot when they're genuinely the closest semantic match, not just the
# most repetitive about a feeling word.
NON_PRIORITY_GITA_PENALTY = 0.15

VERSE_REF_RE = re.compile(r"(\d{1,2})[.:](\d{1,3})")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(BASE, "data", "processed")


class RAGPipeline:
    def __init__(self, chroma_dir=None, groq_api_key=None, groq_model=None):
        self.chroma_dir = chroma_dir or os.environ.get("CHROMA_DIR", "./data/chroma")
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.katha_store = Chroma(
            collection_name="katha_teachings",
            persist_directory=self.chroma_dir,
            embedding_function=self.embeddings,
        )
        self.gita_store = Chroma(
            collection_name="gita_shlokas",
            persist_directory=self.chroma_dir,
            embedding_function=self.embeddings,
        )
        self.groq_client = Groq(api_key=groq_api_key or os.environ["GROQ_API_KEY"])
        self.groq_model = groq_model or os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

        with open(os.path.join(PROCESSED, "gita_shlokas.json"), encoding="utf-8") as f:
            gita_entries = json.load(f)
        self.gita_by_key = {f"{e['chapter']}.{e['verse']}": e for e in gita_entries}
        self.chapter_verse_counts: dict[int, int] = {}
        for e in gita_entries:
            self.chapter_verse_counts[e["chapter"]] = max(
                self.chapter_verse_counts.get(e["chapter"], 0), e["verse"]
            )

    def _detect_direct_verse_ref(self, query: str):
        """Embeddings can't reliably match exact numeric citations like 'BG 2.47' —
        a sentence-similarity model doesn't represent '2.47' meaningfully. If the
        raw query contains a chapter.verse pattern that's a valid Gita reference,
        skip semantic search and fetch it directly."""
        for chapter_str, verse_str in VERSE_REF_RE.findall(query):
            chapter, verse = int(chapter_str), int(verse_str)
            max_verse = self.chapter_verse_counts.get(chapter)
            if max_verse and 1 <= verse <= max_verse:
                return chapter, verse
        return None

    def _direct_verse_hit(self, chapter: int, verse: int):
        entry = self.gita_by_key.get(f"{chapter}.{verse}")
        if not entry:
            return []
        return [(gita_to_document(entry), 0.0)]

    def _metadata_bonus(self, query_tokens: set, metadata: dict) -> float:
        # Word-level overlap rather than exact-phrase substring matching: a
        # rewritten query like "unable to find a job" should still get credit
        # against a life_situations phrase like "job search" (shared word
        # "job"), not just an exact phrase match, which rewrites rarely produce.
        bonus = 0.0
        for field in ("emotions", "life_situations", "themes", "chapter_theme"):
            value = metadata.get(field, "")
            for phrase in value.lower().split(", "):
                phrase_tokens = set(re.findall(r"[a-z]+", phrase))
                if not phrase_tokens:
                    continue
                overlap = phrase_tokens & query_tokens
                if overlap:
                    bonus += EMOTION_BONUS * len(overlap) / len(phrase_tokens)
        if metadata.get("priority"):
            bonus += PRIORITY_BONUS
        return bonus

    def _adjusted_score(self, query_tokens: set, doc_score) -> float:
        doc, score = doc_score
        meta = doc.metadata
        penalty = (
            NON_PRIORITY_GITA_PENALTY
            if meta.get("type") == "shloka" and not meta.get("priority")
            else 0.0
        )
        return score + penalty - self._metadata_bonus(query_tokens, meta)

    def retrieve(self, query: str, k: int = CANDIDATE_K, top_n: int = FINAL_TOP_N):
        katha_hits = self.katha_store.similarity_search_with_score(query, k=k)
        gita_hits = self.gita_store.similarity_search_with_score(query, k=k)
        combined = katha_hits + gita_hits  # cosine distance, lower = closer

        query_tokens = set(re.findall(r"[a-z]+", query.lower()))
        combined.sort(key=lambda doc_score: self._adjusted_score(query_tokens, doc_score))
        return combined[:top_n]

    def format_context(self, hits) -> str:
        return "\n\n---\n\n".join(doc.page_content for doc, _ in hits)

    def format_sources(self, hits):
        sources = []
        for doc, _ in hits:
            meta = doc.metadata
            title = meta.get("title_en") or f"Bhagavad Gita {meta.get('chapter')}.{meta.get('verse')} — {meta.get('chapter_name_en')}"
            sources.append(
                {
                    "id": meta.get("id"),
                    "title": title,
                    "type": meta.get("type"),
                    "source": meta.get("source"),
                }
            )
        return sources

    def invoke(self, query: str, language: str = "auto", conversation_id: str | None = None) -> dict:
        resolved_language = language if language and language != "auto" else detect_language(query)

        direct_ref = self._detect_direct_verse_ref(query)
        if direct_ref:
            hits = self._direct_verse_hit(*direct_ref)
        else:
            retrieval_query = rewrite_query_for_retrieval(self.groq_client, query)
            hits = self.retrieve(retrieval_query)

        context = self.format_context(hits)
        sources = self.format_sources(hits)

        prompt = SYSTEM_PROMPT.format(context=context, query=query)
        completion = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=700,
        )
        response_text = completion.choices[0].message.content

        return {
            "response": response_text,
            "sources": sources,
            "language": resolved_language,
        }
