import json
import os
import threading
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDBACK_PATH = os.path.join(BASE, "data", "feedback.jsonl")

_lock = threading.Lock()


def save_feedback(message_id: str, rating: int, comment: str | None) -> None:
    record = {
        "message_id": message_id,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with _lock:
        with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
