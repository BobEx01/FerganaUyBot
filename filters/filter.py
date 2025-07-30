from config import BLOCKED_WORDS

def is_clean_text(text: str) -> bool:
    """So‘kinish so‘zlari bor-yo‘qligini tekshiradi."""
    text_lower = text.lower()
    for word in BLOCKED_WORDS:
        if word in text_lower:
            return False
    return True
