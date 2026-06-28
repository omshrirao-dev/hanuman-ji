"""
Embeds katha_teachings.json and gita_shlokas.json into two persistent
ChromaDB collections using a multilingual embedding model, so Hindi and
English queries land in the same vector space.

Run after any change to data/processed/*.json:
    .venv/Scripts/python.exe -m app.build_index
"""
import json
import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.documents import gita_to_document, katha_to_document

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(BASE, "data", "processed")
CHROMA_DIR = os.path.join(BASE, "data", "chroma")
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


def build():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    with open(os.path.join(PROCESSED, "katha_teachings.json"), encoding="utf-8") as f:
        katha_entries = json.load(f)
    with open(os.path.join(PROCESSED, "gita_shlokas.json"), encoding="utf-8") as f:
        gita_entries = json.load(f)
    # Chapter 1 (Arjuna Vishada Yoga) is Arjuna's problem statement, not
    # Krishna's teaching — battlefield setup with no practical_action. It kept
    # surfacing for despair/fear/anger queries on resonance alone, with no
    # actual counsel attached. Krishna's response starts at chapter 2, so
    # chapter 1 is excluded from the retrievable/citable index.
    gita_entries = [e for e in gita_entries if e["chapter"] != 1]

    katha_docs = [katha_to_document(e) for e in katha_entries]
    katha_ids = [e["id"] for e in katha_entries]
    Chroma.from_documents(
        documents=katha_docs,
        ids=katha_ids,
        embedding=embeddings,
        collection_name="katha_teachings",
        persist_directory=CHROMA_DIR,
        collection_metadata={"hnsw:space": "cosine"},
    )
    print(f"Embedded {len(katha_docs)} katha entries into collection 'katha_teachings'")

    gita_docs = [gita_to_document(e) for e in gita_entries]
    gita_ids = [e["id"] for e in gita_entries]
    Chroma.from_documents(
        documents=gita_docs,
        ids=gita_ids,
        embedding=embeddings,
        collection_name="gita_shlokas",
        persist_directory=CHROMA_DIR,
        collection_metadata={"hnsw:space": "cosine"},
    )
    print(f"Embedded {len(gita_docs)} gita shlokas into collection 'gita_shlokas'")


if __name__ == "__main__":
    build()
