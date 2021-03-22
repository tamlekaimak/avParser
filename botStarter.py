"""
Здесь стартуется бот
"""

import telebot
import json

# открываем json файл и считываем оттуда токен бота
with open('token.json', 'r', encoding='utf-8') as f:
    text = json.load(f)

botToken = text['token']

bot = telebot.TeleBot(botToken)

print("BOT STARTED!")