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


if __name__ == '__main__':
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT * FROM Clients")
    cursor.execute(query)
    res = cursor.fetchall()
    for i in res:
        print(i)
    connection.close()

