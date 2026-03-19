import logging
import os
from dotenv import load_dotenv
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

# ==================== SOZLAMALAR ====================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_IDS = [int(x.strip()) for x in os.getenv("ADMIN_CHAT_IDS", os.getenv("ADMIN_CHAT_ID", "0")).split(",")]
LOCATION_LATITUDE = float(os.getenv("LOCATION_LATITUDE", "41.2995"))
LOCATION_LONGITUDE = float(os.getenv("LOCATION_LONGITUDE", "69.2401"))
BUILDING_PHOTO_PATH = os.getenv("BUILDING_PHOTO_PATH", "building.jpg")

# ==================== ARIZA RAQAMI ====================
COUNTER_FILE = "ariza_counter.txt"

def get_next_ariza_number():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            num = int(f.read().strip() or "0")
    else:
        num = 0
    num += 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(num))
    return num

# ==================== LOGLAR ====================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== BOSQICHLAR ====================
(
    FIO, TUGILGAN_SANA, TELEFON, JINS,
    TALABA, OQUV_SHAKL, ISH_TAJRIBA, RASM,
    TASDIQLASH
) = range(9)


# ==================== START ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "Ushbu bot orqali ariza topshirishingiz mumkin.\n"
        "Boshlash uchun quyidagi savolga javob bering:\n\n"
        "📝 *1. Pasportdagi Familiya, Ism va Sharifingizni kiriting:*\n"
        "_Misol: Karimov Jasur Aliyevich_",
        parse_mode="Markdown"
    )
    context.user_data["ariza_raqam"] = get_next_ariza_number()
    return FIO


# ==================== 1. FIO ====================
async def get_fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if len(text) < 5:
        await update.message.reply_text("❌ Iltimos, to'liq FIO kiriting.")
        return FIO
    context.user_data["fio"] = text
    await update.message.reply_text(
        "✅ Qabul qilindi!\n\n"
        "📅 *2. Tug'ilgan sanangizni kiriting:*\n"
        "_Misol: 18.03.1995_",
        parse_mode="Markdown"
    )
    return TUGILGAN_SANA


# ==================== 2. TUG'ILGAN SANA ====================
async def get_tugilgan_sana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    import re
    if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", text):
        await update.message.reply_text(
            "❌ Format noto'g'ri. Iltimos, quyidagi formatda kiriting:\n_Misol: 18.03.1995_",
            parse_mode="Markdown"
        )
        return TUGILGAN_SANA
    context.user_data["tugilgan_sana"] = text
    await update.message.reply_text(
        "✅ Qabul qilindi!\n\n"
        "📞 *3. Telefon raqamingizni kiriting:*\n"
        "_Misol: +998931234567_",
        parse_mode="Markdown"
    )
    return TELEFON


