import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8586464933:AAEdcsFFRwu01nRLACfvA4cW3V6cYiFbAVA"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="➕ Добавить в группу",
                url=f"https://t.me/{context.bot.username}?startgroup=true"
            )
        ]
    ])

    await update.message.reply_text(
        "Я — калькулятор бот 🤖\n"
        "Напиши пример снизу, и я решу его.\n\n"
        "Пример: 2+2*5",
        reply_markup=keyboard
    )


# обработка примеров
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace(" ", "")

    # разрешаем только цифры и операторы
    if not re.fullmatch(r"[0-9+\-*/().]+", text):
        return

    try:
        result = eval(text)
        await update.message.reply_text(f"Ответ: {result}")
    except Exception:
        await update.message.reply_text("Ошибка в примере ❌")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calc))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
