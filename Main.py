import telegram as tele
from telegram.ext import Updater
from telegram.ext import CommandHandler as cmdHandler
import logging
from telegram.ext import MessageHandler, Filters
import urllib.request
from pathlib import Path


def start(update, context):
    print(update.message)
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echoImage(update, context):
    print(update.message)
    context.bot.send_message(chat_id=update.effective_chat.id, text="File saved")
    # context.bot.send_photo(chat_id=update.effective_chat.id, photo=update.message.photo[1])
    file = bot.getFile(update.message.photo[1].file_id)
    passvnad = file.file_path.split('.')[len(file.file_path.split('.')) - 1]
    Path(FILE_PATH + '/' + str(update.effective_chat.username)).mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(file.file_path, FILE_PATH + '/' + str(update.effective_chat.username)
                               + '/' + file.file_unique_id + '.' + passvnad)


def echoText(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def otherCalback(update, context):
    print(update.message)
    Path(FILE_PATH + '/' + str(update.effective_chat.username)).mkdir(parents=True, exist_ok=True)
    file = tele.PassportFile.get_file(bot.getFile(update.message.document.file_id))\
        .download(FILE_PATH + '/' + str(update.effective_chat.username) + '/' + update.message.document.file_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text="File saved")


TOKEN = '1250087938:AAHzRycLJu1G2QUTE7O6a_bGfFDhFkswFsc'
FILE_PATH = "files"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

start_handler = cmdHandler('start', start)
dispatcher.add_handler(start_handler)
echoImage_handler = MessageHandler(Filters.photo & (~Filters.command), echoImage)
dispatcher.add_handler(echoImage_handler)
echoText_handler = MessageHandler(Filters.text, echoText)
dispatcher.add_handler(echoText_handler)
otherFile_handler = MessageHandler(Filters.document, otherCalback)
dispatcher.add_handler(otherFile_handler)

caps_handler = cmdHandler('caps', caps)
dispatcher.add_handler(caps_handler)

updater.start_polling()

bot = tele.Bot(token=TOKEN)
botMe = bot.get_me()
