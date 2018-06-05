import requests
from lxml import etree
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import time

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/weather_air.log',
                )
mysql = MySQLWrapper('db_spider')


def run():
    cookies = {
        'cityPy': 'beijing',
        'bdshare_firstime': '1525242341939',
        'Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2': '1525242342',
        'Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2': '1525242342',
    }

    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.baidu.com/link?url=U1VsbLFgNssEcMvnhnoeXnMEglCwmGMIYJG_82EhwyJdWoDYa44F_APf1-cv-dHq&wd=&eqid=dec5ca7b00010fe3000000025ae959de',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get('http://www.tianqi.com/air/', headers=headers, cookies=cookies)
    selector = etree.HTML(response.text)
    result = selector.xpath('/html/body/div[2]/div[3]/div/div[2]/ul/li[position()>1]')
    if not result:
        logging.error('request error')
        return

    insert_sql = 'INSERT INTO m_media_weather_air(f_No,f_City,f_Index,f_State)VALUES(%s,%s,%s,%s)'
    insert_sql_old = 'INSERT INTO m_media_weather_air_history(f_No,f_City,f_Index,f_State)VALUES(%s,%s,%s,%s)'
    select_sql = 'SELECT * FROM m_media_weather_air WHERE f_City=%s'
    update_sql = 'UPDATE m_media_weather_air SET f_No=%s,f_Index=%s,f_State=%s WHERE f_City=%s'
    for item in result:
        No = item.xpath('span[1]/text()')[0]
        city = item.xpath('span[2]/a/text()')[0]
        index = item.xpath('span[3]/text()')[0]
        state = item.xpath('span[4]/em/text()')[0]

        flag = mysql.fetchOne(select_sql,city)
        if flag:
            mysql.execute(update_sql,No,index,state,city)
        else:
            mysql.execute(insert_sql,No,city,index,state)

        mysql.execute(insert_sql_old,No,city,index,state)

if __name__ == '__main__':
    run()






