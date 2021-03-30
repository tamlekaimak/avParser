

from telebot import types
from db import insert, IsNewClient, BuysCount, NewOrder, Orders, dbstart, getOrderStatus, getParseAmount, lastBillAmount, updateParseAmount, minusOneParse
from cities import cities
from messagesControl import mainmenu, welcome, edit, send
from botStarter import bot
from ParseManager import GoParse
from payControl import QiwiPay, check_bill, kill_bill
import json, telebot



# открываем json файл и считываем оттуда токен бота
with open('token.json', 'r', encoding='utf-8') as f:
    text = json.load(f)
botToken = text['token']

bot = telebot.AsyncTeleBot(botToken)

print("BOT STARTED!")

def isCityTrue(name):
    """
    Проверка города на валидность и отправка его английской версии

    :param name: название города на русском
    :return: если город верный, то отправка английской версии, иначе False
    """
    if name in cities.keys():
        return cities[name]
    return False


def removeSettings(chatid):
    if chatid in AmountOn:
        AmountOn.remove(chatid)
    if chatid in ViewsOn:
        ViewsOn.remove(chatid)
    if chatid in RatingOn:
        RatingOn.remove(chatid)

# массив для проверки отправления города пользователем
citysend = []
# массив для проверки отправления города пользователем
valuesend = []
# словарь в который записывается город перед отправкой в БД (на английском)
city = {}
# словарь в который записывается город перед отправкой в БД (на русском)
cityRus = {}
# словарь в который записывается товар, который нужно спарсить
value = {}
# массивы для доп параметров
AmountOn = []
RatingOn = []
ViewsOn = []


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
        new_message = 'Выберите доп. параметры парсера:'
        value[chatid] = message.text
        menu = types.InlineKeyboardMarkup()
        removeSettings(chatid)
        menu.add(types.InlineKeyboardButton(text="Кол-во объявлений продавца: Выкл", callback_data="AmountOn"))
        menu.add(types.InlineKeyboardButton(text="Рейтинг: Выкл", callback_data="RatingOn"))
        menu.add(types.InlineKeyboardButton(text="Кол-во просмотров объявления: Выкл", callback_data="ViewsOn"))
        menu.add(types.InlineKeyboardButton(text="Начать парсинг", callback_data="startParsing"))
        menu.add(types.InlineKeyboardButton(text="отмена", callback_data="cancelsend"))
        send(chatid, new_message, menu)
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
    elif message.data == 'parse' or message.data == 'cancelpay':
        try:
            if message.data == 'cancelpay':
                kill_bill(chatid)
            parseAmount = getParseAmount(chatid)
            menu = types.InlineKeyboardMarkup()
            if parseAmount > 0:
                new_message = 'Осталось еще ' + str(parseAmount) + ' парсов\n\n*Отправь мне название города:*'
                citysend.append(chatid)
                menu.add(types.InlineKeyboardButton(text="отмена", callback_data="cancelsend"))
            else:
                new_message = '*Недостаточно парсов!*\n\nВыберите нужное кол-во парсов'
                menu.add(types.InlineKeyboardButton(text="1 парс - 3₽", callback_data="parse1"))
                menu.add(types.InlineKeyboardButton(text="50 парсов - 35₽", callback_data="parse50"))
                menu.add(types.InlineKeyboardButton(text="300 парсов - 150₽", callback_data="parse300"))
                menu.add(types.InlineKeyboardButton(text="назад", callback_data="retmainmenu"))
            edit(chatid, message.message.message_id, new_message, menu)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif 'parse' in message.data:
        try:
            menu = types.InlineKeyboardMarkup()
            parseTariff = int(message.data[5:])
            if parseTariff == 1:
                href = QiwiPay(chatid, 3, 1)
                new_message = "Оплата 1 парса\n\nСсылка на оплату:\n" + str(href)
            elif parseTariff == 50:
                href = QiwiPay(chatid, 35, 50)
                new_message = "Оплата 50 парсов\n\nСсылка на оплату:\n" + str(href)
            else:
                href = QiwiPay(chatid, 150, 300)
                new_message = "Оплата 300 парсов\n\nСсылка на оплату:\n" + str(href)

            menu.add(types.InlineKeyboardButton(text="Я оплатил", callback_data="checkpay"))
            menu.add(types.InlineKeyboardButton(text="отмена", callback_data="cancelpay"))
            edit(chatid, message.message.message_id, new_message, menu, markdown=False)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'checkpay':
        try:
            if check_bill(chatid):
                new_message = "*Оплата прошла успешно!✅*\n\nПарсы зачислены."
                parseAmount = lastBillAmount(chatid)
                updateParseAmount(chatid, parseAmount)
                edit(chatid, message.message.message_id, new_message)
                mainmenu(chatid)
            else:
                menu = types.InlineKeyboardMarkup()
                kill_bill(chatid)
                new_message = "*Ошибка оплаты!❌*\n\nСчет не оплачен."
                menu.add(types.InlineKeyboardButton(text="назад", callback_data="retmainmenu"))
                edit(chatid, message.message.message_id, new_message, menu)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'profile':
        try:
            menu = types.InlineKeyboardMarkup()
            new_message = "*👨🏽‍💻Профиль*\n\nВаш id: " + str(chatid) + "\nКол-во заказов: " + str(BuysCount(chatid)) + \
                          "\nОсталось парсов: " + str(getParseAmount(chatid))
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
    elif message.data == 'AmountOn' or message.data == 'AmountOff':
        try:
            menu = types.InlineKeyboardMarkup()
            new_message = 'Выберите доп. параметры парсера:'
            if message.data == 'AmountOn':
                AmountOn.append(chatid)
                menu.add(types.InlineKeyboardButton(text="Кол-во объявлений продавца: Вкл", callback_data="AmountOff"))
            else:
                AmountOn.remove(chatid)
                menu.add(types.InlineKeyboardButton(text="Кол-во объявлений продавца: Выкл", callback_data="AmountOn"))
            if chatid in RatingOn:
                menu.add(types.InlineKeyboardButton(text="Рейтинг: Вкл", callback_data="RatingOff"))
            else:
                menu.add(types.InlineKeyboardButton(text="Рейтинг: Выкл", callback_data="RatingOn"))
            if chatid in ViewsOn:
                menu.add(types.InlineKeyboardButton(text="Кол-во просмотров объявления: Вкл", callback_data="ViewsOff"))
            else:
                menu.add(types.InlineKeyboardButton(text="Кол-во просмотров объявления: Выкл", callback_data="ViewsOn"))
            menu.add(types.InlineKeyboardButton(text="Начать парсинг", callback_data="startParsing"))
            menu.add(types.InlineKeyboardButton(text="отмена", callback_data="cancelsend"))
            edit(chatid, message.message.message_id, new_message, menu)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'RatingOn' or message.data == 'RatingOff':
        try:
            menu = types.InlineKeyboardMarkup()
            new_message = 'Выберите доп. параметры парсера:'
            if chatid in AmountOn:
                menu.add(types.InlineKeyboardButton(text="Кол-во объявлений продавца: Вкл", callback_data="AmountOff"))
            else:
                menu.add(types.InlineKeyboardButton(text="Кол-во объявлений продавца: Выкл", callback_data="AmountOn"))
            if message.data == 'RatingOn':
                RatingOn.append(chatid)
                menu.add(types.InlineKeyboardButton(text="Рейтинг: Вкл", callback_data="RatingOff"))
            else:
                RatingOn.remove(chatid)
                menu.add(types.InlineKeyboardButton(text="Рейтинг: Выкл", callback_data="RatingOn"))
            if chatid in ViewsOn:
                menu.add(types.InlineKeyboardButton(text="Кол-во просмотров объявления: Вкл", callback_data="ViewsOff"))
            else:
                menu.add(types.InlineKeyboardButton(text="Кол-во просмотров объявления: Выкл", callback_data="ViewsOn"))
            menu.add(types.InlineKeyboardButton(text="Начать парсинг", callback_data="startParsing"))
            menu.add(types.InlineKeyboardButton(text="отмена", callback_data="cancelsend"))
            edit(chatid, message.message.message_id, new_message, menu)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'ViewsOn' or message.data == 'ViewsOff':
        try:
            menu = types.InlineKeyboardMarkup()
            new_message = 'Выберите доп. параметры парсера:'
            if chatid in AmountOn:
                menu.add(types.InlineKeyboardButton(text="Кол-во объявлений продавца: Вкл", callback_data="AmountOff"))
            else:
                menu.add(types.InlineKeyboardButton(text="Кол-во объявлений продавца: Выкл", callback_data="AmountOn"))
            if chatid in RatingOn:
                menu.add(types.InlineKeyboardButton(text="Рейтинг: Вкл", callback_data="RatingOff"))
            else:
                menu.add(types.InlineKeyboardButton(text="Рейтинг: Выкл", callback_data="RatingOn"))
            if message.data == 'ViewsOn':
                ViewsOn.append(chatid)
                menu.add(types.InlineKeyboardButton(text="Кол-во просмотров объявления: Вкл", callback_data="ViewsOff"))
            else:
                ViewsOn.remove(chatid)
                menu.add(types.InlineKeyboardButton(text="Кол-во просмотров объявления: Выкл", callback_data="ViewsOn"))
            menu.add(types.InlineKeyboardButton(text="Начать парсинг", callback_data="startParsing"))
            menu.add(types.InlineKeyboardButton(text="отмена", callback_data="cancelsend"))
            edit(chatid, message.message.message_id, new_message, menu)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'startParsing':
        try:
            NewOrder(chatid, city[chatid], cityRus[chatid], value[chatid], int(chatid in AmountOn), int(chatid in RatingOn),
                     int(chatid in ViewsOn))
            minusOneParse(chatid)
            new_message = 'Заявка добавлена в очередь, осталось только подождать!\nДля перехода на главную отправь ' \
                          '/start '
            edit(chatid, message.message.message_id, new_message)
            mainmenu(chatid)
            GoParse()
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'cancelsend':
        try:
            if chatid in citysend:
                citysend.remove(chatid)
            if chatid in valuesend:
                valuesend.remove(chatid)
            removeSettings(chatid)
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
