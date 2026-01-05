import asyncio
import ast
import operator
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def eval_expr(expr):
    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            return OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError
    return _eval(ast.parse(expr, mode="eval").body)

async def handler(update: Update, context):
    try:
        res = eval_expr(update.message.text.replace(" ", ""))
        await update.message.reply_text(str(res))
    except:
        pass

async def main():
    app = Application.builder().token("8586464933:AAEdcsFFRwu01nRLACfvA4cW3V6cYiFbAVA").build()
    app.add_handler(MessageHandler(filters.TEXT, handler))

    await app.initialize()
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
