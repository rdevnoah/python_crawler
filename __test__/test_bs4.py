from bs4 import BeautifulSoup

html = '''<td class="title black">
            <div class="tit3" id="my-div">
                <a href="/movie/bi/mi/basic.nhn?code=161967" title="기생충">기생충</a>
            </div>
       </td>'''

# print(html)


# 1. tag 조회
def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    # print(type(bs), bs)
    tag = bs.td
    # print(type(tag), tag)
    tag = bs.a
    # print(tag)
    tag = bs.td.div
    print(tag)


# 2. 속성값(attribute) 가져오기
def ex2():
    bs = BeautifulSoup(html, 'html.parser')
    tag = bs.td
    print(tag['class'])

    tag = bs.div
    # 에러
    # print(t['id'])
    print(tag.attrs)


# 3. attribute로 태그 조회하기
def ex3():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.find('td', attrs={'class': 'title'})
    # print(tag)
    tag = bs.find(attrs={'class': 'title'})
    print(tag)


if __name__ == '__main__':
    # ex1()
    # ex2()
    ex3()
