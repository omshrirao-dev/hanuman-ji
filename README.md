# हनुमान जी | Hanuman Ji — AI Spiritual Guide

> जीवन की हर उलझन का उत्तर — शिव महापुराण और भगवद्गीता की वाणी में
> Every life problem has an answer — in the wisdom of Shiv Mahapuran and Bhagavad Gita.

**Live:** _deploying_ | Voice-enabled | Hindi + English + Hinglish
**Monitored live by [Kavacha](https://github.com/omshrirao-dev/kavacha)** — my AI-maintenance infrastructure

A multilingual RAG system over the Bhagavad Gita (701 shlokas across 18 chapters) and
Shiv Mahapuran katha teachings (28 teachings + 5 upays, from Pandit Pradeep Ji Mishra's
2026 Bathinda katha). It understands the *emotion* and *life situation* behind a message
— not just keyword overlap — and responds with the matching wisdom, in your language,
with voice.

> "naukri nahi mil rahi" → understands the emotion (hopelessness), the situation (career
> failure), and surfaces the sadhu-and-patience teaching whose *lesson* fits — even though
> the word "naukri" never appears in that story.

## How it works

```
User (voice or text)
  → language detection (Hindi / English / Hinglish)
  → query rewritten to an English emotional gloss (a small Groq call — romanized
    Hindi embeds poorly in the multilingual model used directly)
  → semantic search across two ChromaDB collections (katha_teachings, gita_shlokas)
  → re-ranked by emotion / life-situation metadata overlap
  → top 3 passed to Llama 3.3 70B (Groq) with a strict grounding system prompt
  → response: empathy → relevant story/shloka → connection to their situation →
    one practical action → hope — always cited, never invented
  → spoken aloud via the Web Speech API
```

Direct scripture citations (e.g. "BG 2.47 ka arth?") skip semantic search entirely —
embeddings can't reliably represent exact numeric references, so a regex match short-circuits
straight to the verse.

## Tech stack

Python · FastAPI · LangChain · ChromaDB · `paraphrase-multilingual-MiniLM-L12-v2`
(Hindi + English in one 384-dim vector space) · Groq (Llama 3.3 70B) · React · Tailwind ·
Web Speech API (STT + TTS) · Railway · Vercel

## Project structure

```
backend/
  app/                  FastAPI app, RAG pipeline, query understanding, prompts
  data/raw/             Source katha document + the gita/gita verse dataset
  data/processed/       katha_teachings.json, gita_shlokas.json, ingest_gita.py
  data/chroma/          Persisted vector store (built by app/build_index.py)
frontend/
  src/pages/            Landing, Chat, About
  src/hooks/            useSpeechRecognition, useSpeechSynthesis
  src/lib/               API client, localStorage conversation history
docs/                   Original product specs
```

## Run locally

```bash
# Backend
cd backend
python -m venv .venv && .venv/Scripts/activate   # or source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your GROQ_API_KEY
python -m app.build_index   # embeds the knowledge base into ./data/chroma
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Knowledge base

Every entry — katha teaching, upay, or Gita verse — carries `emotions[]`,
`life_situations[]`, and a `core_lesson`, hand-annotated so retrieval matches what
someone is *going through*, not the words they used. 26 of the most pivotal Gita
verses (concentrated in chapters 2, 3, 6, 11, 18) get this treatment individually;
the rest inherit chapter-level context. New source documents can be added without
touching the pipeline — see `data/processed/ingest_gita.py` as the pattern to follow
for additional texts.

## The two-project ecosystem

Hanuman Ji is the product; [Kavacha](https://github.com/omshrirao-dev/kavacha) is the
infrastructure that watches it — hallucinated-shloka detection, cost-vs-budget tracking,
response-drift monitoring, and an automated review agent. Both built and deployed solo.

## Disclaimer

हनुमान जी एक AI आधारित आध्यात्मिक सहायक है। गंभीर स्वास्थ्य, कानूनी, या मानसिक समस्याओं के
लिए कृपया योग्य विशेषज्ञ से परामर्श लें।

Hanuman Ji is an AI spiritual assistant. For serious health, legal, or mental health
concerns, please consult a qualified professional. Conversations are stored only in
your browser.

---
*हर हर महादेव · जय हनुमान* 🙏
