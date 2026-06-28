import re

_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize_query(text: str) -> str:
    text = _CONTROL_CHARS_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:500]
