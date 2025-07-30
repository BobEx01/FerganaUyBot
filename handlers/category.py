from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from states.ad_state import AdState
from config import CATEGORIES

# 🔹 Kategoriya nomlarini olish
CATEGORY_NAMES = [c["name"] for c in CATEGORIES]

# 🔹 Kategoriya tanlanganida ishga tushadi
@dp.message_handler(lambda message: message.text in CATEGORY_NAMES, state='*')
async def choose_category(message: types.Message, state: FSMContext):
    selected = message.text
    await state.update_data(category=selected)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📍 Joylashuvni yuborish"), KeyboardButton("🔙 Orqaga"))
    await message.answer(f"{selected} uchun joylashuvni yuboring yoki '🔙 Orqaga' bosing.", reply_markup=kb)
    await AdState.location.set()
