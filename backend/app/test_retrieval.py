"""
Retrieval quality check, run before wiring up full response generation.
Runs 10 cross-language queries (career/money/family/peace/relationship in
Hindi/English/Hinglish) through the same direct-verse-lookup / query-rewrite
/ embed / rerank path the live pipeline uses, and reports hit rate against
expected ids.

    .venv/Scripts/python.exe -m app.test_retrieval
"""
from dotenv import load_dotenv

load_dotenv()

from app.query_understanding import rewrite_query_for_retrieval
from app.rag_pipeline import RAGPipeline

TEST_CASES = [
    ("naukri nahi mil rahi, bahut tension hai", {"T-07"}),
    ("I can't sleep, money stress is killing me", {"T-01", "T-06", "T-10", "T-16"}),
    ("ghar mein shanti nahi hai", {"T-09", "T-10", "T-16"}),
    ("mujhe paise ki tension hai", {"T-01", "T-06"}),
    ("career mein bahut failure mil rahi hai, himmat toot rahi hai", {"T-07", "BG-2.47"}),
    ("kisi ne mere saath dhoka diya, bahut gussa aa raha hai", {"T-14", "T-18", "BG-2.62"}),
    ("I feel so anxious all the time and can't focus on anything", {"T-09", "BG-6.5", "BG-6.6", "BG-6.35"}),
    ("relationship mein problems hain, partner se ladhai hoti rehti hai", {"T-09", "T-14"}),
    ("BG 2.47 ka arth kya hai?", {"BG-2.47"}),
    ("meri maa bahut bimar hai, dar lag raha hai usse kho dene ka", {"T-12", "BG-2.20"}),
]


def main():
    pipeline = RAGPipeline()
    hits_count = 0
    for query, expected in TEST_CASES:
        direct_ref = pipeline._detect_direct_verse_ref(query)
        if direct_ref:
            hits = pipeline._direct_verse_hit(*direct_ref)
            rewritten = f"<direct lookup BG {direct_ref[0]}.{direct_ref[1]}>"
        else:
            rewritten = rewrite_query_for_retrieval(pipeline.groq_client, query)
            hits = pipeline.retrieve(rewritten, top_n=5)
        top_ids = [doc.metadata.get("id") for doc, _ in hits]

        matched = bool(set(top_ids[:3]) & expected)
        hits_count += matched
        flag = "OK " if matched else "MISS"
        print(f"[{flag}] query={query!r}")
        print(f"       rewritten={rewritten!r}")
        print(f"       expected~{expected} got_top5={top_ids}")

    print(f"\n{hits_count}/{len(TEST_CASES)} queries had an expected id in their top 3")


if __name__ == "__main__":
    main()
