import re

from langdetect import LangDetectException, detect

DEVANAGARI_RE = re.compile(r"[ऀ-ॿ]")

HINGLISH_MARKERS = {
    "hai", "nahi", "nahin", "mujhe", "mera", "meri", "kya", "kyun", "kyu",
    "tension", "pareshan", "pareshaan", "dukh", "shanti", "naukri", "paisa",
    "ghar", "bahut", "karu", "karna", "raha", "rahi", "hoon", "hu", "acha",
    "accha", "thik", "theek", "kuch", "sab", "kaise", "kaun", "kab",
}


def detect_language(text: str) -> str:
    """Returns 'hi' (Hindi/Devanagari), 'hi-en' (Hinglish/romanized Hindi), or 'en'."""
    if DEVANAGARI_RE.search(text):
        return "hi"

    tokens = set(re.findall(r"[a-zA-Z]+", text.lower()))
    hinglish_hits = tokens & HINGLISH_MARKERS
    if hinglish_hits:
        return "hi-en"

    try:
        code = detect(text)
    except LangDetectException:
        return "en"
    return "hi" if code == "hi" else "en"
