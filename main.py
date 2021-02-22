import telebot
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

@bot.message_handler(commands=['start'])
def start(message):
    chatid = message.chat.id
    if newClient(chatid):
        print(132123123)
        insert(chatid, str(message.chat.username))
        new_message = "Привет, " + str(message.chat.first_name) + "!\n\nЭто avParser, здесь ты можешь заказать парс объявлений из Авито!"
    else:
        new_message = "С возвращением, " + str(message.chat.first_name) + "!\n\nХотите заказать парс?"
    send(chatid, new_message)

if __name__ == '__main__':
    bot.polling()