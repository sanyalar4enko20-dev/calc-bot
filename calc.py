import asyncio
import re
from aiogram import Bot, Dispatcher, types

TOKEN = "8586464933:AAEdcsFFRwu01nRLACfvA4cW3V6cYiFbAVA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Регулярка: 2+2, 10*5, -3-7, 8/2
EXPR_RE = re.compile(r"^\s*(-?\d+)\s*([+\-*/])\s*(-?\d+)\s*$")


@dp.message()
async def calculator(message: types.Message):
    if not message.text:
        return

    text = message.text.strip()
    match = EXPR_RE.match(text)

    if not match:
        return  # не пример — молчим

    a, op, b = match.groups()
    a = int(a)
    b = int(b)

    try:
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                await message.reply("❌ Делить на ноль нельзя")
                return
            result = a / b
    except Exception:
        return

    await message.reply(f"🧮 <b>{a} {op} {b} = {result}</b>", parse_mode="HTML")


async def main():
    print("Калькулятор-бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())