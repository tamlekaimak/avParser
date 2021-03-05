import sqlite3 as db

def connectDB():
    connection = db.connect('darkDB.db')
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

def BuysCount(chatid):
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT COUNT(*) FROM Orders WHERE chatid = %s;" % (chatid))
    cursor.execute(query)
    buyscount = cursor.fetchone()[0]
    connection.close()
    return buyscount

def NewOrder(chatid, city, cityRus, orderData):
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Orders (chatid, city, cityRus, orderData, isFinished) VALUES (" + str(chatid) + ", '" + str(city) + "', '" + str(cityRus) + "', '" + str(orderData) + "', 1)")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def Orders(chatid):
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT orderid, cityRus, orderData, isFinished FROM Orders WHERE chatid = %s;" % (chatid))
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

def UpdateOrderStatus(orderid):
    query = ("UPDATE products SET amount = amount - " + str(i[1]) + " where name = '" + str(name) + "' and type = '" + str(type) + "'")