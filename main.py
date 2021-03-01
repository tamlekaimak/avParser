import telebot
import parserPRO
from telebot import types
import json
from db import connectDB, insert, newClient
from cities import cities
import time


# открываем json файл и считываем оттуда токен бота
with open('token.json', 'r', encoding='utf-8') as f:
    text = json.load(f)

botToken = text['token']

bot = telebot.AsyncTeleBot(botToken)

print("BOT STARTED!")

def isCityTrue(name):
    if name in cities.keys():
        return cities[name]
    return False

def sendmenu(chatid, message, menu, markdown=True):
    try:
        if markdown:
            bot.send_message(chatid, message, reply_markup=menu, parse_mode='Markdown')
        else:
            bot.send_message(chatid, message, reply_markup=menu)
    except Exception as e:
        print(e)
        return False
    else:
        return True

def send(chatid, message):
    try:
        bot.send_message(chatid, message, parse_mode='Markdown')
    except Exception as e:
        print(e)
        return False
    else:
        return True

def editmenu(chatid, messageid, new_message, menu, markdown=True):
    try:
        if markdown:
            bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, reply_markup=menu, parse_mode='Markdown')
        else:
            bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, reply_markup=menu)
    except Exception as e:
        print(e)
        return False
    else:
        return True

def senddoc(chatid, value):
    try:    
        bot.send_document(chatid, open('csv//' + value + str(chatid) + '_.csv', 'rb'))
    except Exception as e:
        print(e)
        return False
    else:
        return True


def edit(chatid, messageid, new_message):
    try:
        bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, parse_mode='Markdown')
    except Exception as e:
        print(e)
        return False
    else:
        return True

def mainmenu(chatid):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='🔎Спарсить', callback_data='parse'))
    #menu.add(types.InlineKeyboardButton(text='👨🏽‍💻Профиль', callback_data='profile'), types.InlineKeyboardButton(text='🗒История', callback_data='history'))
    #menu.add(types.InlineKeyboardButton(text='❓Инструкция', callback_data='instruction'), types.InlineKeyboardButton(text='👨🏼‍🔧Помощь', callback_data='help'))
    new_message = "_Главное меню_"
    sendmenu(chatid, new_message, menu)

def retmainmenu(chatid, message_id):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='🔎Спарсить', callback_data='parse'))
    #menu.add(types.InlineKeyboardButton(text='👨🏽‍💻Профиль', callback_data='profile'), types.InlineKeyboardButton(text='🗒История', callback_data='history'))
    #menu.add(types.InlineKeyboardButton(text='❓Инструкция', callback_data='instruction'), types.InlineKeyboardButton(text='👨🏼‍🔧Помощь', callback_data='help'))
    new_message = "_Главное меню_"
    try:
        bot.edit_message_text(chat_id=chatid, message_id=message_id, text=new_message, reply_markup=menu,
                          parse_mode='Markdown')
    except Exception as e:
        print(e)

def welcome(chatid):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text="🗒Инструкция", url="https://telegra.ph/")) #<ссылка на инструкцию>
    menu.add(types.InlineKeyboardButton(text="Пользовательское соглашение", url="https://telegra.ph/")) #<ссылка на польз. соглашение>
    menu.add(types.InlineKeyboardButton(text='Продолжить', callback_data='continue'))
    new_message = "Добро пожаловать в avParser!\n\nПрочитайте инструкцию перед входом.\n\nДля продолжения необходимо принять *Пользовательское соглашение*"
    sendmenu(chatid, new_message, menu)

# массив для проверки отправления города пользователем
citysend = []
# массив для проверки отправления города пользователем
valuesend = []
# словарь в который записывается город перед отправкой в БД
city = {}

@bot.message_handler(commands=['start'])
def start(message):
    chatid = message.chat.id
    if newClient(chatid):
        welcome(chatid)
    else:
        mainmenu(chatid)

@bot.message_handler(content_types=['text'])
def texthandle(message):
    chatid = message.chat.id
    if chatid in citysend:
        check = isCityTrue(message.text)
        if check:
            citysend.remove(chatid)
            city[chatid] = check
            new_message = 'Отлично, теперь запрос:'
            send(chatid, new_message)
            valuesend.append(chatid)
        else:
            new_message = 'Город не найден! Попробуй еще раз:'
            send(chatid, new_message)
    elif chatid in valuesend:
        valuesend.remove(chatid)
        new_message = 'Парсер запущен, осталось только подождать!'
        send(chatid, new_message)
        value = message.text
        print('DATA: ', city[chatid], value, str(chatid))
        parserPRO.main(city[chatid], value, chatid)
        new_message = 'Готово, держи свой csv, терпила!'
        send(chatid, new_message)
        senddoc(chatid, value, new_message)
    else:
        new_message = 'Я тебя не понял!'
        send(chatid, new_message)


@bot.callback_query_handler(func=lambda message: True)
def answer(message):
    chatid = message.message.chat.id
    if message.data == 'continue':
        try:
            username = str(message.message.chat.username)
            insert(chatid, username)
            retmainmenu(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'parse':
        try:
           new_message = 'Оптправь мне название города:'
           citysend.append(chatid)
           edit(chatid, message.message.message_id, new_message)
        except Exception as e:
            print(message.data + ' Error: ', e)
           



if __name__ == '__main__':
    bot.polling()