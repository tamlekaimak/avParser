from parserpro import *
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import cfscrape
import pytest



class TestParser:
    @pytest.fixture(scope="function")
    def url(self):
        MAIN_URL = "https://www.avito.ru/"
        G_CITY = 'kazan'
        search = 'Терменвокс'
        MAIN_URl_NO_PAGES = MAIN_URL + G_CITY + "?"
        DOP_URL_NO_PAGES = "q=" + search.replace(' ', '+')
        URL_GEN = MAIN_URl_NO_PAGES + DOP_URL_NO_PAGES
        return URL_GEN

    @pytest.mark.skip
    def test_get_html_status(self, url):
        assert get_html(url).status_code == 100, f"correct parameter value is 200 but getting {get_html().status_code} "

    @pytest.mark.skip
    def test_get_html_give_original_url(self, url):
        assert get_html(url).url == 'asd', f"correct parameterq value is {url} but getting {get_html().url}"


    def test_pages_num_for_Termenvoks(self,url):
        assert 1 == int(get_pages_number(get_html(
            "https://www.avito.ru/" + 'kazan' + "?" + "q=" + 'Терменвокс'.replace(' ', '+')
        )))

    def test_pages_num_for_Balalika(self,url):
        assert 11 == int(get_pages_number(get_html(
            "https://www.avito.ru/" + 'kazan' + "?" + "q=" + 'Балалайка'.replace(' ', '+')
        )))

    def test_Data_created(self,url):
        html = get_html(url)
        data, counter = get_page_data(html, 'kazan', 0)
        assert all(i in ['Заголовок','Цена','Описание','Имя_Продавца','Рейтинг','Дата','Телефон','Кол-во объяв','url',"Просмотры"] for i in data.columns )