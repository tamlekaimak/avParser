import sqlite3 as db

from db import *
import pandas as pd
import pytest



import string
import random

def id_generator(size=39, chars=string.ascii_uppercase):
    return [''.join(random.choice(chars) for _ in range(size)) for _ in range(0,3)]

LONG_USER = id_generator()

TEST_INSERT_NEGATIVE_CHATID = [(-4, 'Sasha'),(-3,'Sasha')]
TEST_INSERT_LONG_USER = [(1, LONG_USER[0]),(2, LONG_USER[1]),(3,LONG_USER[2])]
TEST_INSERT_CORRECT_VALUES = [(100, 'Gena'), (120, 'Pasha')]
TEST_INSERT_INCORRECT_FORMAT = [('3423423325',1242344), (34543663, True)]
TEST_SELECT_NEW_VALUES = [(50,'Gena'), (60,'Pasha'), (99,'HAHA')]
TEST_SELECT_OLD_VALUES = [(100,'Genaaaa'), (120,'Pashaaaa')]



TEST_CREATE_ORDER = [(123, 'Kazan', 'Казань', 'Самокат', 1), (234, 'Samara', 'Самара', 'Самокат', 2)]
TEST_CREATE_ORDER_PK = [(123131, 'Kazan', 'Казань', 'Самокат', 1),(123131, 'Samara', 'Самара', 'Самокат', 3)]

TEST_PARSE_ORDER = [i[1::2] for i in TEST_CREATE_ORDER_PK]

def clean_():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("Delete from Clients where chatid in (-4,-3,1,0,2,3,100,120,3423423325,34543663,50,60,99);")
    conn.commit()
    cursor.execute("Delete from Orders where chatid in (1,123,234,123131,123132);")
    conn.commit()
    cursor.execute("Delete from ParseOrder;")
    conn.commit()
    conn.close()


class TestDatabase:

    @pytest.fixture(scope='session')
    def fin(self):
        clean_()
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

    @pytest.mark.parametrize("chatid, username", TEST_INSERT_CORRECT_VALUES)
    def test_order_count_empty(self, chatid, username):
        assert BuysCount(chatid) == 0

    @pytest.mark.parametrize("chatid, city, cityRus, orderData, parse_id", TEST_CREATE_ORDER)
    def test_order_create(self, chatid, city, cityRus, orderData, parse_id):
        """
        Test could we add a new client to our db and
        :param chatid: id пользователя
        :param city: город на английском (для парсера)
        :param cityRus: город на русском
        :param orderData: название товара, который нужно спарсить
        :param parse_id: id заказа (в очереди парсера)
        :return:
        """
        NewOrder(chatid, city, cityRus, orderData, parse_id)


    @pytest.mark.parametrize("chatid, city, cityRus, orderData, parse_id", TEST_CREATE_ORDER_PK)
    def test_order_create_pk(self, chatid, city, cityRus, orderData, parse_id):
        """
        Test could we add a new client to our db and
        :param chatid: id пользователя
        :param city: город на английском (для парсера)
        :param cityRus: город на русском
        :param orderData: название товара, который нужно спарсить
        :param parse_id: id заказа (в очереди парсера)
        :return:
        """
        NewOrder(chatid, city, cityRus, orderData, parse_id)

    @pytest.mark.parametrize("chatid, city, cityRus, orderData, parse_id", TEST_CREATE_ORDER_PK)
    def test_order_count_equal(self, chatid, city, cityRus, orderData, parse_id):
        assert BuysCount(chatid) == 2


    @pytest.mark.parametrize("chatid, city, cityRus, orderData, parse_id", TEST_CREATE_ORDER_PK)
    def test_order_chatid(self, chatid, city, cityRus, orderData, parse_id):
        assert getChatid(parse_id) == chatid


    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_NEGATIVE_CHATID)
    def test_insert_negative_id(self, chatid, username):
        insert(chatid, username)

    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_LONG_USER)
    def test_insert_long_name(self, chatid, username):
        insert(chatid, username)

    @pytest.mark.parametrize("chatid, username", TEST_SELECT_NEW_VALUES)
    def test_select_new_chatid(self, chatid, username):
        assert True == IsNewClient(chatid), 'Excepting correct select by chatID'


    @pytest.mark.parametrize("chatid, username", TEST_SELECT_OLD_VALUES)
    def test_select_old_chatid(self, chatid, username):
        assert False == IsNewClient(chatid), 'Excepting correct select by chatID'

    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_SELECT_NEW_VALUES)
    def test_select_wrong_new_chatid(self, chatid, username):
        assert False == IsNewClient(chatid), 'Excepting correct select by chatID'

    @pytest.mark.xfail
    @pytest.mark.parametrize("chatid, username", TEST_INSERT_INCORRECT_FORMAT)
    def test_insert_incorrect(self, chatid, username):
        insert(chatid, username)


    @pytest.mark.parametrize("city, orderData", TEST_PARSE_ORDER)
    def test_create_parse_order(self, city, orderData):
        NewParseOrder(city, orderData)

    def test_is_more_parse_order(self):
        assert isMoreOrders() == True

    @pytest.mark.parametrize("parse_id", [1, 2])
    def test_check_parse_order_status(self, parse_id):
        getOrderStatus(parse_id) == False


