from config import BLOCKED_WORDS

def has_blocked_words(text: str) -> bool:
    """
    Matnda taqiqlangan so‘zlar bor-yo‘qligini tekshiradi
    """
    text_lower = text.lower()
    for word in BLOCKED_WORDS:
        if word in text_lower:
            return True
    return False
