import telebot
from config import keys, TOKEN
from extensions import ConvertionException, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hlp(message: telebot.types.Message):
    text = 'Привет! Я Бот-Конвертер валют и я могу:\
    \n- Показать список доступных валют через команду /values\
    \n- Вывести конвертацию валюты через команду:\n\
    <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\
    \n- Напомнить, что я могу через команду:\n/help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def hlp(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате:\
    \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\
    \nУвидеть список всех доступных валют, через команду:\n/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        quote = quote.lower()
        base = base.lower()
        total_base = float(APIException.get_price(quote, base, amount))
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {round(total_base, 4)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()


