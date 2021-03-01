
# тут будет код для парсера
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import cfscrape


def get_session():
    session = requests.Session()
    session.headers = {
        'Host':'www.avito.ru',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0)   Gecko/20100101 Firefox/69.0',
        'Accept':'text/html,application/xhtm l+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'ru,en-US;q=0.5',
        'Accept-Encoding':'gzip, deflate, br',
        'DNT':'1',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache'}
    return cfscrape.create_scraper(sess=session)

def get_html(url):#возвращает html код
    session = get_session()
    htmlbody = session.get(url)
    print(htmlbody.status_code)
    return htmlbody.text


def delete_symbol(str):
    return re.sub(r'[^0-9.]+', r'', str)#удаляет ненужные символы с номера



def get_page_data(html,name_file,user_id):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='iva-item-body-NPl6W')
    date=''
    Data=pd.DataFrame(columns=['title','price','date','url'])
    for ad in ads:
        try:
            title = ad.find('a').text.strip()
        except:
            title = ''
        try:
            pr = ad.find('span', class_='price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo').text.strip()
            price = delete_symbol(pr) + 'р.'
        except:
            price = ''    
        try:
            url = 'https://www.avito.ru/' + ad.find('a').get('href').strip()
        except:
            url = '' 
        try:
            date = ad.find('div', class_="date-text-2jSvU text-text-1PdBw text-size-s-1PUdo text-color-noaccent-bzEdI").text.strip()
        except:
            date=''
        Data=Data.append({'title': title,
                    'price': price,
                    'date': date,
                    'url': url, },
                        ignore_index=True)

    Data.to_csv('Объявления/'+name_file+"__"+user_id+".csv",encoding="cp1251",)
    return name_file
    
def main(g_city,search,user_id):
    main_url = "https://www.avito.ru/"
    mainurl_no_pages = main_url+g_city+"?"
    dopurl_no_pages = "q="+search.replace(' ', '+')
    url_gen = mainurl_no_pages+dopurl_no_pages
    html = get_html(url_gen)
    page = get_page_data(html,search,user_id)
    print('Excel файл \'' + page + '.csv\' успешно создан! ')


if(__name__=="__main__"):
    main("kazan","Ильдан",'1')

# >>>>>>> 9a6929b207372c3b501b52fe0dca4f5761164901
