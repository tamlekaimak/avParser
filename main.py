import telebot
from telebot import types
import json
from db import connectDB, insert, newClient


with open('token.json', 'r',encoding='utf-8') as f:
    text = json.load(f)

botToken = text['token']

bot = telebot.TeleBot(botToken)
print("BOT STARTED!")

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

def mainmenu(chatid):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='🔎Спарсить', callback_data='parse'))
    menu.add(types.InlineKeyboardButton(text='👨🏽‍💻Профиль', callback_data='profile'), types.InlineKeyboardButton(text='🗒История', callback_data='history'))
    menu.add(types.InlineKeyboardButton(text='❓Инструкция', callback_data='instruction'), types.InlineKeyboardButton(text='👨🏼‍🔧Помощь', callback_data='help'))
    new_message = "_Главное меню_"
    sendmenu(chatid, new_message, menu)

def retmainmenu(chatid, message_id):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='🔎Спарсить', callback_data='parse'))
    menu.add(types.InlineKeyboardButton(text='👨🏽‍💻Профиль', callback_data='profile'), types.InlineKeyboardButton(text='🗒История', callback_data='history'))
    menu.add(types.InlineKeyboardButton(text='❓Инструкция', callback_data='instruction'), types.InlineKeyboardButton(text='👨🏼‍🔧Помощь', callback_data='help'))
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

@bot.message_handler(commands=['start'])
def start(message):
    chatid = message.chat.id
    if newClient(chatid):
        welcome(chatid)
    else:
        mainmenu(chatid)

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


if __name__ == '__main__':
    bot.polling()