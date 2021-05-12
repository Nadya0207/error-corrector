import telebot
from telebot import types
import random                               # импорты

bot = telebot.TeleBot('1842261563:AAFUP-lfLPTRhEkSfPoNM9hFLB53ltxbwLQ')             # токен

MEMORY = dict()                 # хранитель данных


def send_memorize(user_id, text, keyboard=None):
    MEMORY[user_id] = {"text": text, "is upvote": False}
    bot.send_message(user_id, text, reply_markup=keyboard)


@bot.message_handler(commands=['start'])                    # команда /start
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет! Этот бот-апвоут, в котором вы можете прочитать интересные факты"
                                           " и истории людей, а взамен перепечатать увиденную историю и помочь нам "
                                           "с проектом! При печати не требуется отключать Т9, нужно лишь не "
                                           "исправлять никакие ошибки в тексте))")
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Какой фильм законился бы через 10 минут, если бы герой не тупил?',
                                       callback_data='number1')
    keyboard.add(key_1)
    key_2 = types.InlineKeyboardButton(text='Как думаете, что нас ждёт после смерти?',
                                       callback_data='number2')
    keyboard.add(key_2)
    key_3 = types.InlineKeyboardButton(text='Крутые факты про динозавров',
                                       callback_data='number3')
    keyboard.add(key_3)
    bot.send_message(message.from_user.id, text='Выбери тему!', reply_markup=keyboard)


@bot.message_handler(commands=['help'])                # команда /help
def send_help(message):
    bot.send_message(message.from_user.id, "Напиши /start и бот начнет работу. Напиши /menu и откроется меню выбора"
                                           " темы.")


@bot.message_handler(commands=['menu'])                 # команда /menu
def send_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Какой фильм законился бы через 10 минут, если бы герой не тупил?',
                                       callback_data='number1')
    keyboard.add(key_1)
    key_2 = types.InlineKeyboardButton(text='Как думаете, что нас ждёт после смерти?',
                                       callback_data='number2')
    keyboard.add(key_2)
    key_3 = types.InlineKeyboardButton(text='Крутые факты про динозавров',
                                       callback_data='number3')
    keyboard.add(key_3)
    bot.send_message(message.from_user.id, text='Выбери тему!', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "number1":
        with open('1.txt', encoding='utf-8') as f:
            text = f.read()
        splited_text = text.split('$')
        i = random.randint(0, len(splited_text))
        bot.send_message(call.message.chat.id, splited_text[i])
    if call.data == "number2":
        with open('2.txt', encoding='utf-8') as g:
            text = g.read()
        splited_text = text.split('$')
        k = random.randint(0, len(splited_text))
        bot.send_message(call.message.chat.id, splited_text[k])
    if call.data == "number3":
        with open('3.txt', encoding='utf-8') as t:
            text = t.read()
        splited_text = text.split('$')
        j = random.randint(0, len(splited_text))
        bot.send_message(call.message.chat.id, splited_text[j])


bot.polling(none_stop=True, interval=0)
