from telegram.ext import ApplicationBuilder, Application, MessageHandler, CommandHandler, filters

def respond(update, context):
    text = update.message.text

tg_msg_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, respond) # type: ignore

