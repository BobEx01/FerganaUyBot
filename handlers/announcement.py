from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.common import back_button
from config import CHANNELS
from filters.filter import is_clean_text

class AnnouncementStates(StatesGroup):
    category = State()
    description = State()
    photos = State()
    confirm = State()

async def start_announcement(message: types.Message, state: FSMContext):
    await AnnouncementStates.category.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key, name in CHANNELS.items():
        keyboard.add(key.capitalize())
    keyboard.add("🔙 Orqaga")
    await message.answer("Qaysi turdagi e’lon bermoqchisiz?", reply_markup=keyboard)

async def set_category(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await message.answer("🏠 Asosiy menyuga qaytdingiz.", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return

    category = message.text.lower()
    if category not in CHANNELS:
        await message.answer("Noto‘g‘ri kategoriya. Iltimos, qaytadan tanlang.")
        return

    await state.update_data(category=category)
    await AnnouncementStates.next()
    await message.answer("E’lon uchun qisqacha tavsif yozing:", reply_markup=back_button())

async def set_description(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await AnnouncementStates.category.set()
        return await start_announcement(message, state)

    if not is_clean_text(message.text):
        await message.answer("❌ Tavsifda nomaqbul so‘zlar bor. Iltimos, toza matn kiriting.")
        return

    await state.update_data(description=message.text)
    await AnnouncementStates.next()
    await message.answer("📷 Endi e’lon uchun rasmlar yuboring (maks: 10 ta). Tugatgach /send deb yozing.", reply_markup=back_button())

async def collect_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.text == "🔙 Orqaga":
        await AnnouncementStates.description.set()
        return await set_description(message, state)

    if message.content_type == "photo":
        photos.append(message.photo[-1].file_id)
        await state.update_data(photos=photos)

        if len(photos) >= 10:
            await AnnouncementStates.confirm.set()
            return await message.answer("📌 E’lon tayyor. Yuborilsinmi? /send deb yuboring.")
        else:
            return await message.answer(f"✅ {len(photos)} ta rasm qabul qilindi.")

    else:
        await message.answer("Faqatgina rasm yuboring yoki /send buyrug‘ini yozing.")

async def send_announcement(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    description = data["description"]
    photos = data.get("photos", [])

    channel = CHANNELS.get(category)

    media = types.MediaGroup()
    for photo_id in photos[:10]:
        media.attach_photo(photo_id)

    await message.answer("📤 E’loningiz yuborilmoqda...")

    if media.media:
        await message.bot.send_media_group(chat_id=channel, media=media)
    await message.bot.send_message(chat_id=channel, text=description)

    await message.answer("✅ E’lon muvaffaqiyatli joylandi!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("🏠 Siz bosh menyudasiz.", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("🏠 Asosiy menyu"))
    await state.finish()

def register_announcement(dp):
    from aiogram.dispatcher import Dispatcher
    dp.register_message_handler(start_announcement, lambda msg: msg.text.lower() == "elon berish", state="*")
    dp.register_message_handler(set_category, state=AnnouncementStates.category)
    dp.register_message_handler(set_description, content_types=types.ContentTypes.TEXT, state=AnnouncementStates.description)
    dp.register_message_handler(collect_photos, content_types=types.ContentTypes.PHOTO | types.ContentTypes.TEXT, state=AnnouncementStates.photos)
    dp.register_message_handler(send_announcement, commands=["send"], state="*")
