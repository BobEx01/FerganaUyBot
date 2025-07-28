from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import BOT_TOKEN, CATEGORIES, WELCOME_TEXT

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# 🔹 /start komandasi - asosiy menyuni chiqaradi
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for cat in CATEGORIES:
        keyboard.add(KeyboardButton(cat["name"]))
    await message.answer(WELCOME_TEXT, reply_markup=keyboard)

# 🔹 Kategoriya tugmalariga javob
@dp.message_handler(lambda message: message.text in [c["name"] for c in CATEGORIES])
async def category_selected(message: types.Message):
    selected = message.text
    if "Kvartira" in selected:
        await message.answer("🏢 Kvartira e’loni uchun kerakli ma’lumotlarni yuboring.")
    elif "Hovli" in selected or "Uchastka" in selected:
        await message.answer("🏡 Hovli / Uchastka e’loni uchun kerakli ma’lumotlarni yuboring.")
    elif "Yer" in selected:
        await message.answer("🌾 Yer e’loni uchun kerakli ma’lumotlarni yuboring.")
    else:
        await message.answer("Noma’lum turdagi tanlov!")

# 🔹 Matn yuborilganda
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    await message.answer("Iltimos, quyidagi tugmalardan birini tanlang yoki /start buyrug‘ini yuboring.")

# 🔹 Botni ishga tushurish
if name == '__main__':
    print("✅ Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
