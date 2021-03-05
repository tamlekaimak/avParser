import telebot
import parserpro
from telebot import types
import json
from db import connectDB, insert, newClient, BuysCount, NewOrder, Orders
from cities import cities
import time
import dbcreate
import sqlite3 as db
# открываем json файл и считываем оттуда токен бота
with open('token.json', 'r', encoding='utf-8') as f:
    text = json.load(f)

botToken = text['token']

bot = telebot.TeleBot("1484844322:AAGj3l-O8wAIlp-O_0VTIa-zhaFji78lyMY")

print("BOT STARTED!")


try:
    connection = db.connect("darkDB.db")
    print("Connected to DB.\n" + '-'*20 + "\nTables:")
    cursor = connection.cursor()
    cursor.execute('SELECT name from sqlite_master where type= "table"')
    print(cursor.fetchall())
    if not cursor.fetchall():
        dbcreate.createTables()
except Exception as e:
    print(e)

def isCityTrue(name):
    if name in cities.keys():
        return cities[name]
    return False

def send(chatid, message, menu=False, markdown=True):
    try:
        if not menu:
            bot.send_message(chatid, message, parse_mode='Markdown')
        else:
            if markdown:
                bot.send_message(chatid, message, reply_markup=menu, parse_mode='Markdown')
            else:
                bot.send_message(chatid, message, reply_markup=menu)
    except Exception as e:
        print(e)
        return False
    else:
        return True

def edit(chatid, messageid, new_message, menu=False, markdown=True):
    try:
        if not menu:
            bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, parse_mode='Markdown')
        else:
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
        bot.send_document(chatid, open('csv//' + value + str(chatid) + '.csv', 'rb'))
    except Exception as e:
        print(e)
        return False
    else:
        return True


def mainmenu(chatid):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='🔎Спарсить', callback_data='parse'))
    menu.add(types.InlineKeyboardButton(text='👨🏽‍💻Профиль', callback_data='profile'), types.InlineKeyboardButton(text='🗒История', callback_data='history'))
    #menu.add(types.InlineKeyboardButton(text='❓Инструкция', callback_data='instruction'), types.InlineKeyboardButton(text='👨🏼‍🔧Помощь', callback_data='help'))
    new_message = "_Главное меню_"
    send(chatid, new_message, menu)

def retmainmenu(chatid, message_id):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='🔎Спарсить', callback_data='parse'))
    menu.add(types.InlineKeyboardButton(text='👨🏽‍💻Профиль', callback_data='profile'), types.InlineKeyboardButton(text='🗒История', callback_data='history'))
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
    send(chatid, new_message, menu)

# массив для проверки отправления города пользователем
citysend = []
# массив для проверки отправления города пользователем
valuesend = []
# словарь в который записывается город перед отправкой в БД (на английском)
city = {}
# словарь в который записывается город перед отправкой в БД (на русском)
cityRus = {}

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
            menu = types.InlineKeyboardMarkup()
            citysend.remove(chatid)
            city[chatid] = check
            cityRus[chatid] = message.text
            new_message = 'Отлично, теперь запрос:'
            valuesend.append(chatid)
            menu.add(types.InlineKeyboardButton(text="отмена", callback_data="cancelsend"))
            send(chatid, new_message, menu)
        else:
            new_message = 'Город не найден! Попробуй еще раз:'
            send(chatid, new_message)
    elif chatid in valuesend:
        valuesend.remove(chatid)
        new_message = 'Парсер запущен, осталось только подождать!'
        send(chatid, new_message)
        value = message.text
        print('DATA: ', city[chatid], value, str(chatid))
        NewOrder(chatid, city[chatid], cityRus[chatid], value)
        parserpro.main(city[chatid], value, str(chatid))
        new_message = 'Готово, держи свой csv!'
        send(chatid, new_message)
        senddoc(chatid, value)
        mainmenu(chatid)
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
           menu = types.InlineKeyboardMarkup()
           new_message = 'Отправь мне название города:'
           citysend.append(chatid)
           menu.add(types.InlineKeyboardButton(text="отмена", callback_data="cancelsend"))
           edit(chatid, message.message.message_id, new_message, menu)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'profile':
        try:
            menu = types.InlineKeyboardMarkup()
            new_message = "Ваш id: " + str(chatid) + "\nКол-во заказов: " + str(BuysCount(chatid))
            menu.add(types.InlineKeyboardButton(text="назад", callback_data="retmainmenu"))
            edit(chatid, message.message.message_id, new_message, menu)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'history':
        try:
            menu = types.InlineKeyboardMarkup()
            if BuysCount(chatid) == 0:
                new_message = 'У вас нет заказов!'
            else:
                new_message = 'Ваши заказы:\n'
                for orderid, cityRus, orderData, isFinished in Orders(chatid):
                    new_message += "*#" + str(orderid) + "*\n" + str(cityRus) + ": " + str(orderData) + "\nСтатус: "
                    if isFinished == 0:
                        new_message += "В очереди❌\n\n"
                    else:
                        new_message += "Отправлен✅\n\n"
            menu.add(types.InlineKeyboardButton(text="назад", callback_data="retmainmenu"))
            edit(chatid, message.message.message_id, new_message, menu)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'cancelsend':
        try:
            if chatid in citysend:
                citysend.remove(chatid)
            if chatid in valuesend:
                valuesend.remove(chatid)
            
            retmainmenu(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'retmainmenu':
        try:
            retmainmenu(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)
           



if __name__ == '__main__':
    bot.polling()