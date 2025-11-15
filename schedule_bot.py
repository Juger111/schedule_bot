import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.client.default import DefaultBotProperties

API_TOKEN = "8372235894:AAGQtLLgrhSSfLs-iHQlXKAmkFImt2a2Bck"

# ----- Пример расписания -----
# Здесь админ школы меняет уроки под себя.
SCHEDULE = {
    "Понедельник": [
        {"time": "10:00", "course": "Математика 7А", "teacher": "Иванова"},
        {"time": "12:00", "course": "Английский 6Б", "teacher": "Петров"},
    ],
    "Вторник": [
        {"time": "09:00", "course": "Информатика 8А", "teacher": "Сидоров"},
        {"time": "11:00", "course": "Русский язык 5В", "teacher": "Кузнецова"},
    ],
    "Среда": [],
    "Четверг": [],
    "Пятница": [],
    "Суббота": [],
    "Воскресенье": [],
}

DAYS_ORDER = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]

# ----- Клавиатура -----

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Расписание на сегодня")],
        [KeyboardButton(text="🗓 Все уроки школы")],
        [KeyboardButton(text="ℹ️ Помощь")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)


def format_all_schedule() -> str:
    """Форматирование расписания на всю неделю."""
    lines = ["🗓 *Расписание всех уроков школы*:\n"]
    empty = True

    for day in DAYS_ORDER:
        lessons = SCHEDULE.get(day, [])
        lines.append(f"*{day}*")
        if not lessons:
            lines.append("_Уроков нет._\n")
        else:
            empty = False
            for lesson in lessons:
                lines.append(
                    f"• {lesson['time']} — {lesson['course']} "
                    f"(преподаватель: {lesson['teacher']})"
                )
            lines.append("")  # пустая строка-разделитель

    if empty:
        return "Пока расписание пустое. Администратор ещё не добавил уроки 🤓"

    return "\n".join(lines)


def format_today_schedule() -> str:
    """Форматирование расписания на сегодня."""
    # datetime.weekday(): понедельник = 0, воскресенье = 6
    weekday_idx = datetime.now().weekday()
    day_name = DAYS_ORDER[weekday_idx]

    lessons = SCHEDULE.get(day_name, [])
    if not lessons:
        return (
            f"Сегодня *{day_name.lower()}*, и у вас по школьному расписанию нет уроков. 🎉\n"
            "Можно посвятить день самообразованию или отдыху 😉"
        )

    lines = [f"📅 *Расписание на сегодня ({day_name})*:\n"]
    for lesson in lessons:
        lines.append(
            f"• {lesson['time']} — {lesson['course']} "
            f"(преподаватель: {lesson['teacher']})"
        )

    # Немного «живости»
    lines.append("\nУдачи на занятиях! 💪 Если что — бот всегда под рукой.")
    return "\n".join(lines)


# ----- Хэндлеры -----

async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот онлайн-школы 👋\n\n"
        "Помогу быстро посмотреть расписание занятий.\n"
        "Выберите нужную кнопку ниже:",
        reply_markup=main_kb,
    )


async def cmd_help(message: Message):
    await message.answer(
        "ℹ️ *Как пользоваться ботом:*\n\n"
        "• Нажмите кнопку *«📅 Расписание на сегодня»*, чтобы узнать, какие уроки у вас сегодня.\n"
        "• Нажмите *«🗓 Все уроки школы»*, чтобы увидеть полное расписание на неделю.\n\n"
        "Никаких команд и сложных действий — только кнопки 🙂",
        reply_markup=main_kb,
    )


async def handle_today_schedule(message: Message):
    text = format_today_schedule()
    await message.answer(text)


async def handle_full_schedule(message: Message):
    text = format_all_schedule()
    await message.answer(text)


# ----- Точка входа -----

async def main():
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode="Markdown")  # вот оно, вместо parse_mode=...
    )
    dp = Dispatcher()

    # Команды
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_help, Command(commands={"help"}))

    # Кнопки
    dp.message.register(handle_today_schedule, F.text == "📅 Расписание на сегодня")
    dp.message.register(handle_full_schedule, F.text == "🗓 Все уроки школы")
    dp.message.register(cmd_help, F.text == "ℹ️ Помощь")

    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
