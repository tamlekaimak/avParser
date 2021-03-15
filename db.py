"""
Тут функции по работе с БД, выгрузка, обновление, добавление новых строк и т.д.
"""

import sqlite3 as db
import dbcreate


def connectDB():
    connection = db.connect('darkDB.db')
    return connection


def dbstart():
    """
    Стартовый коннект к БД, если таблиц нет, то их создание

    :return:
    """
    try:
        connection = connectDB()
        print("Connected to DB.")

        cursor = connection.cursor()
        cursor.execute('SELECT name from sqlite_master where type= "table"')
        tables = cursor.fetchall()

        if not tables:
            dbcreate.createTables()
            cursor.execute('SELECT name from sqlite_master where type= "table"')
            tables = cursor.fetchall()
            print('-' * 20 + "\nTables created:", tables)
        else:
            print('-' * 20 + "\nTables:", tables)
    except Exception as e:
        print("Connect error: ", e)


def insert(chatid, username):
    """
    Добавление нового пользователя в БД

    :param chatid: id пользователя
    :param username: username пользователя
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Clients (chatid, username) VALUES (" + str(chatid) + ", '" + str(username) + "');")
    cursor.execute(query)
    connection.commit()
    connection.close()


def IsNewClient(chatid):
    """
    Проверка является ли пользователь новым

    :param chatid: id пользователя
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT chatid FROM Clients WHERE chatid = %s;" % chatid)
    cursor.execute(query)
    res = cursor.fetchall()
    connection.close()
    for i in res:
        if chatid == i[0]:
            return False
    return True


def BuysCount(chatid):
    """
    Количество покупок пользователя в системе

    :param chatid: id пользователя
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT COUNT(*) FROM Orders WHERE chatid = %s;" % chatid)
    cursor.execute(query)
    buyscount = cursor.fetchone()[0]
    connection.close()
    return buyscount


def NewOrder(chatid, city, cityRus, orderData):
    """
    Добавление новой заявки в БД

    :param chatid: id пользователя
    :param city: город на английском (для парсера)
    :param cityRus: город на русском
    :param orderData: название товара, который нужно спарсить
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Orders (chatid, city, cityRus, orderData) VALUES (" + str(chatid) +
             ", '" + str(city) + "', '" + str(cityRus) + "','" + str(orderData) + "')")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()


def Orders(chatid):
    """
    Все заявки пользователя

    :param chatid: id пользователя
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT orderid, cityRus, orderData, orderid FROM Orders WHERE chatid = %s;" % chatid)
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


def UpdateOrderStatus(orderid):
    """
    Обновление статуса заказа
    :param orderid: id заказа
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "UPDATE Orders SET isFinished = 1 WHERE orderid = " + str(orderid)
    cursor.execute(query)
    connection.commit()


def ParseOrder():
    """
    Находит и возвращает первый в очереди заказ из БД
    :return: id заказа, город, товар который нужно спарсить
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT orderid, city, orderData FROM Orders WHERE isFinished = 0 AND orderid = (SELECT MIN(" \
            "orderid) FROM Orders WHERE isFinished = 0) "
    cursor.execute(query)
    result = cursor.fetchone()

    return result[0], result[1], result[2]


def getChatid(orderid):
    """
    Находит chatid по id заказа
    :param orderid: id заказа
    :return: chatid пользователя
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT chatid FROM Orders WHERE orderid = " + str(orderid)
    cursor.execute(query)
    return cursor.fetchone()[0]


def isMoreOrders():
    """
    Проверяет, есть ли еще необработанные заказы
    :return: True если есть, иначе False
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT orderid FROM Orders WHERE isFinished = 0"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False


def getOrderStatus(orderid):
    """
    Возвращает статус заказа
    :param orderid: id заказа
    :return: True если заказ спарсен, иначе False
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT isFinished FROM Orders WHERE orderid = " + str(orderid)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    if result == 1:
        return True
    else:
        return False


def getParseAmount(chatid):
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT parseAmount FROM Clients WHERE chatid = " + str(chatid)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result


def newBill(bill_data, chatid, parseAmount):
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO PayBills (bill_data, chatid, parseAmount) VALUES ('" + str(bill_data) + "', " + str(chatid) + ", " + str(parseAmount) + ")")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()


def UpdateBillStatus(bill_data):
    connection = connectDB()
    cursor = connection.cursor()
    query = "UPDATE PayBills SET isPayed = 1 WHERE bill_data = '" + str(bill_data) + "'"
    cursor.execute(query)
    connection.commit()


def getBillid(chatid):
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT bill_data FROM PayBills WHERE isPayed = 0 and chatid = " + str(chatid)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result


def setRejectedStatus(bill_data):
    connection = connectDB()
    cursor = connection.cursor()
    query = "UPDATE PayBills SET isPayed = -1 WHERE bill_data = '" + str(bill_data) + "'"
    cursor.execute(query)
    connection.commit()


def lastBillAmount(chatid):
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT ParseAmount FROM PayBills WHERE chatid = " + str(chatid) + " AND bill_id = (SELECT MAX(bill_id) " \
                                                                               "FROM PayBills WHERE chatid = " + str(
        chatid) + ") "
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result


def updateParseAmount(chatid, ParseAmount):
    connection = connectDB()
    cursor = connection.cursor()
    query = "UPDATE Clients SET ParseAmount = " + str(ParseAmount) + " WHERE chatid = " + str(chatid) + ""
    cursor.execute(query)
    connection.commit()


def minusOneParse(chatid):
    connection = connectDB()
    cursor = connection.cursor()
    query = "UPDATE Clients SET ParseAmount = ParseAmount - 1 WHERE chatid = " + str(chatid) + ""
    cursor.execute(query)
    connection.commit()