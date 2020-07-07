import requests
from lxml.html import etree
import pymysql
import time


def get_ip_info(page):
    url = f"http://www.ip3366.net/free/?stype=1&page={page}"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54"}
    res = requests.get(url, headers=header, timeout=3)
    html = etree.HTML(res.content)
    ip_text = html.xpath('//*[@id="list"]/table/tbody/tr')
    ip_list = []
    for tr in ip_text:
        ip_info = {}
        # print(tr.xpath('./td[1]/text()'))
        ip_info['ip'] = tr.xpath('./td[1]/text()')[0]
        ip_info['port'] = tr.xpath('./td[2]/text()')[0]
        ip_info['anonymity'] = tr.xpath('./td[3]/text()')[0]
        ip_info['type'] = tr.xpath('./td[4]/text()')[0]
        ip_info['address'] = tr.xpath('./td[5]/text()')[0]
        ip_info['responding_speed'] = tr.xpath('./td[6]/text()')[0]
        ip_info['last_verification_time'] = tr.xpath('./td[7]/text()')[0]
        ip_list.append(ip_info)
    return ip_list


def save_to_database(ip_list):
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 db='practice_database',
                                 user='kilo',
                                 password='839211046',
                                 charset='utf8')
    sql = "INSERT ignore INTO free_ip(ip,port,anonymity,type,address,responding_speed,last_verification_time) VALUES\
        (%s,%s,%s,%s,%s,%s,%s)"
    for i in ip_list:
        connection.cursor().execute(sql, (i['ip'], i['port'], i['anonymity'], i['type'], i['address'],\
                                          i['responding_speed'], i['last_verification_time']))
        connection.commit()
    connection.close()


def run(page):
    print(f"开始爬取第{page}页")
    ip_list = get_ip_info(page)
    print(f"第{page}页爬取完成")
    save_to_database(ip_list)
    print(f"第{page}页存储完成")
    print("等待5秒钟")


page_num = 8
for page in range(1, page_num):
    run(page)
    time.sleep(5)
# db_settings = {
#     'host': 'localhost',
#     'port': 3306,
#     'db': 'practice_database',
#     'user': 'kilo',
#     'password': '839211046',
#     'charset': 'utf8'
#     }

