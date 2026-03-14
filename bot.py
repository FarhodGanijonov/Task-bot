import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from config import BOT_TOKEN, ADMIN_GROUP_ID, PROXY_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else None
bot = Bot(token=BOT_TOKEN, session=session) if session else Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class ApplicationForm(StatesGroup):
    name = State()
    phone = State()
    direction = State()
    experience = State()
    portfolio = State()


def direction_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎨 Frontend")],
            [KeyboardButton(text="⚙️ Backend")],
            [KeyboardButton(text="📱 Mobile")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 <b>Telegram botiga xush kelibsiz!</b>\n\n"
        "Ariza topshirish uchun bir necha savolga javob bering.\n\n"
        "❶ Ismingizni kiriting:",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(ApplicationForm.name)


@dp.message(ApplicationForm.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("⚠️ Iltimos, to'liq ismingizni kiriting:")
        return
    await state.update_data(name=name)
    await message.answer("❷ Telefon raqamingiz: (masalan: +998901234567)")
    await state.set_state(ApplicationForm.phone)


@dp.message(ApplicationForm.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if len(phone) < 9:
        await message.answer("⚠️ Telefon raqamni to'g'ri kiriting:")
        return
    await state.update_data(phone=phone)
    await message.answer(
        "❸ Qaysi yo'nalish?\n\nQuyidagilardan birini tanlang:",
        reply_markup=direction_keyboard(),
    )
    await state.set_state(ApplicationForm.direction)


VALID_DIRECTIONS = {"🎨 Frontend", "⚙️ Backend", "📱 Mobile"}

@dp.message(ApplicationForm.direction)
async def process_direction(message: Message, state: FSMContext):
    direction = message.text.strip()
    if direction not in VALID_DIRECTIONS:
        await message.answer(
            "⚠️ Iltimos, quyidagi tugmalardan birini tanlang:",
            reply_markup=direction_keyboard(),
        )
        return
    await state.update_data(direction=direction)
    await message.answer(
        "❹ Tajribangiz haqida qisqacha yozing:\n(masalan: 2 yil, Junior, bootcamp bitiruvchisi...)",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(ApplicationForm.experience)


@dp.message(ApplicationForm.experience)
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text.strip())
    await message.answer(
        "❺ Portfolio yoki GitHub havolangiz:\n(yo'q bo'lsa — <b>yo'q</b> deb yozing)",
        parse_mode="HTML",
    )
    await state.set_state(ApplicationForm.portfolio)


@dp.message(ApplicationForm.portfolio)
async def process_portfolio(message: Message, state: FSMContext):
    await state.update_data(portfolio=message.text.strip())
    data = await state.get_data()

    await message.answer(
        "✅ <b>Arizangiz qabul qilindi!</b>\n\n"
        "Tez orada siz bilan bog'lanamiz. Rahmat! 🙏",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )

    user = message.from_user
    admin_text = (
        "📋 <b>Yangi ariza keldi!</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Ism:</b> {data['name']}\n"
        f"📞 <b>Telefon:</b> {data['phone']}\n"
        f"💼 <b>Yo'nalish:</b> {data['direction']}\n"
        f"🧠 <b>Tajriba:</b> {data['experience']}\n"
        f"🔗 <b>Portfolio:</b> {data['portfolio']}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 Telegram: @{user.username or 'username yoq'}\n"
        f"🔢 User ID: <code>{user.id}</code>"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=admin_text,
            parse_mode="HTML",
        )
    except Exception as e:
        logger.error(f"Admin guruhga yuborishda xato: {e}")

    await state.clear()


@dp.message()
async def unknown_message(message: Message):
    await message.answer(
        "❓ Botni ishlatish uchun /start buyrug'ini bosing."
    )


async def main():
    logger.info("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())