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
        print("Connected to DB.\n" + '-' * 20 + "\nTables:")
        cursor = connection.cursor()
        cursor.execute('SELECT name from sqlite_master where type= "table"')
        print(cursor.fetchall())
        if not cursor.fetchall():
            dbcreate.createTables()
    except Exception as e:
        print(e)


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
    query = ("SELECT chatid FROM Clients WHERE chatid = %s;" % (chatid))
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
    query = ("SELECT COUNT(*) FROM Orders WHERE chatid = %s;" % (chatid))
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
    query = ("INSERT INTO Orders (chatid, city, cityRus, orderData, isFinished) VALUES (" + str(chatid) + ", '" + str(city) + "', '" + str(cityRus) + "', '" + str(orderData) + "', 1)")
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
    query = ("SELECT orderid, cityRus, orderData, isFinished FROM Orders WHERE chatid = %s;" % (chatid))
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


def UpdateOrderStatus(orderid):
    query = ("UPDATE products SET amount = amount - " + str(i[1]) + " where name = '" + str(name) + "' and type = '" + str(type) + "'")