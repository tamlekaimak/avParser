import sqlite3 as db

def createTables():
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
        orderid int PRIMARY KEY,
        chatid int NOT NULL,
        city NVARCHAR(100) NOT NULL,
        orderData NVARCHAR(100) NOT NULL,
        FOREIGN KEY(chatid) REFERENCES Clients(chatid)
    );
    """)
    cursor.execute(query)
    connection.commit()