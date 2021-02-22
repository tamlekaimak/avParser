import pyodbc as db

def connectDB():
    connection = db.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-18IG06U;'
        'DATABASE=avParser;'
        'Trusted_connection=yes;'
    )
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