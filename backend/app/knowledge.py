import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(BASE, "data", "processed")

_cache: list[dict] | None = None


def all_sources() -> list[dict]:
    global _cache
    if _cache is not None:
        return _cache

    with open(os.path.join(PROCESSED, "katha_teachings.json"), encoding="utf-8") as f:
        katha = json.load(f)
    with open(os.path.join(PROCESSED, "gita_shlokas.json"), encoding="utf-8") as f:
        gita = json.load(f)

    entries = []
    for e in katha:
        entries.append(
            {
                "id": e["id"],
                "type": e["type"],
                "title": e["title"],
                "title_en": e["title_en"],
                "themes": e["themes"],
                "core_lesson": e["core_lesson"],
                "source": e["source"],
            }
        )
    for e in gita:
        entries.append(
            {
                "id": e["id"],
                "type": e["type"],
                "title": f"{e['chapter']}.{e['verse']} — {e['chapter_name_en']}",
                "title_en": e["chapter_name_en"],
                "themes": [e["chapter_theme"]],
                "core_lesson": e["core_lesson"],
                "source": e["source"],
            }
        )

    _cache = entries
    return entries
