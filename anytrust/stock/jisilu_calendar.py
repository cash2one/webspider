import requests
import time
import os
if os.name == 'nt':
    setting_path = './settings'
    log_path = 'log/sina.log' 
else:
    setting_path = '/ROOT/www/spider/settings'
    log_path = '/ROOT/logs/sina.log'
import sys
sys.path.append(setting_path)
from mysql import MySQLWrapper
import logging
import calendar


logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename=log_path,
                )
mysql = MySQLWrapper('db_finance_shares')


def investment(qtype,start,end):
    cookies = {
        'event_newstock_apply': 'true',
        'event_CNV': 'true',
        'event_FUND': 'true',
        'event_BOND': 'true',
        'event_STOCK': 'true',
        'event_OTHER': 'true',
        'event_newbond_apply': 'true',
        'event_newbond_onlist': 'true',
        'event_diva': 'true',
        'event_divhk': 'true',
        'kbzw__Session': 'ibf3q59sn3imi46bbjpimtkjb3',
        'Hm_lvt_164fe01b1433a19b507595a43bf58262': '1525332209,1527818246',
        'kbz_newcookie': '1',
        'Hm_lpvt_164fe01b1433a19b507595a43bf58262': '1527842089',
    }
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.jisilu.cn/data/calendar/',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('qtype', TYPE_MAP[qtype]),
        ('start', start),
        ('end', end),
    )
    insert_sql = 'INSERT INTO t_kaishirili(`time`,`type`,`content`)VALUES(%s,%s,%s)'
    response = requests.get('https://www.jisilu.cn/data/calendar/get_calendar_data/', headers=headers, params=params, cookies=cookies)
    res = response.json()
    for item in res:
        title = item['title']
        start_date = item['start']
        _type = qtype

        mysql.execute(insert_sql,start_date,_type,title)
        







year = time.strftime('%Y',time.localtime(time.time()))
mounth = time.strftime('%m',time.localtime(time.time()))
date = calendar.monthrange(2015, 2)
if date[0]>5:
    a = date[1]-(date[0]-5)
last_day = year+'-'+mounth+'-'+str(a)

frist_day = year+'-'+mounth+'-'+'01'
a = time.strftime("%a",time.strptime(frist_day, '%Y-%m-%d'))
if a =='Sat':
    frist_day = year+'-'+mounth+'-'+'03'
elif a == 'Sun':
    frist_day = year+'-'+mounth+'-'+'02'

frist_day = int(time.mktime(time.strptime(frist_day, '%Y-%m-%d')))
last_day = int(time.mktime(time.strptime(last_day, '%Y-%m-%d')))

TYPE_MAP = {
    u'新股上市':'newstock_onlist',
    u'新股申购':'newstock_apply',
    u'可转债':'CNV',
    u'基金':'FUND',
    u'债券':'BOND',
    u'股票':'STOCK',
    u'其它':'OTHER',
    u'新债申购':'newbond_apply',
    u'新债上市':'newbond_onlist',
    u'A股分红':'diva',
    u'H股分红':'divhk',
}

for key in TYPE_MAP.keys():
    investment(key,frist_day,last_day)

