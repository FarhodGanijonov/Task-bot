# 📬 Ariza Bot — Ishga tushirish yo'riqnomasi

## 📁 Fayl tuzilmasi
```
telegram_bot/
├── bot.py           # Asosiy bot kodi
├── config.py        # Token va Group ID
├── requirements.txt # Kutubxonalar
└── README.md
```

---

## ⚙️ O'rnatish va ishga tushirish

### 1. Bot token olish
1. Telegramda **@BotFather** ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username'ini kiriting
4. Olingan **tokenni** `config.py` ga joylashtiring:
   ```python
   BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
   ```

### 2. Admin guruh ID olish
1. Guruh yarating yoki mavjud guruhga kiring
2. Botni guruhga **admin** qilib qo'shing
3. Guruh ID'sini bilish uchun:
   - `@userinfobot` botini guruhga qo'shing, u ID'ni ko'rsatadi
   - Yoki: `https://api.telegram.org/bot<TOKEN>/getUpdates` linkini oching
4. ID'ni `config.py` ga joylashtiring (minus bilan):
   ```python
   ADMIN_GROUP_ID = -1001234567890
   ```

### 3. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Botni ishga tushirish
```bash
python bot.py
```

---

## 🤖 Bot qanday ishlaydi

```
Foydalanuvchi /start bosadi
        ↓
❶ Ism so'raladi
        ↓
❷ Telefon raqam so'raladi
        ↓
❸ Yo'nalish tanlanadi (Frontend / Backend / Mobile)
        ↓
❹ Tajriba so'raladi
        ↓
❺ Portfolio/GitHub so'raladi
        ↓
✅ Foydalanuvchiga tasdiqlash xabari
        ↓
📋 Admin guruhga to'liq ariza yuboriladi
```

---

## 📋 Admin guruhga keladigan ariza ko'rinishi

```
📋 Yangi ariza keldi!
━━━━━━━━━━━━━━━━━━━━
👤 Ism: Alisher Karimov
📞 Telefon: +998901234567
💼 Yo'nalish: 🎨 Frontend
🧠 Tajriba: 1 yil, o'z loyihalarim bor
🔗 Portfolio: github.com/alisher
━━━━━━━━━━━━━━━━━━━━
🆔 Telegram: @alisher_dev
🔢 User ID: 123456789
```