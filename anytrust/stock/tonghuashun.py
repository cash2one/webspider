import requests
from lxml import etree
import time
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import time
import json
import re



logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/tonghuashun.log',
                )
mysql = MySQLWrapper('db_finance_shares')


def parse_res(response):
    selector = etree.HTML(response.text)
    result = selector.xpath('/html/body/table/tbody/tr')
    for item in result:
        stock_name = item.xpath('td[2]/a/text()')[0]        #股票简称
        a_code = item.xpath('td[3]/a/text()')[0]            #股票代码a
        a_price = item.xpath('td[4]/text()')[0]             #A股价格
        a_rise = item.xpath('td[5]/text()')[0]              #A股涨跌幅
        b_code = item.xpath('td[6]/a/text()')[0]            #股票代码b
        b_price = item.xpath('td[7]/text()')[0]             #B股价格
        b_price_cny = item.xpath('td[8]/text()')[0]         #B股价格(CNY)
        b_rise = item.xpath('td[9]/text()')[0]              #B股涨跌幅
        ab_ratio = item.xpath('td[10]/text()')[0]          #AB股价格比
        stock_type = str(b_code)[0]
        create_time = int(time.time())

        select_sql = 'SELECT * FROM t_shares_ab_new WHERE f_code_a=%s'
        flag = mysql.fetchOne(select_sql,a_code)
        if flag:
            update_sql = 'UPDATE t_shares_ab_new SET f_name=%s,f_price_a=%s,f_rise_a=%s,f_code_b=%s,f_price_b=%s,f_price_b_cny=%s,'\
                        'f_rise_b=%s,f_ab=%s,f_type=%s,f_create_time=%s WHERE f_code_a=%s'
            mysql.execute(update_sql,stock_name,a_price,a_rise,b_code,b_price,b_price_cny,b_rise,ab_ratio,stock_type,create_time,a_code)
        else:
            insert_sql = 'INSERT INTO t_shares_ab_new(f_name,f_code_a,f_price_a,f_rise_a,f_code_b,f_price_b,f_price_b_cny,f_rise_b,f_ab,f_type,'\
                            'f_create_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,stock_name,a_code,a_price,a_rise,b_code,b_price,b_price_cny,b_rise,ab_ratio,stock_type,create_time)

        insert_sql_old = 'INSERT INTO t_shares_ab_old(f_name,f_code_a,f_price_a,f_rise_a,f_code_b,f_price_b,f_price_b_cny,f_rise_b,f_ab,f_type,'\
                            'f_create_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        mysql.execute(insert_sql_old,stock_name,a_code,a_price,a_rise,b_code,b_price,b_price_cny,b_rise,ab_ratio,stock_type,create_time)

if __name__ == '__main__':
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Referer': 'http://data.10jqka.com.cn/market/abgbj/',
        'X-Requested-With': 'XMLHttpRequest',
        'hexin-v': 'AueOA066cR9FwPWT6W7uKYFwdhC1bLn7FUY_nblUAQefiAnGwTxLniUQzxXK',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    }

    response = requests.get('http://data.10jqka.com.cn/market/abgbj/field/BL/order/desc/page/1/ajax/1/', headers=headers)
    parse_res(response)
    time.sleep(2)
    response = requests.get('http://data.10jqka.com.cn/market/abgbj/field/BL/order/desc/page/2/ajax/1/', headers=headers)
    parse_res(response)
