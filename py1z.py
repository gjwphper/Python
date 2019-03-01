import requests
import time
import pymysql.cursors
from bs4 import BeautifulSoup

def download_page(url):
    headers = {
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding": "gzip, deflate",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        # "Connection": "keep-alive",
        # "Cookie": "UM_distinctid=167c90556c47e-0fe92116796226-58432916-1fa400-167c90556c6fc; jxnewsbbs_b3c3_saltkey=jt6EidTp; jxnewsbbs_b3c3_lastvisit=1550704553; insert_cookie=76891161; CNZZDATA30059797=cnzz_eid%3D125691490-1545264890-http%253A%252F%252Fbbs.jxnews.com.cn%252F%26ntime%3D1550815237; CNZZDATA30059789=cnzz_eid%3D1359613091-1545262069-http%253A%252F%252Fbbs.jxnews.com.cn%252F%26ntime%3D1550816829; Hm_lvt_dde6ba2851f3db0ddc415ce0f895822e=1550708436,1550708451,1550817505; jxnewsbbs_b3c3_st_t=0%7C1550818269%7C5b3c51eb37459c8fd348fd28781aebc6; jxnewsbbs_b3c3_forum_lastvisit=D_716_1550708407D_724_1550708425D_703_1550817203D_711_1550818269; jxnewsbbs_b3c3_st_p=0%7C1550820165%7C967f9a7192151c8ba49a72c93504147f; jxnewsbbs_b3c3_visitedfid=298D711D724D716; jxnewsbbs_b3c3_viewid=tid_3160338; jxnewsbbs_b3c3_lastact=1550820166%09home.php%09misc; jxnewsbbs_b3c3_sendmail=1; Hm_lpvt_dde6ba2851f3db0ddc415ce0f895822e=1550820551; td_cookie=18446744073526191933",
        # "Host": "bbs.jxnews.com.cn",
        # "Referer": "http://bbs.jxnews.com.cn/forum-711-1.html",
        # "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    ee = r.text
    return r.text

def get_content(html,page,conn):
    soup = BeautifulSoup(html, 'html.parser')
    con_list = soup.find_all('a',class_='xst')
    for i in con_list:
        print('----outer-----{}'.format(page))
        title = i.string
        info = (title,title)
        insert(conn,info)




def insert(conn, info):
    '''数据写入数据库'''
    with conn.cursor() as cursor:
        sql = "INSERT INTO `py1z` (`title`,`content`) VALUES (%s, %s)"
        cursor.execute(sql, info)
    conn.commit()

def get_conn():
    '''建立数据库连接'''
    conn = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='spider_py1z',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return conn


def main():
    conn = get_conn()
    for i in range(1,21):
        url = 'http://bbs.jxnews.com.cn/forum-711-{}.html'.format(i)

        html = download_page(url)
        get_content(html,i,conn)
        time.sleep(5)  # 休息一下，不要给网站太大压力，避免被封


if __name__ == '__main__':
    main()
