import telebot
from telebot import types

bot = telebot.TeleBot('1760095413:AAEGj4-Zl_Ux28_10xXphDH1Ni5t0LsfkEk')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
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
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши /start и бот начнет работу. Напиши /menu и откроется меню выбора"
                                               " темы.")
    elif message.text == "/menu":
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
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю(( Напиши /help')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "number1":
        with open('1.txt', encoding='utf-8') as f:
            text = f.read()
        splited_text = text.split('$')
        for i in splited_text:
            bot.send_message(call.message.chat.id, i)
            keyboard = types.InlineKeyboardMarkup()
            key_next = types.InlineKeyboardButton(text='Следующий апвоут', callback_data='next')
            keyboard.add(key_next)
            key_previous = types.InlineKeyboardButton(text='Предыдущий апвоут', callback_data='previous')
            keyboard.add(key_previous)
            bot.send_message(call.from_user.id, text='Выбери, что делать дальше', reply_markup=keyboard)
    if call.data == "number2":
        with open('2.txt', encoding='utf-8') as g:
            text = g.read()
        splited_text = text.split('$')
        for k in splited_text:
            bot.send_message(call.message.chat.id, k)
    if call.data == "number3":
        with open('3.txt', encoding='utf-8') as t:
            text = t.read()
        splited_text = text.split('$')
        for j in splited_text:
            bot.send_message(call.message.chat.id, j)


bot.polling(none_stop=True, interval=0)
