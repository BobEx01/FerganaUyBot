from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from states.ad_state import AdState
from handlers.confirm import show_summary

MAX_DESCRIPTION_LENGTH = 1000

@dp.message_handler(state=AdState.description)
async def get_description(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        from handlers.photos import ask_description  # To'g'ri o'tish uchun
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("Davom etish"), KeyboardButton("🔙 Orqaga"))
        await message.answer("🖼 Surat yuboring yoki 'Davom etish' tugmasini bosing.", reply_markup=kb)
        await AdState.photos.set()
        return

    if len(message.text) > MAX_DESCRIPTION_LENGTH:
        await message.answer("❗️ Tavsif juda uzun. Iltimos, 1000 belgidan kam yozing.")
        return

    await state.update_data(description=message.text)

    # Tasdiqqa o‘tish
    await show_summary(message, state)
    await AdState.confirm.set()
