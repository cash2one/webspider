import requests
from lxml import etree
import time
import sys
sys.path.append("./settings")
from mysql import MySQLWrapper
import logging
import time
import json
import re


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://vip.stock.finance.sina.com.cn/q/go.php/vIR_SumRating/index.phtml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    }



logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='log/sina_long.log',
                )
mysql = MySQLWrapper('db_Stock_Holding')

def run():
    select_sql = 'SELECT f_organization_code FROM t_Organization_Attention'
    result = mysql.fetchAll(select_sql)
    code_list = []
    for item in result:
        a = str(item['f_organization_code'])
        if a[0]=='6':
            code_list.append('s_sh'+a)
        elif a[0] == '0' or a[0] == '3':
            code_list.append('s_sz'+a)
        if len(code_list) == 60:
            sina_stock_level_fast(code_list,'t_Organization_Attention')
            code_list = []
    if code_list:
        sina_stock_level_fast(code_list,'t_Organization_Attention')

    select_sql = 'SELECT distinct f_stock_code FROM t_Stock_Rate'
    result = mysql.fetchAll(select_sql)
    code_list = []
    for item in result:
        a = str(item['f_stock_code'])
        if a[0]=='6':
            code_list.append('s_sh'+a)
        elif a[0] == '0' or a[0] == '3':
            code_list.append('s_sz'+a)

        if len(code_list) == 60:
            sina_stock_level_fast(code_list,'t_Stock_Rate')
            code_list = []
    if code_list:
        sina_stock_level_fast(code_list,'t_Stock_Rate')

    


# 股票综合评级
def sina_stock_level_fast(code_list,database):
    code_list = ','.join(code_list)
    time.sleep(1)
    response = requests.get('http://hq.sinajs.cn/rn=152472708015936913793770697234&list='+code_list, headers=headers)
    result = re.findall(r'(\d+?=".+?)";',response.text)
    res = {}
    for item in result:
        a = item.split('=')
        b = a[1].split(',')
        res[a[0]]=[b[1],b[3]]
    for key,vlaue in res.items():
        if database =='t_Organization_Attention':
            update_mysql(key,vlaue)
        else:
            update_rate(key,vlaue)

def update_mysql(key,vlaue):
    update_sql = 'UPDATE t_Organization_Attention set f_latest_price=%s,f_price_limit=%s where f_organization_code=%s'
    mysql.execute(update_sql,vlaue[0],vlaue[1],key)


def update_rate(key,vlaue):
    update_sql = 'UPDATE t_Stock_Rate set f_latest_price=%s,f_price_limit=%s where f_stock_code=%s'
    mysql.execute(update_sql,vlaue[0],vlaue[1],key)




if __name__ =='__main__':
    while 1:
        time.sleep(60*2)
        run()



