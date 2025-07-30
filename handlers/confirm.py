from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto

from loader import dp, bot
from states.ad_state import AdState
from config import CHANNELS

@dp.message_handler(state=AdState.confirm)
async def confirm_post(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        from handlers.description import get_description
        await message.answer("📋 E’lon uchun tavsif yozing (1000 belgigacha):", reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True).add(KeyboardButton("🔙 Orqaga")))
        await AdState.description.set()
        return

    if message.text != "Tasdiqlash":
        await message.answer("Iltimos, 'Tasdiqlash' yoki '🔙 Orqaga' tugmasini bosing.")
        return

    data = await state.get_data()
    category = data.get("category")
    photos = data.get("photos", [])
    location = data.get("location", {})
    description = data.get("description", "")

    text = f"📢 Yangi e’lon:\n\n📂 Kategoriya: {category}\n"
    if location:
        text += f"📍 Joylashuv: {location.get('city', '')}, {location.get('district', '')}\n"
    text += f"\n📝 Tavsif:\n{description}"

    # Kanalga yuborish
    channel_id = CHANNELS.get(category)
    if not channel_id:
        await message.answer("❌ Kanal topilmadi.")
        return

    if photos:
        media = [InputMediaPhoto(media=p) for p in photos[:10]]
        media[0].caption = text
        await bot.send_media_group(chat_id=channel_id, media=media)
    else:
        await bot.send_message(chat_id=channel_id, text=text)

    await message.answer("✅ E’lon muvaffaqiyatli joylandi!", reply_markup=ReplyKeyboardMarkup(
        resize_keyboard=True).add(KeyboardButton("🏠 Bosh menyu")))

    await state.finish()
