from parserpro import get_session, get_html, delete_symbol, get_page_data
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import cfscrape
import pytest



MAIN_URL = "https://www.avito.ru/"
G_CITY = 'kazan'
search = 'Sasha'
MAIN_URl_NO_PAGES = MAIN_URL+G_CITY+"?"
DOP_URL_NO_PAGES = "q="+search.replace(' ', '+')
URL_GEN = MAIN_URl_NO_PAGES + DOP_URL_NO_PAGES

class TestParser:
    # @pytest.fixture(scope="function")
    # def resource_setup(request):
    #     driver = webdriver.Chrome(executable_path='C:\\chromedriver\\chromedriver.exe')
    #
    #     def resource_teardown():
    #         driver.quit()
    #
    #     request.addfinalizer(resource_teardown)
    #     return driver

    def test_get_html_status(self, url):
        assert get_html(url).status_code == 200, f"correct parameter value is 200 but getting {get_html().status_code} "

    def test_get_html_give_original_url(self, url):
        assert get_html(url).url == url, f"correct parameter value is {url} but getting {get_html().url}"

