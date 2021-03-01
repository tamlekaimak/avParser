import pyodbc as db

from db import connectDB, insert, newClient
import pandas as pd
import pytest



import string
import random

def id_generator(size=33, chars=string.ascii_uppercase):
    return [''.join(random.choice(chars) for _ in range(size)) for _ in range(0,3)]

LONG_USER = id_generator()

TEST_INSERT_NEGATIVE_CHATID = [('-4','Sasha'),('-3','Sasha')]
TEST_INSERT_LONG_USER = [('1',LONG_USER[0]),('2',LONG_USER[1]),('3',LONG_USER[2])]
TEST_INSERT_PM_KEY = [('12','Sashsa'), ('12','Misha')]
TEST_INSERT_CORRECT_VALUES = [('100','Gena'), ('120','Pasha')]
TEST_SELECT_VALUES = [(100,'Gena'), (120,'Pasha'),(99,'HAHA'),('100','HIHI')]

class TestDatabase:

    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_PM_KEY)
    def test_insert_PM_KEY(self, chatid, username):
        insert(chatid, username)

    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_NEGATIVE_CHATID)
    def test_insert_negative_id(self, chatid, username):
        insert(chatid, username)

    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_LONG_USER)
    def test_insert_long_name(self, chatid, username):
        insert(chatid, username)

    @pytest.mark.xpass
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_CORRECT_VALUES)
    def test_insert_correct(self, chatid, username):
        insert(chatid, username)

    @pytest.mark.parametrize("chatid, username", TEST_SELECT_VALUES)
    def test_select_new_chatid(self, chatid,username):
        assert False == newClient(chatid), 'Excepting correct select by chatID'




# def clean_():
#     conn = db.connect(driver='{SQL Server}', server='DESKTOP-PGQ7DJM', database='avParser')
#     cursor = conn.cursor()
#     cursor.execute("Delete from Clients where [chatid] IN (?,?,?,?,?,?) ;",('12','100','120','-4','-3','100'))
#     conn.commit()
#     conn.close()
#
# if __name__ =='__main__':
#
#     clean_()






