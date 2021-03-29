"""
Тут функция по парсингу
"""

from db import ParseOrder, getChatid, isMoreOrders, UpdateOrderStatus, getGmail
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
            gmail = getGmail(chatid)
            if gmail == 'не указан':
                gmail = None
            data = {
                "userInfo": {
                    "userID": chatid
                },
                "parseBody": {
                    "filters":
                        {
                            "addsAmount": int(Amount),
                            "sellerRating": int(Rating),
                            "addViews": int(Views)
                        },
                    "city": city,
                    "value": value,
                    "google": gmail
                }
            }
            if gmail:
                name, href = parserpro.main(data)
                UpdateOrderStatus(parse_id)
                send(chatid, 'Готово, держи свой заказ!\n\nСсылка на Google Documents:\n' + str(href))
            else:
                name = parserpro.main(data)
                UpdateOrderStatus(parse_id)
                send(chatid, 'Готово, держи свой заказ!')
            senddoc(chatid, name, '.xlsx')
            senddoc(chatid, name, '.csv')
            if not isMoreOrders():
                isParsingNow = False
                break
