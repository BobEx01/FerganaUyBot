from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.menu import main_menu

# ⬅️ Orqaga tugmasi ishlovchisi
async def handle_back(message: types.Message):
    await message.answer("🔙 Asosiy menyuga qaytdingiz:", reply_markup=main_menu())

def register_back_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_back, lambda msg: msg.text == "⬅️ Orqaga")
