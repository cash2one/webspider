import requests
from lxml import etree
import time
import os
if os.name == 'nt':
    setting_path = '../settings'
    log_path = 'sina.log' 
else:
    setting_path = '/ROOT/www/spider/settings'
    log_path = '/ROOT/logs/sina.log'
import sys
sys.path.append(setting_path)
from mysql import MySQLWrapper
import logging
import json
import re



logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename=log_path,
                )
mysql = MySQLWrapper('db_finance_shares')

cookies = {
    'UOR': 'www.baidu.com,tech.sina.com.cn,',
    'SINAGLOBAL': '124.65.127.142_1524019116.251870',
    'Apache': '124.65.127.142_1524019116.251872',
    'lxlrtst': '1524018574_o',
    'lxlrttp': '1524018574',
    'U_TRS1': '0000000e.9b596696.5ad6b174.e0ad695d',
    'U_TRS2': '0000000e.9b646696.5ad6b174.18fdc148',
    'ULV': '1524019575077:2:2:2:124.65.127.142_1524019116.251872:1524019119080',
    'FINANCE2': '83a6c35dc42b641f24ee430c69b8dd38',
    'FIN_ALL_VISITED': 'sh600078',
    'rotatecount': '1',
    'FINA_V_S_2': 'sh600078',
    'SR_SEL': '1_511',
}


headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml?p=2276',
}

