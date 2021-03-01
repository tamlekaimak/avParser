<<<<<<< HEAD
print("Yaho");
=======
# тут будет код для парсера
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import re
from unidecode import unidecode
import time
from requests.exceptions import ProxyError, ReadTimeout, SSLError, ConnectionError
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
    r = session.get(url)
    print(r.status_code)
    return r.text


def delete_symbol(str):
    return re.sub(r'[^0-9.]+', r'', str)#удаляет ненужные символы с номера



def get_page_data(html,name_file,user_id): 
    session = get_session()
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='iva-item-body-NPl6W')
    for ad in ads:
        #title,price,place,nomer,opisanie
        print(q)
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
            data = ad.find('div',class_="date-text-2jSvU text-text-1PdBw text-size-s-1PUdo text-color-noaccent-bzEdI").text.strip()
        except:
            data = ''
        data = {'title':title,
                'price':price,
                'data':data,
                'url':url}
        write_csv(data, name_file,user_id)
        q=q+1
    return name_file



def write_csv(data, name_file,user_id ):#запись в файл
    with open(str(name_file) +user_id+'_'+'.csv','a', encoding="cp1251", newline='',errors='replace') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow((data['title'],
                         data['price'],
                         data['data'],
                         data['url']))



def paste_total(url, name_file,user_id):#запись таблицы
    soup = BeautifulSoup(url, 'lxml') 
    try:
        total = soup.find('span', class_='page-title-count-1oJOc').text
    except:
        total = 0
    try:        
        name_razdel = soup.find('h1', class_='page-title-inline-2v2CW').text.strip()
    except:
        name_razdel = ''    
    data = {'total': total,
            'name_razdel':name_razdel
           }
    try:
        write_shapka_csv(data,name_file,user_id)
    except: print("(((")
    
def main(g_city,search,user_id):
    main_url="https://www.avito.ru/"
    path=main_url+g_city+"?q="+search.replace(' ','+')
    mainurl_no_pages=main_url+g_city+"?"
    dopurl="&"+"q="+search.replace(' ', '+')
    dopurl_no_pages="q="+search.replace(' ', '+')
    url_gen = mainurl_no_pages+dopurl_no_pages
    html = get_html(url_gen)
    page = get_page_data(html,search,user_id)
    paste_total(path, search,user_id)
    print('Excel файл \'' + page + '.csv\' успешно создан! ')




>>>>>>> 9a6929b207372c3b501b52fe0dca4f5761164901
