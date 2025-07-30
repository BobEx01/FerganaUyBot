from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from states.ad_state import AdState

MAX_PHOTOS = 10  # configda ham bor

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=AdState.photos)
async def get_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])

    if len(photos) >= MAX_PHOTOS:
        await message.answer("❗️10 tagacha rasm yuborish mumkin.")
        return

    file_id = message.photo[-1].file_id
    photos.append(file_id)
    await state.update_data(photos=photos)
    await message.answer(f"✅ Rasm qabul qilindi. {len(photos)} ta rasm yuklandi.")

@dp.message_handler(state=AdState.photos)
async def photos_controls(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        from handlers.amenities import get_amenities
        await message.answer("🏘 Qulayliklarni tanlang:", reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True).add(KeyboardButton("Davom etish"), KeyboardButton("🔙 Orqaga")))
        await AdState.amenities.set()
        return

    if message.text == "Davom etish":
        await ask_description(message)
        await AdState.description.set()
    else:
        await message.answer("🖼 Rasm yuboring yoki 'Davom etish' tugmasini bosing.")

# 🔹 Tavsif bosqichiga o‘tish
async def ask_description(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🔙 Orqaga"))
    await message.answer("📝 E'lon tavsifini yozing (1000 ta belgigacha):", reply_markup=kb)
