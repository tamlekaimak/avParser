<<<<<<< HEAD
=======

# тут будет код для парсера
# -*- coding: utf-8 -*-
import json
import time

>>>>>>> 0489e3fead170cd8c8cc0b8a983112fde1cc9fbc
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import cfscrape
import openpyxl


def get_session():
    session = requests.Session()
    session.headers = {
        'Host': 'www.avito.ru',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0)   Gecko/20100101 Firefox/69.0',
        'Accept': 'text/html,application/xhtm l+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru,en-US;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'}
    return cfscrape.create_scraper(sess=session)


def get_html(url):  # возвращает html код
    session = get_session()
    htmlbody = session.get(url)
    print(htmlbody.status_code)
    return htmlbody.text


def delete_symbol(str):
    return re.sub(r'[^0-9.]+', r'', str)  # удаляет ненужные символы с номера


<<<<<<< HEAD
def get_page_data(html, name_file, user_id):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='iva-item-body-NPl6W')
    date = ''
    Data = pd.DataFrame(columns=['title', 'price', 'date', 'url'])
=======
def get_page_data(html,g_city):
    isEnd=False
    api_sellerJson_1 = "https://m.avito.ru/api/14/items/"
    api_sellerJson_2 = "?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&action=view"
    api_phone_1 = "https://m.avito.ru/api/1/items/"
    api_phone_2 = "/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='iva-item-body-NPl6W')
    date=''
    pages = 'Нету информации'
    seller_rating = 'Нету информации'
    seller_name = 'Нету информации'
    description = 'Нету информации'
    phone='Нету информации'
    Data=pd.DataFrame(columns=['Заголовок','Цена','Описание','Имя_Продавца','Рейтинг','Дата','Телефон','Кол-во объяв','url',"Просмотры"])
    counter=1
    session = get_session()
>>>>>>> 0489e3fead170cd8c8cc0b8a983112fde1cc9fbc
    for ad in ads:
        if(counter%50==0):
            session=get_session()
            print('Подождите 30 секунд')
            time.sleep(30)
            counter=counter+1;
        try:
            url = 'https://www.avito.ru/' + ad.find('a').get('href').strip()
        except:
            url = 'none'
        try:
            title = ad.find('a').text.strip()
        except:
            title="none"
        try:
            pr = ad.find('span', class_='price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo').text.strip()
            price = delete_symbol(pr) + 'р.'
        except:
<<<<<<< HEAD
            price = ''
        try:
            url = 'https://www.avito.ru/' + ad.find('a').get('href').strip()
        except:
            url = ''
        try:
            date = ad.find('div',
                           class_="date-text-2jSvU text-text-1PdBw text-size-s-1PUdo text-color-noaccent-bzEdI").text.strip()
        except:
            date = ''
        Data = Data.append({'title': title,
                            'price': price,
                            'date': date,
                            'url': url, },
                           ignore_index=True)

    Data.to_csv('csv/'+name_file+user_id+".csv")
    return name_file


def main(g_city, search, user_id):
    main_url = "https://www.avito.ru/"
    mainurl_no_pages = main_url + g_city + "?"
    dopurl_no_pages = "q=" + search.replace(' ', '+')
    url_gen = mainurl_no_pages + dopurl_no_pages
    html = get_html(url_gen)
    page = get_page_data(html, search, user_id)
    print('Excel файл \'' + page + '.csv\' успешно создан! ')


if (__name__ == "__main__"):
    main("kazan", "Ильдан", '1')
=======
            price = 'none'
        if(url!='none'):
            print(url[22:28])
            counter = counter + 1;
            print('counter:',counter)
            id=url.split('_')[-1].split('?')[0]
            print(id)
            jsonfile=json.loads(session.get('https://m.avito.ru/api/14/items/'+id+'?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&action=view').text)
            try:
                jsonfile['code']
                error=True
            except:
                error=False
            print("Заблокирован:",error)
            try:
                total=jsonfile["stats"]['views']['total']
            except:
                total='Нету информации'
            try:
                seller_rating = jsonfile["seller"]["rating"]["score"]
            except:
                seller_rating='Нету информации'
            try:
                seller_name = jsonfile["seller"]["name"]
            except:
                seller_name='Нету информации'
            try:
                description = jsonfile["description"]
            except:
                description='Нету информации'
            try:
                pages=jsonfile['seller']['summary'].split(' ')[0]
            except:
                pages='Нету информации'
            try:
                phone=json.loads(session.get('https://m.avito.ru/api/1/items/'+id+'/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&action=view').text)
                print(phone)
                if(phone['result']['action']['uri'].find('number')!=-1):
                    phone=phone['result']['action']['uri'][-11:]
                elif(phone['result']['action']['uri'].find('authenticate')!=-1):
                    phone='Необходима авторизация'
                else:
                    phone='Нету информации'
            except: phone='Нету информации'
            try:
                date = ad.find('div',
                               class_="date-text-2jSvU text-text-1PdBw text-size-s-1PUdo text-color-noaccent-bzEdI").text.strip()
            except:
                date = 'none'
            Data=Data.append({
                            'Заголовок': title,
                            'Кол-во объяв':pages,
                            'Цена': price,
                            'Описание':description,
                            'Имя_Продавца':seller_name,
                            'Рейтинг':seller_rating,
                            'Дата': date,
                            'Просмотры':total,
                            'Телефон':phone,
                            'url': url, },
                            ignore_index=True)
    return Data

def all_pages_parser(pagesNumber,g_city,search,chat_id,filters):
    main_url = "https://www.avito.ru/"
    mainurl = main_url + g_city + "?"+"p=1&"
    print('Объявлений:', pagesNumber)
    dopurl = "q=" + search.replace(' ', '+')
    mainDF=pd.DataFrame(columns=['Заголовок','Цена','Описание','Имя_Продавца','Рейтинг','Дата','Телефон','Кол-во объяв','url',"Просмотры"])
    for i in range(1):
        # Генерируем URL для функции get_page_data
        url_gen = mainurl[:len(mainurl)-2] +str(i)+'&'+ dopurl
        # Взять информацию из страницы
        page_df=get_page_data(get_html(url_gen),g_city)
        mainDF=mainDF.append(page_df)
    for i in filters.keys():
        if(filters[i]):
            mainDF=mainDF.drop(i,axis=1)
    mainDF.to_excel('Объявления/'+search+chat_id+'.xlsx',sheet_name='Объявления',index=False,engine='openpyxl')

def get_pages_number(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        pages = soup.find_all('span', class_='pagination-item-1WyVp')[-2].get('data-marker')
        p = pages.split('(')[1].split(')')[0]
    except:
        p = 1
    return p

def main(g_city,search,user_id,isRating,isAdsNumber,isViews):
    filters={'Рейтинг':isRating,'Кол-во объяв':isAdsNumber,'Просмотры':isViews}
    all_pages_parser(g_city=g_city,search=search,chat_id=user_id,pagesNumber=int(get_pages_number(get_html(
        "https://www.avito.ru/" + g_city + "?" + "q=" + search.replace(' ', '+')
    ))),filters=filters)
    print('парсер закончил работу')


if(__name__=="__main__"):
    main("kazan","ноутбук",'1',1,1,1)

# >>>>>>> 9a6929b207372c3b501b52fe0dca4f5761164901
>>>>>>> 0489e3fead170cd8c8cc0b8a983112fde1cc9fbc
