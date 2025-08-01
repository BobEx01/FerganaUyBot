from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers.start import register_start_handlers
from handlers.ad_creation import register_ad_creation_handlers
from handlers.back import register_back_handlers
from handlers.confirmation import register_confirmation_handlers

# FSM uchun xotira
storage = MemoryStorage()

# Bot va dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

# Barcha handlerlarni ro‘yxatdan o‘tkazamiz
register_start_handlers(dp)
register_ad_creation_handlers(dp)
register_back_handlers(dp)
register_confirmation_handlers(dp)

if __name__ == "__main__":
    print("✅ FerganaUyBot ishga tushdi!")
    executor.start_polling(dp, skip_updates=True)
