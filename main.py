import telebot
import requests
import json

TOKEN = '6826299493:AAHgy5FvpOaNHMBeMwX621tRiEmD2GpNm8s'

keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB'
}

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите комманду боту в следующем формате:\n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n\
Чтобы увидеть список доступных валют, введите /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    base, quote, amount = values

    response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
    total_quote = json.loads(response.content)[keys[quote]] * float(amount)
    text = f'Цена на {amount} {base} в {quote} составляет {total_quote}'
    bot.send_message(message.chat.id, text)

bot.polling(non_stop=True)