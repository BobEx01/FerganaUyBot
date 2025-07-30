from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, bot
from config import CHANNELS, BLOCKED_WORDS, CATEGORIES
from utils.filters import has_blocked_words

# 🔹 Holatlar sinfi
class AdForm(StatesGroup):
    category = State()
    location = State()
    size = State()
    amenities = State()
    communications = State()
    price = State()
    photos = State()
    confirm = State()

# 🔹 "🔙 Orqaga" tugmasi
back_button = KeyboardButton("🔙 Orqaga")
back_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(back_button)

# 🔹 E’lon berishni boshlash
@dp.message_handler(lambda m: m.text in [cat["name"] for cat in CATEGORIES])
async def start_ad_form(message: types.Message, state: FSMContext):
    cat_key = next((cat["key"] for cat in CATEGORIES if cat["name"] == message.text), None)
    await state.update_data(category=cat_key)
    await message.answer("📍 Joylashuvni yozing (masalan: Farg‘ona shahar, Marg‘ilon ko‘chasi):", reply_markup=back_markup)
    await AdForm.location.set()

# 🔹 Joylashuv
@dp.message_handler(state=AdForm.location)
async def set_location(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await message.answer("Qaysi turdagi e’lon bermoqchisiz?", reply_markup=start_menu())
        await state.finish()
        return
    await state.update_data(location=message.text)
    await message.answer("📐 Maydonni yozing (kv.m yoki sotix):", reply_markup=back_markup)
    await AdForm.size.set()

# 🔹 Maydon
@dp.message_handler(state=AdForm.size)
async def set_size(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await message.answer("📍 Joylashuvni yozing:", reply_markup=back_markup)
        await AdForm.location.set()
        return
    await state.update_data(size=message.text)
    await message.answer("🏠 Qulayliklarni yozing (masalan: balkon, isitish):", reply_markup=back_markup)
    await AdForm.amenities.set()

# 🔹 Qulayliklar
@dp.message_handler(state=AdForm.amenities)
async def set_amenities(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await message.answer("📐 Maydonni yozing:", reply_markup=back_markup)
        await AdForm.size.set()
        return
    await state.update_data(amenities=message.text)
    await message.answer("🔌 Kommunikatsiyalar (gaz, suv, svet, internet):", reply_markup=back_markup)
    await AdForm.communications.set()

# 🔹 Kommunikatsiyalar
@dp.message_handler(state=AdForm.communications)
async def set_communications(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await message.answer("🏠 Qulayliklarni yozing:", reply_markup=back_markup)
        await AdForm.amenities.set()
        return
    await state.update_data(communications=message.text)
    await message.answer("💰 Narxni yozing (so‘mda):", reply_markup=back_markup)
    await AdForm.price.set()

# 🔹 Narx
@dp.message_handler(state=AdForm.price)
async def set_price(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await message.answer("🔌 Kommunikatsiyalar:", reply_markup=back_markup)
        await AdForm.communications.set()
        return
    await state.update_data(price=message.text)
    await message.answer("🖼 Rasmlarni yuboring (1–10 ta):")
    await AdForm.photos.set()

# 🔹 Rasm qabul qilish
@dp.message_handler(content_types=types.ContentType.PHOTO, state=AdForm.photos)
async def receive_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(message.photo[-1].file_id)

    if len(photos) >= 10:
        await state.update_data(photos=photos)
        await confirm_ad(message, state)
        return

    await state.update_data(photos=photos)
    await message.answer(f"✅ {len(photos)} rasm qabul qilindi. Yana yuboring yoki /ok ni bosing.
  ")

# 🔹 Yuborishni tugatish
@dp.message_handler(commands=["ok"], state=AdForm.photos)
async def done_uploading_photos(message: types.Message, state: FSMContext):
    await confirm_ad(message, state)

# 🔹 E’lonni yakuniy tasdiqlash
async def confirm_ad(message, state):
    data = await state.get_data()
    if has_blocked_words(data):
        await message.answer("🚫 E’londa nomaqbul so‘zlar mavjud. Qaytadan urinib ko‘ring.")
        await state.finish()
        return

    caption = (
        f"📢 Yangi e’lon:\n"
        f"📍 Joylashuv: {data['location']}\n"
        f"📐 Maydon: {data['size']}\n"
        f"🏠 Qulayliklar: {data['amenities']}\n"
        f"🔌 Kommunikatsiyalar: {data['communications']}\n"
        f"💰 Narx: {data['price']} so‘m\n"
        f"📞 Aloqa: @{message.from_user.username if message.from_user.username else 'Telefon raqam yo‘q'}"
    )

    channel_id = CHANNELS.get(data["category"])
    if not channel_id:
        await message.answer("Xatolik yuz berdi. Kanal aniqlanmadi.")
        await state.finish()
        return

    media = types.MediaGroup()
    for i, photo_id in enumerate(data["photos"]):
        if i == 0:
            media.attach_photo(photo_id, caption=caption)
        else:
            media.attach_photo(photo_id)
    await bot.send_media_group(chat_id=channel_id, media=media)

    await message.answer("✅ E’loningiz yuborildi! Bosh menyuga qaytdik.", reply_markup=start_menu())
    await state.finish()

# 🔹 Start menyu
def start_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for cat in CATEGORIES:
        kb.add(KeyboardButton(cat["name"]))
    return kb
