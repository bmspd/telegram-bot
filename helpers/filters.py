import telebot
from telebot import AdvancedCustomFilter
from telebot.callback_data import CallbackData

currency_first_factory = CallbackData('currency_id', prefix='currency_first')
currency_second_factory = CallbackData('currency_id', 'first', prefix='currency_second') 
currency_value_factory = CallbackData('value', 'first', 'second', prefix='currency_value')


class CurrenciesValueCallbackFilter(AdvancedCustomFilter):
    key = 'currency_value'

    def check(self, call, config):
        return config.check(query=call)


class CurrenciesFirstCallbackFilter(AdvancedCustomFilter):
    key = 'currency_first_config'

    def check(self, call, config):
        return config.check(query=call)


class CurrenciesSecondCallbackFilter(AdvancedCustomFilter):
    key = 'currency_second_config'

    def check(self, call, config):
        return config.check(query=call)


def bind_filters(bot: telebot.TeleBot):
    bot.add_custom_filter(CurrenciesFirstCallbackFilter())
    bot.add_custom_filter(CurrenciesSecondCallbackFilter())