# 限售解禁
def sina_stock_xsjj(page):

    params = (
        ('p', page),
        ('num', '60'),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/xsjj/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//*[@id="dataTable"]/tr')
    insert_sql = 'INSERT INTO t_shares_xsjj_copy(f_code,f_name,f_lift_date,f_lift_num,f_lift_price,f_batch,f_announcement_date,f_create_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in result:
        code = item.xpath('td[1]/a/text()')[0]   
        name = item.xpath('td[2]/a/text()')[0]                     
        lift_date = item.xpath('td[3]/text()')[0]                             
        lift_num = item.xpath('td[4]/text()')[0]                      
        lift_price = item.xpath('td[5]/text()')[0]                    
        batch = item.xpath('td[6]/text()')[0]            
        announcement_date = item.xpath('td[7]/text()')[0]            
        create_time = int(time.time())


        mysql.execute(insert_sql,code,name,lift_date,lift_num,lift_price,batch,announcement_date,create_time)

# 历史分红
def sina_stock_lsfh(page):

    params = (
        ('p', page),
        ('num', '60'),
    )


    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lsfh/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//*[@id="dataTable"]/tr')
    insert_sql = 'INSERT INTO t_shares_lsfh_copy(f_code,f_name,f_list_date,f_total_dividends,f_average_dividends,f_dividend_num,f_price,f_num,f_create_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in result:
        code = item.xpath('td[1]/a/text()')[0]   
        name = item.xpath('td[2]/a/text()')[0]                     
        lift_date = item.xpath('td[3]/text()')[0]                             
        total_dividends = item.xpath('td[4]/text()')[0]                      
        average_dividends = item.xpath('td[5]/text()')[0]                    
        dividend_num = item.xpath('td[6]/text()')[0]            
        price = item.xpath('td[7]/text()')[0]
        num = item.xpath('td[8]/text()')[0]          
        create_time = int(time.time())


        mysql.execute(insert_sql,code,name,lift_date,total_dividends,average_dividends,dividend_num,price,num,create_time)

# 交易提示
def sina_stock_jyts():
    today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    params = (
        ('tradedate', today),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/jyts/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//table[@class="list_div"]/tr')
    select_sql = 'SELECT f_id from t_shares_jyts_event where f_event=%s'
    insert_event_sql = 'INSERT INTO t_shares_jyts_event(f_event)VALUES(%s)'
    insert_sql = 'INSERT INTO t_shares_jyts(f_event_id,f_event_body,f_create_time)VALUES(%s,%s,%s)'
    res = {}
    for item in result:
        if item.xpath('td[1]/span/text()'):
            event = item.xpath('td[1]/span/text()')[0]
            res[event]=[]
        else:
            content = ' '.join(item.xpath('td[1]//text()'))
            res[event].append(content)


    for key in res.keys():
        event_id = mysql.fetchOne(select_sql,key)
        if not event_id:
            mysql.execute(insert_event_sql,key)
        event_id = mysql.fetchOne(select_sql,key)
        content = '\n'.join(res[key])
        create_time = int(time.time())
        mysql.execute(insert_sql,event_id['f_id'],content,create_time)

# 融资融券
def sina_stock_rzrq():

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml', headers=headers, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//*[@id="dataTable"]')
    table1 = result[0].xpath('tr[position()>2]')
    insert_sql = 'INSERT INTO t_shares_rzrq_total(f_market,f_day_balance,f_day_buy,f_day_repay,f_day_total,f_create_time)VALUES(%s,%s,%s,%s,%s,%s)'
    for item in table1:
        market = item.xpath('td[1]/text()')[0]
        day_balance = item.xpath('td[2]/text()')[0]
        day_buy = item.xpath('td[3]/text()')[0]
        day_repay = item.xpath('td[4]/text()')[0]
        day_total = item.xpath('td[4]/text()')[0]
        create_time = int(time.time())

        mysql.execute(insert_sql,market,day_balance,day_buy,day_repay,day_total,create_time)

    table2 = result[1].xpath('tr[position()>3]')
    insert_sql = 'INSERT INTO t_shares_rzrq_detail(f_code,f_name,f_balance_long,f_buy_long,f_repay_long,f_margin_price_short,f_margin_short,f_pay_short,f_repay_num_short,f_securities_balance_short,f_create_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in table2:
        code = item.xpath('td[2]/a/text()')[0]
        name = item.xpath('td[3]/a/text()')[0]
        balance_long = item.xpath('td[4]/text()')[0]
        buy_long = item.xpath('td[5]/text()')[0]
        repay_long = item.xpath('td[6]/text()')[0]
        margin_price_short = item.xpath('td[7]/text()')[0]
        margin_short = item.xpath('td[8]/text()')[0]
        pay_short = item.xpath('td[9]/text()')[0]
        repay_num_short = item.xpath('td[10]/text()')[0]
        securities_balance_short = item.xpath('td[11]/text()')[0]
        create_time = int(time.time())

        mysql.execute(insert_sql,code,name,balance_long,buy_long,repay_long,margin_price_short,margin_short,pay_short,repay_num_short,securities_balance_short,create_time)

# 大宗交易
def Block_trade(page):
    
    params = (
        ('p', page),
        ('num', '60'),
    )
    today = int(time.strftime("%Y%m%d", time.localtime(time.time()-24*60*60)))
    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK', 'ignore'))
    result = selector.xpath('//div[@id="divContainer"]/table/tr')
    insert_sql = 'INSERT INTO t_shares_large_trans(f_date,f_code,f_name,f_price,f_num,f_total_price,f_buyer_name,f_seller_name,f_type,f_create_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in result:
        f_date = item.xpath('td[1]/text()')[0]
        a = int(f_date.replace('-',''))
        if today != a:
            return
        f_code = item.xpath('td[2]/a/text()')[0]
        f_name = item.xpath('td[3]/a/text()')[0]
        f_price = item.xpath('td[4]/text()')[0]
        f_num = item.xpath('td[5]/text()')[0]
        f_total_price = item.xpath('td[6]/text()')[0]
        f_buyer_name = item.xpath('td[7]/text()')[0]
        f_seller_name = item.xpath('td[8]/text()')[0]
        f_type = item.xpath('td[9]/text()')[0]
        create_time = int(time.time())

        

        mysql.execute(insert_sql,f_date,f_code,f_name,f_price,f_num,f_total_price,f_buyer_name,f_seller_name,f_type,create_time)
        

# 内部交易
def Internal_trade(page):

    params = (
        ('p', page),
    )

    today = int(time.strftime("%Y%m%d", time.localtime(time.time()-24*60*60)))
    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/nbjy/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK', 'ignore'))
    result = selector.xpath('//div[@id="divContainer"]/table/tr')
    insert_sql = 'INSERT INTO t_shares_inside_trans(f_code,f_name,f_user,f_type,f_change_num,f_average_trans_price,f_change_price,f_after_num,f_change_reason,f_change_data,f_holding_type,f_relationship,f_post,f_create_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in result:
        f_change_data = item.xpath('td[10]/text()')[0]
        a = int(f_change_data.replace('-',''))
        if today != a:
            return
        f_code = item.xpath('td[1]/a/text()')[0]
        f_name = item.xpath('td[2]/a/text()')[0]
        f_user = item.xpath('td[3]/text()')[0]
        f_type = item.xpath('td[4]//text()')[0].strip()
        f_change_num = item.xpath('td[5]//text()')[0].strip()
        f_average_trans_price = item.xpath('td[6]/text()')[0].strip()
        f_change_price = item.xpath('td[7]/text()')[0]
        f_after_num = item.xpath('td[8]/text()')[0].strip()
        if item.xpath('td[9]/text()'):
            f_change_reason = item.xpath('td[9]/text()')[0]
        else:
            f_change_reason = ''
        f_holding_type = item.xpath('td[11]/text()')[0]
        f_relationship = item.xpath('td[12]/text()')[0]
        f_post = item.xpath('td[13]/text()')[0]
        create_time = int(time.time())
        
        mysql.execute(insert_sql,f_code,f_name,f_user,f_type,f_change_num,f_average_trans_price,f_change_price,f_after_num,f_change_reason,f_change_data,f_holding_type,f_relationship,f_post,create_time)
        

    
if __name__ =='__main__':
    # 限售解禁 5页
    b = 'TRUNCATE TABLE t_shares_xsjj_copy'
    mysql.execute(b)
    
    for i in range(1,6):
        time.sleep(6)
        sina_stock_xsjj(str(i))

    b = 'TRUNCATE TABLE t_shares_xsjj'
    mysql.execute(b)
    a = 'INSERT INTO t_shares_xsjj SELECT * FROM t_shares_xsjj_copy'
    mysql.execute(a)

    # 历史分红 59页
    b = 'TRUNCATE TABLE t_shares_lsfh_copy'
    mysql.execute(b)
    
    for i in range(1,60):
        time.sleep(6)
        sina_stock_lsfh(str(i))

    b = 'TRUNCATE TABLE t_shares_lsfh'
    mysql.execute(b)
    a = 'INSERT INTO t_shares_lsfh SELECT * FROM t_shares_lsfh_copy'
    mysql.execute(a)
    sina_stock_jyts()
    sina_stock_rzrq()
    ##################################大众交易

    for i in range(1,3):
        time.sleep(6)
        Block_trade(str(i))

    #####################################################内部交易

    for i in range(1,3):
        time.sleep(6)
        Internal_trade(str(i))


