from model import ClassPredictor
from telegram_token import token
import torch
from config import reply_texts, classes
import numpy as np
from PIL import Image
from io import BytesIO


model = ClassPredictor()

REQUEST_KWARGS={
    'proxy_url': 'socks4://23.252.66.25:54321',
    # Optional, if you need authentication:
    #'username': 'PROXY_USER',
    #'password': 'PROXY_PASS',
}


def send_prediction_on_photo(bot, update):
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
    image_stream = BytesIO()
    image_file.download(out=image_stream)

    class_ = model.predict(image_stream)

    # теперь отправим результат
    update.message.reply_text("Я думаю это: {}".format(classes[str(class_)]))
    print ("Sent Answer to user, predicted: {}".format(class_))

def start(bot, update):
    chat_id = update.message.chat_id
    print("Use /start {}".format(chat_id))
    
    update.message.reply_text(reply_texts['start_message'])
    update.message.reply_text(reply_texts['start_message_2'])
    update.message.reply_text(reply_texts['start_message_3'])
    
def dogs(bot, update):
    chat_id = update.message.chat_id
    print("Use /dogs {}".format(chat_id))

    update.message.reply_text(reply_texts['dogs_1'])
    update.message.reply_text(reply_texts['dogs_2'])
    update.message.reply_text(reply_texts['dogs_3'])

  
    

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests
import re
import logging

def main():
  logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
    # используем прокси, так как без него у меня ничего не работало(
  
    
  updater = Updater(token=token, request_kwargs=REQUEST_KWARGS)
  updater.dispatcher.add_handler(MessageHandler(Filters.photo, send_prediction_on_photo))
  updater.dispatcher.add_handler(CommandHandler('start', start))
  updater.dispatcher.add_handler(CommandHandler('dogs', dogs))
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
    main()


