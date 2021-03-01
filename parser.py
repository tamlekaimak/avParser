import requests
from bs4 import BeautifulSoup
import csv
import re
import time
from requests.exceptions import ProxyError, ReadTimeout, SSLError, ConnectionError
import cfscrape

from city import cities


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
    r = session.get(url)
    print(r.status_code)
    return r.text


def get_total_pages(html):  # возвращает количество страниц, чтобы потом запустить цикл и считать по каждой странице
    soup = BeautifulSoup(html, 'lxml')
    try:
        pages = soup.find_all('span', class_='pagination-item-1WyVp')[-2].get('data-marker')
        p = pages.split('(')[1].split(')')[0]
    except:
        p = 1
    return int(p)


def delete_symbol(str):
    return re.sub(r'[^0-9.]+', r'', str)  # удаляет ненужные символы с номера


def get_page_data(html, name_file, user_id):
    session = get_session()
    q = 1
    api_view = "https://m.avito.ru/api/14/items/"
    api_view2 = "?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&action=view"
    api_nomer = "https://m.avito.ru/api/1/items/"
    api_nomer2 = "/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='iva-item-body-NPl6W')
    for ad in ads:
        # title,price,place,nomer,opisanie
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
            data = ad.find('div',
                           class_="date-text-2jSvU text-text-1PdBw text-size-s-1PUdo text-color-noaccent-bzEdI").text.strip()
        except:
            data = ''
        if (q % 200 == 0):
            session = get_session()
            time.sleep(30)
            print(q)
        else:
            lenght_url = len(url)
            private_number = url[lenght_url - 10:lenght_url]
            ##############################################имя
            link_view = api_view + private_number + api_view2
            response1 = session.get(link_view)
            if (response1.status_code) == 200:
                name = response1.text[response1.text.find("name") + 7:response1.text.find("name") + 37]
                ind = name.find(",") - 1
                name = " " + name[:ind]
                #####описание
                ind1 = response1.text.find("description") + 14
                ind2 = response1.text.find("advertOptions") - 3
                opisanie = " " + response1.text[ind1:ind2]
                ############
                try:
                    ind_ob = response1.text.find("summary") + 10
                except:
                    ind_ob = 1
                count_ob = response1.text[ind_ob:ind_ob + 3]
            else:
                name = "имя отсутсвует"
                opisanie = " отсутствует"
            #####номер
            link_nomer = api_nomer + private_number + api_nomer2
            response = session.get(link_nomer)
            ###########запись в документ
            index = response.text.find("number") + 10
            nomer = " " + response.text[index:index + 11]
            print(nomer[1])
            if nomer[1] == '"' or nomer[1] == ':' or nomer[1] == '{':
                print(nomer[0])
                nomer = "номер отсутствует"
            data = {'title': title,
                    'price': price,
                    'data': data,
                    'nomer': nomer,
                    'name': name,
                    'url': url,
                    'opisanie': opisanie,
                    'count_ob': count_ob}
            write_csv(data, name_file, user_id)
        q = q + 1
    return name_file


def write_csv(data, name_file, user_id):  # запись в файл
    with open(str(name_file) + user_id + '_' + '.csv', 'a', encoding="cp1251", newline='', errors='replace') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow((data['title'],
                         data['price'],
                         data['data'],
                         data['nomer'],
                         data['name'],
                         data['url'],
                         data['opisanie'],
                         data['count_ob']))


def paste_total(url, name_file, user_id):  # запись таблицы
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
            'name_razdel': name_razdel
            }
    try:
        write_csv(data, name_file, user_id)
    except:
        print("(((")


def main(g_city, search, user_id):
    print("Yo")
    main_url = "https://www.avito.ru/"
    path = main_url + g_city + "?q=" + search.replace(' ', '+')
    total_pages = get_total_pages(get_html(path))  # обращается к функции которая считает количество страниц
    print("obshee kol-vo pages")
    print(total_pages)
    mainurl = "https://www.avito.ru/" + g_city + "?p="
    mainurl_no_pages = "https://www.avito.ru/" + g_city + "?"
    dopurl = "&" + "q=" + search.replace(' ', '+')
    dopurl_no_pages = "q=" + search.replace(' ', '+')
    if (total_pages > 6):
        total_pages = 5
    # for i in range(1, total_pages + 1):
    # for i in range(1,2):
    #    if(i==1):
    #        url_gen = mainurl_no_pages+dopurl_no_pages
    #    else: url_gen=mainurl+str(i)+dopurl
    #    print(url_gen)
    #    html = get_html(url_gen)
    #    page = get_page_data(html,search)
    url_gen = mainurl_no_pages + dopurl_no_pages
    html = get_html(url_gen)
    page = get_page_data(html, search, user_id)
    paste_total(path, search, user_id)
    print('Excel файл \'' + page + '.csv\' успешно создан! ')

if( __name__ == "__main__"):
    print("hello")
    main("kazan","Велосипеды","1")