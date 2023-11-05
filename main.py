import telebot
import requests
import json

TOKEN = '6826299493:AAHgy5FvpOaNHMBeMwX621tRiEmD2GpNm8s'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите комманду боту в следующем формате:\n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n\
Чтобы увидеть список доступных валют, введите /values'
    bot.reply_to(message, text)

bot.polling(non_stop=True)