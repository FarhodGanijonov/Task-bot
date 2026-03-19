# 📋 Ariza Qabul Qiluvchi Telegram Bot

## 🚀 O'rnatish va Ishga Tushirish

### 1. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 2. Bot tokenini olish
1. Telegramda [@BotFather](https://t.me/BotFather) ga boring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting
4. Token oling — uni `bot.py` faylida `BOT_TOKEN` ga kiriting

### 3. Admin ID ni olish
1. Telegramda [@userinfobot](https://t.me/userinfobot) ga boring
2. U sizning Telegram ID ingizni ko'rsatadi
3. Uni `bot.py` faylida `ADMIN_CHAT_ID` ga kiriting

### 4. bot.py faylini tahrirlash
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"   # ← o'zgartiring
ADMIN_CHAT_ID = 123456789           # ← o'zgartiring
```

### 5. Bino rasmini qo'shish (ixtiyoriy)
- `building.jpg` nomli rasmni `bot.py` bilan bir papkaga qo'ying
- Yoki `bot.py` da `BUILDING_PHOTO_PATH` ni o'zgartiring

### 6. Botni ishga tushirish
```bash
python bot.py
```

---

## 📌 Bot Ishlash Tartibi

| № | Savol | Tur |
|---|-------|-----|
| 1 | FIO (Familiya Ism Sharif) | Matn |
| 2 | Tug'ilgan sana (18.03.1995) | Matn (format tekshiriladi) |
| 3 | Telefon (+998XXXXXXXXX) | Matn (format tekshiriladi) |
| 4 | Jins | Tugma: Erkak / Ayol |
| 5 | Talabami? | Tugma: Ha / Yo'q |
| 6 | O'qish shakli (faqat Ha desa) | Tugma: Kunduzgi / Kechgi / Sirtqi |
| 7 | Ish tajriba | Matn yoki O'tkazib yuborish |
| 8 | Rasm (selfi) | Foto |
| 9 | Tasdiqlash | Tugma: Tasdiqlash / Bekor qilish |

---

## 📤 Oxirida nima yuboriladi?

**Foydalanuvchiga:**
- ✅ Suhbat vaqti va manzil haqida xabar
- 📍 Joylashuv (location)
- 🏢 Bino rasmi + matn

**Adminga:**
- 📸 Ariza egasining rasmi + barcha ma'lumotlar

---

## ⚙️ Sozlamalar (bot.py ichida)

```python
BOT_TOKEN = "..."          # Bot token
ADMIN_CHAT_ID = ...        # Admin Telegram ID
LOCATION_LATITUDE = 41.2995    # Manzil koordinatasi
LOCATION_LONGITUDE = 69.2401   # Manzil koordinatasi
BUILDING_PHOTO_PATH = "building.jpg"  # Bino rasmi yo'li
```

---

## 🛑 Botni to'xtatish
`Ctrl + C` bosing

## ❌ Bekor qilish
Foydalanuvchi istalgan payt `/cancel` buyrug'ini yuborib jarayonni bekor qila oladi.