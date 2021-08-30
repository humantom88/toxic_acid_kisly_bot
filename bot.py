# -- coding: utf-8 -
# t.me/ToxicAcidKislyBot

# !pip install python-telegram-bot --upgrade
from env import TELEGRAM_TOKEN
from telegram import Update
from telegram.ext  import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pickle
from utils import Analyzer

updater = Updater(token=TELEGRAM_TOKEN, use_context=True) # Токен API к Telegram
dispatcher = updater.dispatcher

with open('./analyzer.pkl', 'rb') as f:
    analyzer = pickle.load(f)

# Обработка команд
def start(update, context):
    update.message.reply_text("Привет!")

def echo(update: Update, context: CallbackContext):
    txt = update.message.text
    result = analyzer.answer_message(txt)
    update.message.reply_text(result)    

# on different commands - answer in Telegram
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Start the Bot
print('Successfully started')
updater.start_polling()
updater.idle()