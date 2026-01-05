import ast
import operator
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def safe_eval(expr: str):
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            return OPERATORS[type(node.op)](
                _eval(node.left),
                _eval(node.right)
            )
        if isinstance(node, ast.UnaryOp):
            return OPERATORS[type(node.op)](
                _eval(node.operand)
            )
        raise ValueError("bad expr")

    return _eval(ast.parse(expr, mode="eval").body)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace(" ", "")
    try:
        result = safe_eval(text)
        await update.message.reply_text(f"= {result}")
    except Exception:
        pass

async def main():
    app = (
        ApplicationBuilder()
        .token("8586464933:AAEdcsFFRwu01nRLACfvA4cW3V6cYiFbAVA")
        .build()
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    await app.initialize()
    await app.start()
    await app.bot.initialize()
    await app.stop()  # Render требует, чтобы процесс жил
    await asyncio.Event().wait()  # держим процесс навсегда

if __name__ == "__main__":
    asyncio.run(main())
