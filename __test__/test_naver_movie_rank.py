from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from collection import crawler


def ex01():
    request = Request('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
    response = urlopen(request)
    html = response.read().decode('cp949')

    # print(html)
    bs = BeautifulSoup(html, 'html.parser')
    divs = bs.findAll('div', attrs={'class': 'tit3'})

    for index, div in enumerate(divs):
        print(index+1, div.a.text, div.a['href'], sep=':')

    print('==========================================')



def proc_naver_movie_rank(html):

    # processing
    bs = BeautifulSoup(html, 'html.parser')
    result = bs.findAll('div', attrs={'class': 'tit3'})
    return result


def store_naver_movie_rank(data):

    # output
    for index, div in enumerate(data):
        print(index + 1, div.a.text, div.a['href'], sep=':')


def ex02():

    # fetch
    crawler.crawling(
        url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn',
        encoding='cp949',
        proc1=proc_naver_movie_rank,
        proc2=lambda data: list(map(lambda div: print(div.a.text, div.a['href'], sep=':'), data))
    )



__name__ == '__main__' and not \
    ex01() and not \
    ex02()


