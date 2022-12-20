import telebot
from telebot import types
from helpers.filters import currency_first_factory, currency_second_factory, currency_value_factory
CURRENCIES = [
    {'id': '0', 'name': 'USD'},
    {'id': '1', 'name': 'RUB'},
    {'id': '2', 'name': 'KZT'}
]


def currency_keyboard():
    return telebot.types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=currency['name'],
                    callback_data=currency_first_factory.new(currency_id=currency['id'])
                )
            ]
            for currency in CURRENCIES
        ]
    )


def second_currency_keyboard(first):
    return telebot.types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=currency['name'],
                    callback_data=currency_second_factory.new(currency_id=currency['id'], first=first)
                )
            ]
            for currency in CURRENCIES
        ]
    )


def value_currency_keyboard(first, second):
    return telebot.types.InlineKeyboardMarkup(
        keyboard=[
            types.InlineKeyboardButton(
                text='Посчитать',
                callback_data=currency_value_factory.new()
            )
        ]
    )