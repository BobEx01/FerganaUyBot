from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🔘 Bosh menyu tugmalari
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📤 E'lon berish"))
    kb.add(KeyboardButton("👀 E'lonlarni ko‘rish"))
    return kb

# 📤 E’lon kategoriyalari
def post_categories():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("🏢 Kvartira"),
        KeyboardButton("🏡 Hovli / Uchastka"),
        KeyboardButton("🌾 Yer maydoni")
    )
    kb.add(KeyboardButton("⬅️ Orqaga"))
    return kb

# 👀 E’lon ko‘rish kanallari
def view_ads_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📌 Kvartira kanali"),
        KeyboardButton("📌 Uchastka kanali"),
        KeyboardButton("📌 Yer kanali")
    )
    kb.add(KeyboardButton("⬅️ Orqaga"))
    return kb
