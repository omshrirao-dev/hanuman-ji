"""Shared Document construction for both the offline indexer (build_index.py)
and the live pipeline (rag_pipeline.py's direct verse-lookup bypass)."""
from langchain_core.documents import Document


def _join(values):
    return ", ".join(values) if values else ""


def katha_to_document(entry: dict) -> Document:
    text = "\n".join(
        [
            entry["title_en"],
            entry["story_summary"],
            f"Core lesson: {entry['core_lesson']}",
            f"Themes: {_join(entry['themes'])}",
            f"Emotions: {_join(entry['emotions'])}",
            f"Life situations: {_join(entry['life_situations'])}",
            f"Practical action: {entry['practical_action']}",
            entry["full_text"],
        ]
    )
    metadata = {
        "id": entry["id"],
        "type": entry["type"],
        "title": entry["title"],
        "title_en": entry["title_en"],
        "themes": _join(entry["themes"]),
        "emotions": _join(entry["emotions"]),
        "life_situations": _join(entry["life_situations"]),
        "core_lesson": entry["core_lesson"],
        "practical_action": entry["practical_action"],
        "source": entry["source"],
        "day": entry["day"] if entry["day"] is not None else -1,
    }
    return Document(page_content=text, metadata=metadata)


def gita_to_document(entry: dict) -> Document:
    # Emotions/life_situations are NOT embedded even though every verse has
    # them: for the ~675 non-priority verses they're a generic, repeated
    # chapter-level blob (e.g. 47 chapter-1 verses all say "grief, fear,
    # despair"). Embedding that text let chapters with many verses
    # statistically dominate any distress query, drowning out the few
    # specific, well-matched katha entries. Tried embedding it for the 26
    # priority verses too (to bridge their formal scriptural register to
    # colloquial query phrasing) — net regression: it made priority verses
    # lexically "supercharged" with emotion words and let them out-compete
    # katha entries broadly. Kept metadata-only everywhere; the rerank bonus
    # (PRIORITY_BONUS + token overlap) is the right place for this signal.
    text = "\n".join(
        [
            f"Bhagavad Gita {entry['chapter']}.{entry['verse']} — {entry['chapter_name_en']} ({entry['chapter_theme']})",
            f"Core lesson: {entry['core_lesson']}",
            entry["hindi"],
            entry["english"],
        ]
    )
    metadata = {
        "id": entry["id"],
        "type": entry["type"],
        "chapter": entry["chapter"],
        "verse": entry["verse"],
        "chapter_name_en": entry["chapter_name_en"],
        "chapter_theme": entry["chapter_theme"],
        "emotions": _join(entry["emotions"]),
        "life_situations": _join(entry["life_situations"]),
        "core_lesson": entry["core_lesson"],
        "practical_action": entry["practical_action"] or "",
        "priority": entry["priority"],
        "source": entry["source"],
    }
    return Document(page_content=text, metadata=metadata)
