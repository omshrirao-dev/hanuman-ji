"""
Embeds katha_teachings.json and gita_shlokas.json into two persistent
ChromaDB collections using a multilingual embedding model, so Hindi and
English queries land in the same vector space.

Run after any change to data/processed/*.json:
    .venv/Scripts/python.exe -m app.build_index
"""
import gc
import json
import os
import time

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.documents import gita_to_document, katha_to_document

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(BASE, "data", "processed")
CHROMA_DIR = os.path.join(BASE, "data", "chroma")
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
BATCH_SIZE = 16


def build():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    with open(os.path.join(PROCESSED, "katha_teachings.json"), encoding="utf-8") as f:
        katha_entries = json.load(f)

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
    del katha_entries, katha_docs, katha_ids
    gc.collect()

    with open(os.path.join(PROCESSED, "gita_shlokas.json"), encoding="utf-8") as f:
        gita_entries = json.load(f)
    # Chapter 1 (Arjuna Vishada Yoga) is Arjuna's problem statement, not
    # Krishna's teaching — battlefield setup with no practical_action. It kept
    # surfacing for despair/fear/anger queries on resonance alone, with no
    # actual counsel attached. Krishna's response starts at chapter 2, so
    # chapter 1 is excluded from the retrievable/citable index.
    gita_entries = [e for e in gita_entries if e["chapter"] != 1]
    gita_docs = [gita_to_document(e) for e in gita_entries]
    gita_ids = [e["id"] for e in gita_entries]

    gita_store = Chroma(
        collection_name="gita_shlokas",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
        collection_metadata={"hnsw:space": "cosine"},
    )
    total = len(gita_docs)
    for i in range(0, total, BATCH_SIZE):
        gita_store.add_documents(
            documents=gita_docs[i : i + BATCH_SIZE],
            ids=gita_ids[i : i + BATCH_SIZE],
        )
        print(f"  ...gita batch {i // BATCH_SIZE + 1}/{-(-total // BATCH_SIZE)} embedded")
        gc.collect()
        time.sleep(0.5)
    print(f"Embedded {total} gita shlokas into collection 'gita_shlokas'")


if __name__ == "__main__":
    build()
