import time
from datetime import datetime
import ssl
from itertools import count
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


def crawling_pelicana():
    results = []

    for page in count(start=1):
        url = 'http://www.pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page

        html = crawler.crawling(url)
        print(f'{datetime.now()}: success for request [{url}]')

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        if len(tags_tr) == 0 :
            break
        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split(' ')[:2]

            t = (name, address) + tuple(sidogu)
            results.append(t)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    print(table)
    table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=True)

    for result in results:
        print(result)


def crawling_nene():
    check_end = ''
    results = []
    for page in count(1):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page

        html = crawler.crawling(url)
        print(f'{datetime.now()}: success for request [{url}]')

        bs = BeautifulSoup(html, 'html.parser')
        shop_divs = bs.findAll('div', attrs={'class': 'shop'})

        first_shop = shop_divs[0].text.replace('\n', ' ').strip().split(' ')[0]
        if first_shop == check_end:
            break

        check_end = first_shop

        for shop_div in shop_divs:
            name = shop_div.find('div', attrs={'class': 'shopName'}).text
            address = shop_div.find('div', attrs={'class': 'shopAdd'}).text
            sidogu = address.split(' ')[:2]

            t = (name, address) + tuple(sidogu)
            results.append(t)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/nene.csv', encoding='utf-8', mode='w', index=True)


def crawling_kyochon():
    results = []
    for sido1 in range(1, 18):
        for sido2 in count(1):
            url = 'http://www.kyochon.com/shop/domestic.asp?txtsearch=&sido1=%d&sido2=%d' % (sido1, sido2)
            html = crawler.crawling(url)

            if html is None:
                break;
            print(f'{datetime.now()}: success for request [{url}]')

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tag_spans = tag_ul.findAll('span', attrs={'class': 'store_item'})
            for tag_span in tag_spans:
                strings = list(tag_span.strings)
                name = strings[1]
                address = strings[3].strip('\r\n\t')
                sidogu = address.split(' ')[:2]

                results.append((name, address) + tuple(sidogu))
    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/kyochon.csv', encoding='utf-8', mode='w', index=True)


def crawling_goobne():
    results = []

    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('/Users/noah/cafe24/libs/selenium-chrome-driver/chromedriver')
    wd.get(url)
    time.sleep(3)

    for page in range(86, 87):
        # 자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()}: success for request [{script}]')
        time.sleep(3)

        # 실행 결과 동적으로 렌더링 된 HTML 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # detect last page
        if tags_tr[0].get('class') is None:
            break;

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split(' ')[:2]
            results.append((name, address) + tuple(sidogu))


    wd.quit()
    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)

if __name__ == '__main__':
    # 페리카나
    # crawling_pelicana()

    # 네네치킨은 과제
    crawling_nene()

    # 교촌치킨
    # crawling_kyochon()

    # 굽네치킨
    # crawling_goobne()