from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import datetime, requests, datetime
from bs4 import BeautifulSoup


reply_keyboard = [['/info', '/today']]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
TOKEN = open("res/token.txt").read()


def start(update, context):
    update.message.reply_text(
        "Привет! Я — бот, который сообщает о праздниках и событиях, произошедших сегодня", reply_markup=markup)


def info(update, context):
    update.message.reply_text("Используйте команду /today, чтобы увидеь праздники, которые отмечают сегодня")


def today(update, context):
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    months = ["января", "февраля",  "марта",  "апреля",  "мая",  "июня",  "июля",  "августа",  "сентября",  "октяюря",  "ноября",  "декабря"]
    URL = f'https://ru.wikipedia.org/wiki/Категория:Праздники_{day}_{months[month - 1]}'
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")
    total = []

    for tag in soup.find_all("li"):
        if "Праздники " in tag.text:
            break
        total.append("— " + tag.text)

    update.message.reply_text("\n".join(total))


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("today", today))
    
    updater.start_polling()
    updater.idle()
    

if __name__ == '__main__':
    main()
