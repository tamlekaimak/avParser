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


def NewOrder(chatid, city, cityRus, orderData, parse_id):
    """
    Добавление новой заявки в БД

    :param chatid: id пользователя
    :param city: город на английском (для парсера)
    :param cityRus: город на русском
    :param orderData: название товара, который нужно спарсить
    :param parse_id: id заказа (в очереди парсера)
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Orders (chatid, city, cityRus, parse_id, orderData) VALUES (" + str(chatid) +
             ", '" + str(city) + "', '" + str(cityRus) + "'," + str(parse_id) + ",'" + str(orderData) + "')")
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
    query = ("SELECT orderid, cityRus, orderData, parse_id FROM Orders WHERE chatid = %s;" % chatid)
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


def NewParseOrder(city, orderData):
    """
    Добавление новой заявки на парсинг в БД

    :param city: город
    :param orderData: товар который нужно спарсить
    :return: id этого заказа
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO ParseOrder (city, orderData) VALUES ('" + str(city) + "', '" + str(orderData) + "')")
    cursor.execute(query)
    connection.commit()

    query = "SELECT MAX(parse_id) FROM ParseOrder"
    cursor.execute(query)
    parse_id = cursor.fetchone()[0]

    connection.close()
    return parse_id


def UpdateOrderStatus(parse_id):
    """
    Обновление статуса заказа
    :param parse_id: id заказа
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "UPDATE ParseOrder SET isFinished = 1 WHERE parse_id = " + str(parse_id)
    cursor.execute(query)
    connection.commit()


def ParseOrder():
    """
    Находит и возвращает первый в очереди заказ из БД
    :return: id заказа, город, товар который нужно спарсить
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT parse_id, city, orderData FROM ParseOrder WHERE isFinished = 0 AND parse_id = (SELECT MIN(" \
            "parse_id) FROM ParseOrder WHERE isFinished = 0) "
    cursor.execute(query)
    result = cursor.fetchone()

    return result[0], result[1], result[2]


def getChatid(parse_id):
    """
    Находит chatid по id заказа
    :param parse_id: id заказа
    :return: chatid пользователя
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT chatid FROM Orders WHERE parse_id = " + str(parse_id)
    cursor.execute(query)
    return cursor.fetchone()[0]


def isMoreOrders():
    """
    Проверяет, есть ли еще необработанные заказы
    :return: True если есть, иначе False
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT parse_id FROM ParseOrder WHERE isFinished = 0"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False


def getOrderStatus(parse_id):
    """
    Возвращает статус заказа
    :param parse_id: id заказа
    :return: True если заказ спарсен, иначе False
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT isFinished FROM ParseOrder WHERE parse_id = " + str(parse_id)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    if result == 1:
        return True
    else:
        return False

