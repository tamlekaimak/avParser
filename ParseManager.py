"""
Тут функция по парсингу
"""

from db import ParseOrder, getChatid, isMoreOrders, UpdateOrderStatus
import parserpro
from messagesControl import send, senddoc


# переменная для проверки вошел ли поток в парсер
isParsingNow = False


def GoParse():
    """
    Функция котролирует чтобы оба потока не заходили в парсер, пока один поток парсит, второй отвечает на сообщения
    :return:
    """
    global isParsingNow

    if not isParsingNow:
        isParsingNow = True
        while True:
            parse_id, city, value, Amount, Rating, Views = ParseOrder()
            chatid = getChatid(parse_id)

            parserpro.main(city, value, str(chatid), bool(int(Amount)), bool(int(Rating)), bool(int(Views)))
            UpdateOrderStatus(parse_id)

            send(chatid, 'Готово, держи свой csv!')
            senddoc(chatid, value)

            if not isMoreOrders():
                isParsingNow = False
                break
