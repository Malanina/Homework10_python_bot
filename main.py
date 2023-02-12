import random
import time
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters)
from commands_bot import *



handler = ConversationHandler(
    entry_points=[CommandHandler("start", sweets_game)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, after_move)],
    },
    fallbacks=[CommandHandler("end", end)]
)


app = ApplicationBuilder().token('YOUR TOKEN HERE').build()


app.add_handler(handler)

print('server start')

app.run_polling()