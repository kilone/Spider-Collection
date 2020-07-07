from bs4 import BeautifulSoup as bs
import requests
import time
import random
import pymysql
import re


def get_url():
    connection = pymysql.connect(host='localhost', user='kilo', passwd='839211046', db='practice_database')
    cursor = connection.cursor()
    sql = 'select movie_name, user_url, user_name from movie_comments order by movie_name'
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.commit()
    connection.close()
    return data

def get_html(url):
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                   '73.0.3683.103 Safari/537.36'
               }
    cookies = {'cookie':
                   'bid=Fun3o0yy2oc; douban-fav-remind=1; viewed="5257905"; gr_user_id=65af1a05-e8bb-4b5e-a8eb-877'
                   'f699bf46b; _vwo_uuid_v2=D8EDE9087607920089BE2F47281FEC4A0|1d8c4341fd127e3a6d3b9af33dea13aa; '
                   'll="118178"; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1556168326%2C%22https%3A%2F%'
                   '2Fwww.douban.com%2Fsearch%3Fq%3D%25E5%25A4%258D%25E4%25BB%2587%25E8%2580%2585%25E8%2581%2594%2'
                   '5E7%259B%259F%22%5D; _pk_ses.100001.4cf6=*; __yadk_uid=VkIi7okhJW9XpphTrUS9F4pJn3kvvS6v; dbcl'
                   '2="195505411:ekSY77DMoMw"; ck=RcbX; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=53'
                   '6cef4996d2a1b5.1556168326.1.1556170175.1556168326.'
               }
    res = requests.get(url, headers=headers, cookies=cookies)
    return res

def parser_html(html):
    soup = bs(html.text, 'html.parser')
    contents = soup.find_all('div', class_='user-info')
    for content in contents:
        if content.find('a') == None:
            location = ''
        else:
            location = content.find('a').string
        sign_strings = list(content.find('div', class_='pl').strings)
        sign_time = sign_strings[-1][:-2]
    movie_info = soup.find_all('div', id='movie')
    for info in movie_info:
        if info.find('a', href=re.compile("do$")) == None:
            watching_num = None
        else:
            watching_num = info.find('a', href=re.compile("do$")).string[:-3]
        if info.find('a', href=re.compile("wish$")) == None:
            wish_num = None
        else:
            wish_num = info.find('a', href=re.compile("wish$")).string[:-3]
        if info.find('a', href=re.compile("collect$")) == None:
            collect_num = None
        else:
            collect_num = info.find('a', href=re.compile("collect$")).string[:-3]
    return location, sign_time, watching_num, wish_num, collect_num


while 1:
    data = get_url()
    for i in data:
        movie_name = i[0]
        url = i[1]
        user_name = i[2]
        html = get_html(url)
        information = parser_html(html)
        print(user_name)
        location = information[0]
        sign_time = information[1]
        watching_num = information[2]
        wish_num = information[3]
        collect_num = information[4]
        connection = pymysql.connect(host='localhost', user='kilo', passwd='839211046', db='practice_database')
        cursor = connection.cursor()
        sql = '''insert ignore into user_information(user_name, location, sign_time, watching_num, wish_num
                , collect_num, movie_name) values(%s, %s, %s, %s, %s, %s, %s)'''
        values = (user_name, location, sign_time, watching_num, wish_num, collect_num, movie_name)
        cursor.execute(sql,values)
        data = cursor.fetchall()
        cursor.close()
        connection.commit()
        connection.close()
        time.sleep(random.randint(1, 5))
