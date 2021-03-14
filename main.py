from telebot import types
import parserpro
from db import insert, IsNewClient, BuysCount, NewOrder, Orders, dbstart, NewParseOrder, getOrderStatus
from cities import cities
from messagesControl import mainmenu, welcome, edit, send
from botStarter import bot
from ParseManager import GoParse

def isCityTrue(name):
    """
    Проверка города на валидность и отправка его английской версии

    :param name: название города на русском
    :return: если город верный, то отправка английской версии, иначе False
    """
    if name in cities.keys():
        return cities[name]
    return False


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
    if IsNewClient(chatid):
        welcome(chatid)
    else:
        mainmenu(chatid)


@bot.message_handler(content_types=['text'])
def texthandler(message):
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
        new_message = 'Заявка добавлена в очередь, осталось только подождать!\nДля перехода на главную отправь /start'
        send(chatid, new_message)
        value = message.text
        print('DATA: ', city[chatid], value, str(chatid))
        parse_id = NewParseOrder(city[chatid], value)
        NewOrder(chatid, city[chatid], cityRus[chatid], value, parse_id)
        GoParse()
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
            mainmenu(chatid, message.message.message_id)
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
            new_message = "*👨🏽‍💻Профиль*\n\nВаш id: " + str(chatid) + "\nКол-во заказов: " + str(BuysCount(chatid))
            menu.add(types.InlineKeyboardButton(text="назад", callback_data="retmainmenu"))
            edit(chatid, message.message.message_id, new_message, menu)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'history':
        try:
            menu = types.InlineKeyboardMarkup()
            new_message = '*🗒История*\n\n'
            if BuysCount(chatid) == 0:
                new_message += 'У вас нет заказов!'
            else:
                new_message += 'Ваши заказы:\n'
                for orderid, CityRus, orderData, parse_id in Orders(chatid):
                    new_message += "*#" + str(orderid) + "*\n" + str(CityRus) + ": " + str(orderData) + "\nСтатус: "
                    if getOrderStatus(parse_id):
                        new_message += "Отправлен✅\n\n"
                    else:
                        new_message += "В очереди⏳\n\n"
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

            mainmenu(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'retmainmenu':
        try:
            mainmenu(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)


if __name__ == '__main__':
    dbstart()
    bot.polling()
