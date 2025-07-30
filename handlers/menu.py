from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.menu import category_keyboard
from config import CATEGORIES

async def menu_handler(message: types.Message):
    await message.answer("Iltimos, kategoriya tanlang:", reply_markup=category_keyboard())

async def category_chosen(message: types.Message):
    selected = message.text
    if "Kvartira" in selected:
        await message.answer("🏢 Kvartira e’loni uchun kerakli ma’lumotlarni yuboring.")
    elif "Hovli" in selected or "Uchastka" in selected:
        await message.answer("🏡 Hovli / Uchastka e’loni uchun kerakli ma’lumotlarni yuboring.")
    elif "Yer" in selected:
        await message.answer("🌾 Yer e’loni uchun kerakli ma’lumotlarni yuboring.")
    else:
        await message.answer("Noma’lum kategoriya tanlandi.")

def register_menu(dp: Dispatcher):
    dp.register_message_handler(menu_handler, lambda msg: msg.text == "🏠 Asosiy menyu")
    dp.register_message_handler(category_chosen, lambda msg: msg.text in [c["name"] for c in CATEGORIES])
