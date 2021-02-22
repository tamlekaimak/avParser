import telebot
import json
import pyodbc as db

with open('token.json', 'r',encoding='utf-8') as f:
    text = json.load(f)

botToken = text['token']

bot = telebot.TeleBot(botToken)
print("BOT STARTED!")

def connectDB():
    connection = db.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-18IG06U;'
        'DATABASE=avParser;'
        'Trusted_connection=yes;'
    )
    return connection

def insert(chatid, username):
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Clients (chatid, username) VALUES (" + str(chatid) + ", '" + str(username) + "');")
    cursor.execute(query)
    connection.commit()
    connection.close()

def newClient(chatid):
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT chatid FROM Clients WHERE chatid = %s;" % (chatid))
    cursor.execute(query)
    res = cursor.fetchall()
    connection.close()
    for i in res:
        if chatid == i[0]:
            return False
    return True

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