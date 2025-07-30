from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from states.ad_state import AdState

# 🔹 Qulayliklarni qabul qilish
@dp.message_handler(state=AdState.amenities)
async def get_amenities(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        from handlers.price import get_price  # narxga qaytish
        await message.answer("💰 Narxni kiriting:", reply_markup=types.ReplyKeyboardRemove())
        await AdState.price.set()
        return

    data = await state.get_data()
    amenities = data.get("amenities", [])

    if message.text == "Davom etish":
        await state.update_data(amenities=amenities)
        await ask_photos(message)
        await AdState.photos.set()
        return

    amenities.append(message.text)
    await state.update_data(amenities=amenities)
    await message.answer(f"✅ Qulaylik qo‘shildi: {message.text}\nYana qulaylik tanlang yoki 'Davom etish' ni bosing.")
    
# 🔹 Suratlarni so‘rash
async def ask_photos(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Davom etish"), KeyboardButton("🔙 Orqaga"))
    await message.answer("🖼 Suratlarni yuboring (10 tagacha):", reply_markup=kb)