# ==================== 3. TELEFON ====================
async def get_telefon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    import re
    if not re.match(r"^\+998\d{9}$", text):
        await update.message.reply_text(
            "❌ Format noto'g'ri. Iltimos quyidagi formatda kiriting:\n_Misol: +998931234567_",
            parse_mode="Markdown"
        )
        return TELEFON
    context.user_data["telefon"] = text

    keyboard = ReplyKeyboardMarkup(
        [["👨 Erkak", "👩 Ayol"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        "✅ Qabul qilindi!\n\n"
        "👤 *4. Jinsni tanlang:*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    return JINS


# ==================== 4. JINS ====================
async def get_jins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text not in ["👨 Erkak", "👩 Ayol"]:
        await update.message.reply_text("❌ Iltimos, tugmalardan birini tanlang.")
        return JINS
    context.user_data["jins"] = text

    keyboard = ReplyKeyboardMarkup(
        [["✅ Ha", "❌ Yo'q"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        "✅ Qabul qilindi!\n\n"
        "🎓 *5. Siz talabamisiz?*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    return TALABA


# ==================== 5. TALABA ====================
async def get_talaba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text not in ["✅ Ha", "❌ Yo'q"]:
        await update.message.reply_text("❌ Iltimos, tugmalardan birini tanlang.")
        return TALABA
    context.user_data["talaba"] = text

    if text == "✅ Ha":
        keyboard = ReplyKeyboardMarkup(
            [["🌅 Kunduzgi", "🌆 Kechgi", "📚 Sirtqi"]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await update.message.reply_text(
            "✅ Qabul qilindi!\n\n"
            "📖 *6. O'qish shaklini belgilang:*",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        return OQUV_SHAKL
    else:
        context.user_data["oquv_shakl"] = "—"
        await ask_ish_tajriba(update, context)
        return ISH_TAJRIBA


async def ask_ish_tajriba(update, context):
    keyboard = ReplyKeyboardMarkup(
        [["⏭ O'tkazib yuborish"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        "✅ Qabul qilindi!\n\n"
        "💼 *7. Ish tajribangiz qanday?*\n"
        "_Ishlagan vaqtingizni ko'rsating._\n"
        "_Misol: MCHJ \"Zo'r ish\", kassir, 2015-2018_\n\n"
        "Agar ish tajribangiz bo'lmasa ⏭ *O'tkazib yuborish* tugmasini bosing.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# ==================== 6. O'QUV SHAKL ====================
async def get_oquv_shakl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text not in ["🌅 Kunduzgi", "🌆 Kechgi", "📚 Sirtqi"]:
        await update.message.reply_text("❌ Iltimos, tugmalardan birini tanlang.")
        return OQUV_SHAKL
    context.user_data["oquv_shakl"] = text
    await ask_ish_tajriba(update, context)
    return ISH_TAJRIBA


# ==================== 7. ISH TAJRIBA ====================
async def get_ish_tajriba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "⏭ O'tkazib yuborish":
        context.user_data["ish_tajriba"] = "Ko'rsatilmagan"
    else:
        context.user_data["ish_tajriba"] = text

    await update.message.reply_text(
        "✅ Qabul qilindi!\n\n"
        "📸 *8. Rasmingizni yuboring*\n"
        "_Selfi ham mumkin!_",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    return RASM


# ==================== 8. RASM ====================
async def get_rasm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Iltimos, rasm yuboring (foto shaklida).\n_Selfi ham mumkin!_",
            parse_mode="Markdown"
        )
        return RASM

    photo = update.message.photo[-1]
    context.user_data["rasm_file_id"] = photo.file_id

    # Arizani tasdiqlash sahifasi
    await show_summary(update, context)
    return TASDIQLASH


async def show_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = context.user_data
    summary = (
        f"📋 *Arizangizni tekshiring* | #{d.get('ariza_raqam', '?')}:\n\n"
        f"👤 *FIO:* {d.get('fio', '—')}\n"
        f"📅 *Tug'ilgan sana:* {d.get('tugilgan_sana', '—')}\n"
        f"📞 *Telefon:* {d.get('telefon', '—')}\n"
        f"👤 *Jins:* {d.get('jins', '—')}\n"
        f"🎓 *Talaba:* {d.get('talaba', '—')}\n"
        f"📖 *O'qish shakli:* {d.get('oquv_shakl', '—')}\n"
        f"💼 *Ish tajriba:* {d.get('ish_tajriba', '—')}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🗓 *Suhbat vaqti:*\n"
        "Bugun va ertaga 🕐 11:00 da\n"
        "_(Yakshanba kuni bo'lmaydi)_\n\n"
        "📍 *Manzil:*\n"
        "Toshkent shahar, Uchtepa tumani,\n"
        "Beshqayrog'och 170-uy\n\n"
        "✅ Tasdiqlaysizmi?"
    )

    keyboard = ReplyKeyboardMarkup(
        [["✅ Tasdiqlash", "❌ Bekor qilish"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(summary, reply_markup=keyboard, parse_mode="Markdown")


# ==================== 9. TASDIQLASH ====================
async def get_tasdiqlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "❌ Bekor qilish":
        await update.message.reply_text(
            "❌ Ariza bekor qilindi.\n/start buyrug'i bilan qaytadan boshlashingiz mumkin.",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data.clear()
        return ConversationHandler.END

    if text != "✅ Tasdiqlash":
        await update.message.reply_text("❌ Iltimos, tugmalardan birini tanlang.")
        return TASDIQLASH

    # Foydalanuvchiga manzil, rasm va xabar yuborish
    await send_final_info(update, context)

    # Adminga yuborish
    await send_to_admin(update, context)

    await update.message.reply_text(
        "🎉 *Arizangiz muvaffaqiyatli qabul qilindi!*\n\n"
        "Tez orada siz bilan bog'lanamiz.\n"
        "Rahmat! 🙏",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    context.user_data.clear()
    return ConversationHandler.END


async def send_final_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchiga oxirgi ma'lumotlarni yuborish"""
    chat_id = update.effective_chat.id

    # Suhbat va manzil haqida xabar
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "📌 *Muhim ma'lumotlar:*\n\n"
            "🗓 *Suhbat vaqti:*\n"
            "Bugun va ertaga 🕐 11:00 da\n"
            "_(Yakshanba kuni bo'lmaydi)_\n\n"
            "📍 *Manzilimiz:*\n"
            "Toshkent shahar, Uchtepa tumani,\n"
            "Beshqayrog'och 170-uy"
        ),
        parse_mode="Markdown"
    )

    # Joylashuv yuborish
    await context.bot.send_location(
        chat_id=chat_id,
        latitude=LOCATION_LATITUDE,
        longitude=LOCATION_LONGITUDE
    )

    # Bino rasmi yuborish (agar mavjud bo'lsa)
    if os.path.exists(BUILDING_PHOTO_PATH):
        with open(BUILDING_PHOTO_PATH, "rb") as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=("🏢 Manzilimiz: Toshkent shahar, Uchtepa tumani, Beshqayrog'och 170-uy\n\n⚠️ Shu bino — mabodo telefonga javob bera olmasak yoki Telegramga javob bera olmay qolsak, to'g'ri o'ng eshigidan kirib: \"Suhbatga keldim\" deb aytaverasiz!")
            )


async def send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adminga arizani yuborish"""
    d = context.user_data
    user = update.effective_user

    fio = d.get("fio", "—")
    tug_sana = d.get("tugilgan_sana", "—")
    telefon = d.get("telefon", "—")
    jins = d.get("jins", "—")
    talaba = d.get("talaba", "—")
    oquv = d.get("oquv_shakl", "—")
    tajriba = d.get("ish_tajriba", "—")
    username = user.username or "yoq"

    ariza_raqam = d.get("ariza_raqam", "?")
    admin_text = (
        f"🔔 YANGI ARIZA KELDI! | #{ariza_raqam}\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 FIO: {fio}\n"
        f"📅 Tugilgan sana: {tug_sana}\n"
        f"📞 Telefon: {telefon}\n"
        f"👤 Jins: {jins}\n"
        f"🎓 Talaba: {talaba}\n"
        f"📖 Oquv shakli: {oquv}\n"
        f"💼 Ish tajriba: {tajriba}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🆔 Telegram ID: {user.id}\n"
        f"👤 Username: @{username}\n"
        f"📛 Telegram ismi: {user.full_name}"
    )

    # Barcha adminlarga rasm bilan yuborish
    for admin_id in ADMIN_CHAT_IDS:
        await context.bot.send_photo(
            chat_id=admin_id,
            photo=d.get("rasm_file_id"),
            caption=admin_text
        )


# ==================== BEKOR QILISH ====================
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Jarayon bekor qilindi.\n/start bilan qaytadan boshlashingiz mumkin.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# ==================== ASOSIY ====================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fio)],
            TUGILGAN_SANA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tugilgan_sana)],
            TELEFON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_telefon)],
            JINS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_jins)],
            TALABA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_talaba)],
            OQUV_SHAKL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_oquv_shakl)],
            ISH_TAJRIBA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ish_tajriba)],
            RASM: [MessageHandler(filters.PHOTO, get_rasm)],
            TASDIQLASH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tasdiqlash)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("✅ Bot ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()