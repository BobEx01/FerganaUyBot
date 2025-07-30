from aiogram.dispatcher.filters.state import State, StatesGroup

class AdState(StatesGroup):
    category = State()            # 1. Kategoriya tanlash (kvartira, uchastka, yer)
    location = State()            # 2. Joylashuv
    price = State()               # 3. Narx
    size = State()                # 4. Maydon (kv.m yoki sotix)
    amenities = State()           # 5. Qo‘shimcha qulayliklar
    communication = State()       # 6. Komunikatsiyalar (gaz, suv, svet)
    description = State()         # 7. Matnli tavsif
    photos = State()              # 8. Rasmlar
    confirm = State()             # 9. Tasdiqlash
