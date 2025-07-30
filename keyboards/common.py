from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# 🔙 Orqaga qaytish tugmasi
back_button = KeyboardButton("⬅️ Orqaga")

# 📍 Kategoriyalar uchun tugmalar (asosiy menyu)
def category_keyboard(categories):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for cat in categories:
        kb.add(KeyboardButton(cat["name"]))
    return kb

# 📍 Viloyat va tuman tanlash uchun
def location_keyboard(options):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        kb.add(KeyboardButton(option))
    kb.add(back_button)
    return kb

# ✅ Ha / Yo‘q tugmalari
def yes_no_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("✅ Ha"), KeyboardButton("❌ Yo‘q"))
    kb.add(back_button)
    return kb

# 📤 Tasdiqlash / Bekor qilish tugmalari
def confirm_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ E'lonni tasdiqlash", callback_data="confirm"),
        InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")
    )
    return markup
