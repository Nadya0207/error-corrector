import telebot
from telebot import types
import json
import random                               # импорты

bot = telebot.TeleBot('1842261563:AAFUP-lfLPTRhEkSfPoNM9hFLB53ltxbwLQ')             # токен

memory_from_user = dict()                 # хранитель данных, полученных от пользователя
memory_from_bot = dict()                  # хранитель данных, отправляемых ботом


def send_upvote(message, text, i, number):                  # отправляет апвоут
    bot.send_message(message.from_user.id, text[i])
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    key_next = types.InlineKeyboardButton(text='Другой апвоут', callback_data=number)
    keyboard.add(key_next)
    key_home = types.InlineKeyboardButton(text='Другая тема', callback_data='menu')
    keyboard.add(key_home)
    msg = 'Что хочешь дальше?'
    a = bot.send_message(message.from_user.id, text=msg, reply_markup=keyboard)
    return a


def get_answer(message):
    if message.from_user.id not in memory_from_user:
        memory_from_user[message.from_user.id] = list()
    memory_from_user[message.from_user.id].append({'text': message.text, 'time': message.date})
    with open('data_from_user.json', 'w', encoding='utf-8') as r:
        json.dump(memory_from_user, r, ensure_ascii=False, indent=4)


@bot.message_handler(commands=['start'])                    # команда /start
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет! Этот бот-апвоут, в котором вы можете прочитать интересные факты"
                                           " и истории людей\n" + "✨" + "Чтобы узнать, как пользоваться ботом, "
                                           " воспользуйтесь командой /help\n" + "✨" + "Чтобы открыть меню выбора "
                                           " текстов, воспользуйтесь командой /menu\n" + "✨" + "Чтобы узнать, откуда"
                                           " взята информация для этого бота, воспользуйтесь командой /info")


@bot.message_handler(commands=['help'])                # команда /help
def send_help(message):
    bot.send_message(message.from_user.id, "Что нужно знать про бот:\n" + "1️⃣" + "В меню выбора (/menu) Вам будут "
                                           "предложены несколько тем, выберите одну из них\n" + "2️⃣" + "После выбора "
                                           "темы Вы получите апвоут, его можно не только прочитать, но и"
                                           " ответным сообщением перенабрать с клавиатуры, чтобы помочь нам собрать"
                                           "данные для проекта\n" + "3️⃣" + "Т9 отключать не нужно, главное - отправить"
                                           " то, что получится, не исправляя\n" + "4️⃣" + "Наш бот, к сожалению, "
                                           "не совершенен, поэтому иногда он может присылать то, что уже присылал " +
                                           "🤡" + " Это нормально, просто нажмите 'Другой апвоут'\n" + "5️⃣" + "В ботах"
                                           " ограниченное число апвоутов, поэтому, если не получаете новых, просто "
                                           "поменяйте тему")


@bot.message_handler(commands=['info'])                # команда /info
def send_info(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="👉" + "Клик" + "👈",
                                            url="https://www.youtube.com/channel/UC-iU28QW_832Fx_3RJ_vYPQ")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Все тексты апвоутов взяты отсюда", reply_markup=keyboard)


@bot.message_handler(commands=['menu'])                 # команда /menu
def send_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Какой фильм кончился бы за 10 минут, если бы герой не тупил?',
                                       callback_data='number1')
    keyboard.add(key_1)
    key_2 = types.InlineKeyboardButton(text='Как думаете, что нас ждёт после смерти?',
                                       callback_data='number2')
    keyboard.add(key_2)
    key_3 = types.InlineKeyboardButton(text='Крутые факты про динозавров',
                                       callback_data='number3')
    keyboard.add(key_3)
    bot.send_message(message.from_user.id, text='Выбери тему!', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)         # обработчик кнопочек
def callback_worker(call):
    if call.data == "menu":
        send_menu(call)

    if call.data == "number1":
        with open('1.txt', encoding='utf-8') as f:
            text = f.read()
        splited_text = text.split('$')
        s = random.randint(0, len(splited_text) - 1)
        msg_send_first = splited_text[s]
        msg_send_second = send_upvote(call, splited_text, s, 'number1')
        bot.register_next_step_handler(msg_send_second, get_answer)
        if call.from_user.id not in memory_from_bot:
            memory_from_bot[call.from_user.id] = list()
        memory_from_bot[call.from_user.id].append({'text': msg_send_first, 'time': msg_send_second.date})
        with open('data_from_bot.json', 'w', encoding='utf-8') as p:
            json.dump(memory_from_bot, p, ensure_ascii=False, indent=4)

    if call.data == "number2":
        with open('2.txt', encoding='utf-8') as g:
            text = g.read()
        splited_text = text.split('$')
        s = random.randint(0, len(splited_text) - 1)
        msg_send_first = splited_text[s]
        memory_from_bot[call.from_user.id] = msg_send_first
        msg_send_second = send_upvote(call, splited_text, s, 'number2')
        bot.register_next_step_handler(msg_send_second, get_answer)
        if call.from_user.id not in memory_from_bot:
            memory_from_bot[call.from_user.id] = list()
        memory_from_bot[call.from_user.id].append({'text': msg_send_first, 'time': msg_send_second.date})
        with open('data_from_bot.json', 'w', encoding='utf-8') as p:
            json.dump(memory_from_bot, p, ensure_ascii=False, indent=4)

    if call.data == "number3":
        with open('3.txt', encoding='utf-8') as t:
            text = t.read()
        splited_text = text.split('$')
        s = random.randint(0, len(splited_text) - 1)
        msg_send_first = splited_text[s]
        memory_from_bot[call.from_user.id] = msg_send_first
        msg_send_second = send_upvote(call, splited_text, s, 'number3')
        bot.register_next_step_handler(msg_send_second, get_answer)
        if call.from_user.id not in memory_from_bot:
            memory_from_bot[call.from_user.id] = list()
        memory_from_bot[call.from_user.id].append({'text': msg_send_first, 'time': msg_send_second.date})
        with open('data_from_bot.json', 'w', encoding='utf-8') as p:
            json.dump(memory_from_bot, p, ensure_ascii=False, indent=4)


bot.polling(none_stop=True, interval=0)
