import telegram as tele
from telegram.ext import Updater
from telegram.ext import CommandHandler as cmdHandler
import logging
from telegram.ext import MessageHandler, Filters
import urllib.request
from pathlib import Path
import csv
import os
import sqlite3


def start(update, context):
    print(update.message)
    # start_conn.execute(f'''INSERT INTO USER (FIRST_NAME, LAST_NAME, USER_NAME, CHAT_ID)
    #     VALUES ({str(update.effective_chat.first_name)}, {str(update.effective_chat.last_name)},
    #             {str(update.effective_chat.username)}, {str(update.effective_chat.id)}, NULL );''')
    try:
        start_conn = sqlite3.connect("user.db")
        start_conn.execute(f"INSERT INTO USER (FIRST_NAME, LAST_NAME, USER_NAME, CHAT_ID, STUDENT_NUMBER) "
                           f"VALUES ('{str(update.effective_chat.first_name)}', "
                           f"'{str(update.effective_chat.last_name)}', "
                           f"'{str(update.effective_chat.username)}', "
                           f"'{str(update.effective_chat.id)}', 'NULL' )")
        start_conn.commit()
        start_conn.close()
        context.bot.send_message(chat_id=update.effective_chat.id, text="به بات درس برنامه سازی پیشرفته خوش آمدید")
    except ValueError:
        print(ValueError)


def echoImage(update, context):
    print(update.message)
    # context.bot.send_photo(chat_id=update.effective_chat.id, photo=update.message.photo[1])
    file = bot.getFile(update.message.photo[1].file_id)
    passvnad = file.file_path.split('.')[len(file.file_path.split('.')) - 1]
    Path(FILE_PATH + '/' + str(update.effective_chat.first_name) +
         str(update.effective_chat.last_name)).mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(file.file_path, FILE_PATH + '/' + str(update.effective_chat.first_name) +
         str(update.effective_chat.last_name) + '/' + file.file_unique_id + '.' + passvnad)
    context.bot.send_message(chat_id=update.effective_chat.id, text="عکس ارسالی ذخیره شد")


def handleTextMessage(update, context):
    print(update)
    with open('comment/comments.csv', mode='a', encoding="utf-8", newline='') as first_csv_file:
        inner_writer = csv.writer(first_csv_file)
        message_text = str(update.message.text)
        inner_writer.writerow([str(update.effective_chat.first_name),
                               str(update.effective_chat.last_name),
                               str(update.effective_chat.username),
                               message_text])
    first_csv_file.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text="پیام شما ذخیره شد با تشکر از شما")


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def helpHandler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="شما در بات درس برنامه سازی پیشرفته ثبت نام شده اید برای ارسال شماره دانشجویی و یا ویرایش آن از دستور \n /studentnum  شماره  دانشجویی \n استفاده کنید")


def otherCalback(update, context):
    print(update.message)
    Path(FILE_PATH + '/' + str(update.effective_chat.first_name) +
         str(update.effective_chat.last_name)).mkdir(parents=True, exist_ok=True)
    file = tele.PassportFile.get_file(bot.getFile(update.message.document.file_id)) \
        .download(FILE_PATH + '/' + str(update.effective_chat.first_name) +
         str(update.effective_chat.last_name) + '/' + str(update.message.document.file_name))
    context.bot.send_message(chat_id=update.effective_chat.id, text="فایل ارسالی ذخیره شد")


def handleStudentNumberCallBack(update, context):
    if len(context.args) > 0:
        number = context.args[0]
        student_conn = sqlite3.connect("user.db")
        student_conn.execute(
            f"UPDATE USER SET STUDENT_NUMBER = '{number}' where CHAT_ID = '{update.effective_chat.id}'")
        student_conn.commit()
        student_conn.close()
        context.bot.send_message(chat_id=update.effective_chat.id, text="شماره دانشجویی شما ذخیره شد")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="ورودی نا معتبر است")


TOKEN = '1250087938:AAHzRycLJu1G2QUTE7O6a_bGfFDhFkswFsc'
FILE_PATH = "files"

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

start_handler = cmdHandler('start', start)
dispatcher.add_handler(start_handler)
caps_handler = cmdHandler('caps', caps)
dispatcher.add_handler(caps_handler)
help_handler = cmdHandler('help', helpHandler)
dispatcher.add_handler(help_handler)
student_number_handler = cmdHandler('studentnum', handleStudentNumberCallBack)
dispatcher.add_handler(student_number_handler)
echoImage_handler = MessageHandler(Filters.photo & (~Filters.command), echoImage)
dispatcher.add_handler(echoImage_handler)
otherFile_handler = MessageHandler(Filters.document, otherCalback)
dispatcher.add_handler(otherFile_handler)
echoText_handler = MessageHandler(Filters.text, handleTextMessage)
dispatcher.add_handler(echoText_handler)
updater.start_polling()

# CSV file created if not exist
if not os.path.isfile('comment/comments.csv'):
    print("Create CSV")
    Path("comment").mkdir(parents=True, exist_ok=True)
    with open('comment/comments.csv', mode='w', newline='') as csv_file:
        fieldnames = ['First_Name', 'Last_Name', 'User_Name', 'Message']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    csv_file.close()

bot = tele.Bot(token=TOKEN)

# Create data base
conn = sqlite3.connect("user.db")
conn.execute('''CREATE TABLE IF NOT EXISTS  USER 
         (ID INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
         FIRST_NAME           TEXT  ,
         LAST_NAME            TEXT    ,
         USER_NAME        TEXT,
         CHAT_ID         TEXT unique , 
         STUDENT_NUMBER   TEXT NULLABLE );''')
conn.close()
