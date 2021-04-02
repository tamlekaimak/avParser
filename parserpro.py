
# тут будет код для парсера
# -*- coding: utf-8 -*-
import csv
import json
import time
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import cfscrape
import googleSheets


def get_session(proxy):
    session = requests.Session()
    if(proxy!=0):
        session.proxies.update(proxy)
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
    session = get_session(0)
    htmlbody = session.get(url)
    print(htmlbody.status_code)
    return htmlbody.text


def delete_symbol(str):
    return re.sub(r'[^0-9.]+', r'', str)  #удаляет ненужные символы с номера



def get_page_data(html,g_city,counter,proxies_list):
    api_sellerJson_1 = "https://m.avito.ru/api/14/items/"
    api_sellerJson_2 = "?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&action=view"
    api_phone_1 = "https://m.avito.ru/api/1/items/"
    api_phone_2 = "/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='iva-item-body-NPl6W')
    Data=pd.DataFrame(columns=['Заголовок','Цена','Описание','Имя_Продавца','Рейтинг','Дата','Телефон','Кол-во объяв','url',"Просмотры"])
    session=get_session({'http':'socks5://aibulatryic4445:bc6b63@176.119.142.202:10098',
                     'https':'socks5://aibulatryic4445:bc6b63@176.119.142.202:10098'
})
    for ad in ads:
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
            price = 'none'
        if(url!='none'):
            print(url[22:28])
            print('counter:',counter)
            id=url.split('_')[-1].split('?')[0]
            print(id)
            jsonfile = json.loads(session.get(
                'https://m.avito.ru/api/14/items/' + id + '?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&action=view').text)
            phone = json.loads(session.get(
                'https://m.avito.ru/api/1/items/' + id + '/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&action=view').text)
            try:
                print(jsonfile['code'])
                session = get_session({'http': 'socks5://aibulatryic4445:bc6b63@176.119.142.202:10098',
                                       'https': 'socks5://aibulatryic4445:bc6b63@176.119.142.202:10098'})
                print('была создана сессия в jsonfile')
            except:
                print('ok json')
                try:
                    print(phone['code'])
                    session=get_session()
                except:
                    print('all okay')
            try:
                if (phone['result']['action']['uri'].find('number') != -1):
                    phone = phone['result']['action']['uri'][-11:]
                elif (phone['result']['action']['uri'].find('authenticate') != -1):
                    phone = 'Необходима авторизация'
                else:
                    phone = 'Нет информации'
            except:
                phone = 'Нет информации'
            try:
                pages = jsonfile['seller']['summary'].split(' ')[0]
            except:
                pages = 'Нет информации'
            try:
                total=jsonfile["stats"]['views']['total']
            except:
                total='Нет информации'
            try:
                seller_rating = jsonfile["seller"]["rating"]["score"]
            except:
                seller_rating='Нет информации'
            try:
                seller_name = jsonfile["seller"]["name"]
            except:
                seller_name='Нет информации'
            try:
                description = jsonfile["description"]
            except:
                description='Нет информации'


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
    return Data,counter
def get_proxies_list():
    proxilist=[]
    with open('proxies.csv','r') as f:
        reader=csv.reader(f)
        for row in reader:
            try:
                session = get_session({"http": row[0].replace('\t', ''), "https": row[0].replace('\t', '')})
                soup = BeautifulSoup(session.get('https://2ip.ru').text, 'lxml')

                print(soup.find('div', class_='ip').find('span').text + ' is working')
                proxilist.append({"http": row[0].replace('\t', ''), "https": row[0].replace('\t', '')})
            except:
                print({"http":row[0].replace('\t',''),"https":row[0].replace('\t','')}, 'doesn\'t work')

    return proxilist

def all_pages_parser(pagesNumber,g_city,search,chat_id,filters,gmail):
    main_url = "https://www.avito.ru/"
    mainurl = main_url + g_city + "?"+"p=1&"
    print('Страниц:', pagesNumber)
    dopurl = "q=" + search.replace(' ', '+')
    counter=1;
    mainDF=pd.DataFrame(columns=['Заголовок','Цена','Описание','Имя_Продавца','Рейтинг','Дата','Телефон','Кол-во объяв','url',"Просмотры"])
    for i in range(pagesNumber):
        # Генерируем URL для функции get_page_data
        url_gen = mainurl[:len(mainurl)-2] +str(i)+'&'+ dopurl
        # Взять информацию из страницы
        page_df,counter=get_page_data(get_html(url_gen),g_city,counter=counter,proxies_list=get_proxies_list())
        mainDF=mainDF.append(page_df)
    for i in filters.keys():
        if(filters[i]==0):
            mainDF=mainDF.drop(i,axis=1)
    mainDF.to_excel('Объявления/' + search + str(chat_id) + '.xlsx', sheet_name='Объявления', index=False,
                    engine='openpyxl')
    mainDF.to_csv('Объявления/'+search+str(chat_id)+'.csv')
    if(gmail!=None):
        return search+str(chat_id),str(googleSheets.main(search+str(chat_id),gmail=gmail,df=mainDF))
    return search+str(chat_id)



def get_pages_number(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        pages = soup.find_all('span', class_='pagination-item-1WyVp')[-2].get('data-marker')
        p = pages.split('(')[1].split(')')[0]
    except:
        p = 1
    return p

def main(fromUserData):
    print(fromUserData)
    return all_pages_parser(g_city=fromUserData['parseBody']['city'],
                            search=fromUserData['parseBody']['value'],
                            chat_id=fromUserData['userInfo']['userID'],
                            pagesNumber=int(get_pages_number(get_html(
        "https://www.avito.ru/" + fromUserData['parseBody']['city'] + "?" + "q=" + fromUserData['parseBody']['value'].replace(' ', '+')
    ))),
                            filters=fromUserData['parseBody']['filters'],
                            gmail=fromUserData['parseBody']['google'])



if(__name__=="__main__"):
    main({'userInfo':{'userID':1},
          'parseBody':{'filters':{'Кол-во объяв':1,
                                  'Рейтинг':1,
                                  'Просмотры':1},
                       'city':'kazan',
                       'value':'acer predator gelios',
                       'google':'aibulat.ryic@gmail.com'},
          })

# >>>>>>> 9a6929b207372c3b501b52fe0dca4f5761164901
