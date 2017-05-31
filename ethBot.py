import telegram

bot = telegram.Bot(token='')

print(bot.get_me())

from telegram.ext import Updater

updater = Updater(token='')

dispatcher = updater.dispatcher

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def start(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Let's trade some shit!")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)

import requests

def price(bot,update):
    r = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=ETH')
    priceEUR = r.json()['data']['rates']['EUR']
    priceUSD = r.json()['data']['rates']['USD']
    messageText = "1 ETH = " + priceEUR + "EUR \n" + "1 ETH = " + priceUSD + "USD"
    bot.send_message(chat_id=update.message.chat_id, text = messageText)

price_handler = CommandHandler('price',price)

dispatcher.add_handler(price_handler)

def watch(bot, update ):
    r = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=ETH')
    mainPrice = r.json()['data']['rates']['EUR']
    while(true):
        r = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=ETH')
        newPrice = r.json()['data']['rates']['EUR']
        if(mainPrice - newPrice < - 0.01):
            messageText = "1 ETH = " + newPrice + "EUR" + " going up"
            bot.send_message(chat_id=update.message.chat_id, text = messageText)
        elif(mainPrice - newPrice > 0.01):
            messageText = "1 ETH = " + newPrice + "EUR" + " going down"
            bot.send_message(chat_id=update.message.chat_id, text = messageText)
            time.sleep(5)

watch_handler = CommandHandler('watch',watch)
dispatcher.add_handler(watch_handler)
updater.start_polling()
