from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from states.ad_state import AdState

# 🔹 Narxni qabul qilish
@dp.message_handler(state=AdState.price)
async def get_price(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        from handlers.location import ask_price  # import qilish kerak bo‘ladi
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.add(KeyboardButton("📍 Lokatsiya yuborish"), KeyboardButton("🔙 Orqaga"))
        await message.answer("📍 Manzilni kiriting yoki lokatsiya yuboring:", reply_markup=kb)
        await AdState.location.set()
        return

    await state.update_data(price=message.text)
    await ask_amenities(message, state)

# 🔹 Uy qulayliklarini so‘rash funksiyasi
async def ask_amenities(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("Remont qilingan"), KeyboardButton("Yangi uy"),
        KeyboardButton("Avtoturargoh"), KeyboardButton("Balkon"),
        KeyboardButton("Isitish tizimi"), KeyboardButton("Hovli / Bog‘"),
        KeyboardButton("Davom etish"), KeyboardButton("🔙 Orqaga")
    )
    await message.answer("🏠 Qulayliklarni tanlang (bir nechtasini yuboring):", reply_markup=kb)
    await AdState.amenities.set()
