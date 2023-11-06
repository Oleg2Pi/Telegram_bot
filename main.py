import telebot
from config import TOKEN, keys
from extensions import APIException, CryptoConverter


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
    try:
        values = message.text.split(' ')

        if len(values) == 1 and values[0].startswith('/'):
            raise Exception()

        if len(values) != 3:
            raise APIException('Количество параметров не соответствует правильному запросу.')
        
        base, quote, amount = values
        total_quote = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена на {amount} {base} в {quote} составляет {total_quote}'
        bot.send_message(message.chat.id, text)
    
bot.polling(non_stop=True)