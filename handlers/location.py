from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from states.ad_state import AdState

# 🔹 Lokatsiya yuborilganda
@dp.message_handler(content_types=types.ContentType.LOCATION, state=AdState.location)
async def get_location(message: types.Message, state: FSMContext):
    location = message.location
    await state.update_data(location={'lat': location.latitude, 'lon': location.longitude})
    await ask_price(message, state)

# 🔹 Matn bilan manzil yozilganda
@dp.message_handler(content_types=types.ContentType.TEXT, state=AdState.location)
async def get_location_text(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        # Orqaga – kategoriyaga qaytish
        from handlers.menu import send_main_menu
        await send_main_menu(message, state)
        return
    await state.update_data(location_text=message.text)
    await ask_price(message, state)

# 🔹 Narx so‘rash funksiyasi
async def ask_price(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🔙 Orqaga"))
    await message.answer("💰 Narxni kiriting:", reply_markup=kb)
    await AdState.price.set()
