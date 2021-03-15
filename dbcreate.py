"""
Тут функция для создания таблиц
"""

import sqlite3 as db


def createTables():
    """
    Создание нужных таблиц

    :return:
    """
    connection = db.connect("darkDB.db")
    cursor = connection.cursor()
    query = ("""
            CREATE TABLE Clients(
            chatid int PRIMARY KEY,
            username VARCHAR(32) NOT NULL,
            ParseAmount int NOT NULL DEFAULT (0),
            SubDate DATETIME	
            );
            """)
    cursor.execute(query)
    connection.commit()
    query = ("""    
    CREATE TABLE Orders(
        orderid INTEGER PRIMARY KEY AUTOINCREMENT,
        chatid int NOT NULL,
        city NVARCHAR(100) NOT NULL,
        cityRus NVARCHAR(100) NOT NULL,
        orderData NVARCHAR(100) NOT NULL,
        Amount int NOT NULL,
        Rating int NOT NULL,
        Views int NOT NULL,
        isFinished int NOT NULL DEFAULT (0),
        FOREIGN KEY(chatid) REFERENCES Clients(chatid)
    );
    """)
    cursor.execute(query)
    connection.commit()

    query = ("""    
        CREATE TABLE PayBills(
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_data NVARCHAR(100) NOT NULL,
            parseAmount int NOT NULL,
            chatid int NOT NULL,
            isPayed int NOT NULL DEFAULT (0),
            FOREIGN KEY(chatid) REFERENCES Clients(chatid)
        );
        """)
    cursor.execute(query)
    connection.commit()

