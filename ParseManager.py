from db import ParseOrder, getChatid, isMoreOrders, UpdateOrderStatus
import parserpro
from messagesControl import send, senddoc


# переменная для проверки вошел ли поток в парсер
isParsingNow = False


def GoParse():
    global isParsingNow

    if not isParsingNow:
        isParsingNow = True
        while True:
            parse_id, city, value = ParseOrder()
            chatid = getChatid(parse_id)

            parserpro.main(city, value, str(chatid))
            UpdateOrderStatus(parse_id)

            send(chatid, 'Готово, держи свой csv!')
            senddoc(chatid, value)

            if not isMoreOrders():
                isParsingNow = False
                break
