import requests
import pymysql


def get_data():
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 db='practice_database',
                                 user='kilo',
                                 password='839211046',
                                 charset='utf8')
    sql = "SELECT ip, port, type FROM free_ip LIMIT 20;"
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    free_ip = cursor.fetchall()
    return free_ip


def test_ip(free_ip):
    usable_ip = []
    useless_ip = []
    for i in free_ip:
        proxy = {}
        if i['type'] == 'HTTP':
            proxy['HTTP'] = i['ip'] + ':' + i['port']
        else:
            proxy['HTTPS'] = i['ip'] + ':' + i['port']
        print(proxy)
        try:
            res = requests.get(url, headers=headers, proxies=proxy, timeout=1)
            if res.status_code == 200:
                usable_ip.append(proxy)
        except Exception:
            print("测试不通过")
            useless_ip.append(proxy)
        else:
            print("测试通过")
    return usable_ip, useless_ip


url = "https://www.google.com/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54"}
free_ip = get_data()
print(free_ip)
test_ip(free_ip)
print(len(test_ip(free_ip)[0]))