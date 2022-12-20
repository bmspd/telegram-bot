import os
from dotenv import load_dotenv
import requests
import telebot
from helpers.currency import currency_keyboard, CURRENCIES, second_currency_keyboard
from helpers.filters import currency_first_factory, bind_filters, currency_second_factory

store = {
    'users': {}
}

if __name__ == '__main__':
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        bot.reply_to(message, "Hello, I am bot!")

    @bot.message_handler(commands=['converter'])
    def start_conversion(message):
        text = 'Выберите вашу валюту'
        markup = currency_keyboard()
        sent_msg = bot.send_message(message.chat.id, text=text, reply_markup=markup)


    @bot.callback_query_handler(func=None, currency_first_config=currency_first_factory.filter())
    def currency_callback(call: telebot.types.CallbackQuery):
        callback_data: dict = currency_first_factory.parse(callback_data=call.data)
        currency_id = int(callback_data.get('currency_id'))
        first_currency = CURRENCIES[currency_id]['name']
        text = 'Выберите в какую валюту конвертировать'
        markup = second_currency_keyboard(first=first_currency)
        bot.send_message(call.message.chat.id, text=text, reply_markup=markup)

    @bot.callback_query_handler(func=None, currency_second_config=currency_second_factory.filter())
    def second_currency_callback(call: telebot.types.CallbackQuery):
        callback_data: dict = currency_second_factory.parse(callback_data=call.data)
        text = 'Введите число для подсчета'
        bot.send_message(call.message.chat.id, text=text)
        currency_id = int(callback_data.get('currency_id'))
        second_currency = CURRENCIES[currency_id]['name']
        formatted_data = {'first': callback_data['first'], 'second': second_currency}
        bot.register_next_step_handler(call.message, conversion, formatted_data)

    def conversion(message, formatted_data):
        url = f"https://api.exchangerate.host/convert?" \
              f"from={formatted_data['first']}" \
              f"&to={formatted_data['second']}" \
              f"&amount={message.text}"
        response = requests.get(url)
        data: dict = response.json()
        bot.send_message(message.chat.id, text=data.get('result'))


    @bot.message_handler(func=lambda msg: True)
    def echo_all(message):
        bot.reply_to(message, message.text)

    bind_filters(bot)
    bot.infinity_polling()
