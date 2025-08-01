from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.menu import main_menu
from config import WELCOME_TEXT

async def start_command(message: types.Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_menu())

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
