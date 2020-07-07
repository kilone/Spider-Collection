from bs4 import BeautifulSoup as bs
import requests
import time
import random
import pymysql


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


def get_comment(html):
    movie_name = '复仇者联盟'
    connect = pymysql.connect(host='localhost', user='kilo', passwd='839211046', db='practice_database')
    cursor = connect.cursor()
    sql = """insert ignore into movie_comments(movie_name, user_name, watched, rating, rating_time, comment, 
    votes, user_url) values(%s, %s, %s, %s, %s, %s, %s, %s)"""
    soup = bs(html.text, 'html.parser')
    contents = soup.find_all('div', class_='comment')
    for content in contents:
        # 用户名
        name = content.find('a', class_='').string
        # 是否看过
        watched = content.find('span', class_=False).string
        # 评分
        if content.find('span', class_='rating') == None:
            rating = ''
        else:
            rating = content.find('span', class_='rating').get('title')
        # 评论时间
        comment_time = content.find('span', class_='comment-time').get('title')
        # 点赞数
        votes = content.find('span', class_='votes').string
        # 评论内容
        comment = content.find('span', class_='short').string
        # 用户链接
        user_url = content.find('a', class_='').get('href')
        values = (movie_name, name, watched, rating, comment_time, comment, votes, user_url)
        cursor.execute(sql, values)
    cursor.close()
    connect.commit()
    connect.close()


# def save_file(content_list):pe
#     with open('movie_comment.csv', 'w+',encoding='utf-8-sig',newline='') as f:
#         spamwriter = csv.writer(f, dialect='excel')
#         #spamwriter.writerow(['name', 'watched', 'rate', 'comment time', 'comment'])
#         for item in content_list:
#             spamwriter.writerow(item)

start = 0
while start < 25:
    url = 'https://movie.douban.com/subject/26100958/comments?start=' + str(start * 20) + \
          '&limit=20&sort=new_score&status=P'
    html = get_html(url)
    print("正在从第" + str(start + 1) + "页抓取评论")
    print(url)
    get_comment(html)
    time.sleep(random.randint(5, 10))
    start += 1
# save_file(content_list)