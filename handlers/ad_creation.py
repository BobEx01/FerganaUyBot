from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.menu import main_menu, post_categories, view_ads_menu

# 📤 E'lon berish
async def handle_post_ad(message: types.Message):
    await message.answer("Iltimos, elon turini tanlang:", reply_markup=post_categories())

# 👀 E'lonlarni ko‘rish
async def handle_view_ads(message: types.Message):
    await message.answer(
        "Quyidagi kanallar orqali e’lonlarni ko‘rishingiz mumkin:",
        reply_markup=view_ads_menu()
    )

# 📌 Kanalga ssilkalar
async def handle_channel_links(message: types.Message):
    if "Kvartira" in message.text:
        await message.answer("📌 https://t.me/KvartiraFergana")
    elif "Uchastka" in message.text:
        await message.answer("📌 https://t.me/UchastkaFergana")
    elif "Yer" in message.text:
        await message.answer("📌 https://t.me/YerlarFergana")

# ⬅️ Orqaga
async def handle_back(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=main_menu())

# ✅ ENDI SHU QISM QO‘SHILDI:
def register_ad_creation_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_post_ad, lambda msg: msg.text == "📤 E'lon berish")
    dp.register_message_handler(handle_view_ads, lambda msg: msg.text == "👀 E'lonlarni ko‘rish")
    dp.register_message_handler(handle_channel_links, lambda msg: "kanali" in msg.text)
    dp.register_message_handler(handle_back, lambda msg: msg.text == "⬅️ Orqaga")
