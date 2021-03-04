import pyodbc as db_

from db import connectDB, insert, newClient
import pandas as pd
import pytest



import string
import random

def id_generator(size=39, chars=string.ascii_uppercase):
    return [''.join(random.choice(chars) for _ in range(size)) for _ in range(0,3)]

LONG_USER = id_generator()

TEST_INSERT_NEGATIVE_CHATID = [(-4, 'Sasha'),(-3,'Sasha')]
TEST_INSERT_LONG_USER = [(1, LONG_USER[0]),(2, LONG_USER[1]),(3,LONG_USER[2])]
TEST_INSERT_CORRECT_VALUES = [(100,'Gena'), (120,'Pasha')]
TEST_INSERT_INCORRECT_FORMAT = [('3423423325',1242344), (34543663, True)]
TEST_SELECT_NEW_VALUES = [(50,'Gena'), (60,'Pasha'), (99,'HAHA')]
TEST_SELECT_OLD_VALUES = [(100,'Genaaaa'), (120,'Pashaaaa')]


def clean_():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("Delete from Clients")
    conn.commit()
    conn.close()

# if __name__=='__main__':
#      clean_()


class TestDatabase:

    @pytest.fixture(scope='session')
    def fin(self):
        yield
        clean_()

    @pytest.mark.xpass
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_CORRECT_VALUES)
    def test_insert_correct(self, chatid, username):
        insert(chatid, username)

    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_CORRECT_VALUES)
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
    @pytest.mark.parametrize("chatid, username", TEST_SELECT_NEW_VALUES)
    def test_select_new_chatid(self, chatid, username):
        assert True == newClient(chatid), 'Excepting correct select by chatID'

    @pytest.mark.xpass
    @pytest.mark.parametrize("chatid, username", TEST_SELECT_OLD_VALUES)
    def test_select_old_chatid(self, chatid, username):
        assert False == newClient(chatid), 'Excepting correct select by chatID'

    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_SELECT_NEW_VALUES)
    def test_select_wrong_new_chatid(self, chatid, username):
        assert False == newClient(chatid), 'Excepting correct select by chatID'

    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_INCORRECT_FORMAT)
    def test_insert_incorrect(self, chatid, username, fin):
        insert(chatid, username)






