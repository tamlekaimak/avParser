from parserpro import get_session, get_html, delete_symbol, get_page_data
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
        search = 'Sasha'
        MAIN_URl_NO_PAGES = MAIN_URL + G_CITY + "?"
        DOP_URL_NO_PAGES = "q=" + search.replace(' ', '+')
        URL_GEN = MAIN_URl_NO_PAGES + DOP_URL_NO_PAGES
        return URL_GEN


    def test_get_html_status(self, url):
        assert get_html(url).status_code == 100, f"correct parameter value is 200 but getting {get_html().status_code} "

    def test_get_html_give_original_url(self, url):
        assert get_html(url).url == 'asd', f"correct parameter value is {url} but getting {get_html().url}"

