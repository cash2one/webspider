import requests
from lxml import etree
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import time
import json
import re

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
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml?p=2276',
}


logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/sina_finance.log',
                )
mysql = MySQLWrapper('db_Stock_Holding')


# 机构持股汇总
def sina_stock_department(page):

    params = (
        ('p', page),
    )
    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml',params=params, headers=headers, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//*[@id="dataTable"]/tr')
    selecet_sql = 'SELECT * from t_Share_Holding where f_share_code=%s'
    insert_sql = 'INSERT INTO t_Share_Holding(f_year,f_month,f_share_name,f_share_code,f_num,f_num_balance,f_stock_percent,f_stock_percent_balance,f_current_stock_percent,f_current_percent_balance)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    f_year = u'2018年'
    f_month = u'一季报'
    for item in result[::2]:
        share_code = item.xpath('td[1]/a/text()')[0]                     #证券代码
        share_name = item.xpath('td[2]/a/text()')[0]                     #证券简称
        num = item.xpath('td[3]/text()')[0]                              #机构数
        num_balance = item.xpath('td[4]/text()')[0]                      #机构数变化
        stock_percent = item.xpath('td[5]/text()')[0]                    #持股比例(%)
        stock_percent_balance = item.xpath('td[6]/text()')[0]            #持股比例增幅(%) 
        current_stock_percent = item.xpath('td[7]/text()')[0]            #占流通股比例(%)
        current_percent_balance = item.xpath('td[8]/text()')[0]          #占流通股比例增幅(%)


        flag = mysql.fetchOne(selecet_sql,share_code)
        if not flag:
            mysql.execute(insert_sql,f_year,f_month,share_name,share_code,num,num_balance,stock_percent,stock_percent_balance,current_stock_percent,current_percent_balance)


def sina_stock_department_moreinfo():
    params = (
        ('symbol', '300639'),
        ('quarter', '20181'),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/api/jsonp.php/var%20details=/ComStockHoldService.getJGCGDetail', headers=headers, params=params, cookies=cookies)
    res = re.findall(r'\(\((.+?)\)',response.text)[0]
    res = res.replace(':','":').replace('{','{"').replace(',',',"')
    res = json.loads(res)
    print(res)
    for key in res['data']['fund']:        
        if key == 'total' and res['data']['fund']['total']:
            print(res['data']['fund']['total']['totalAmount'])
            print(res['data']['fund']['total']['totalStockPercent'])
            print(res['data']['fund']['total']['totalCurrentPercent'])
            print(res['data']['fund']['total']['totalPercentBalance'])
            print(res['data']['fund']['total']['totalCurrentBalance'])
        elif res['data']['fund']['total']:
            print(res['data']['fund'][key]['orgCode'])
            print(res['data']['fund'][key]['orgName'])
            print(res['data']['fund'][key]['orgFullName'])
            print(res['data']['fund'][key]['stockAmount'])
            print(res['data']['fund'][key]['stockAmountLast'])
            print(res['data']['fund'][key]['currentPercent'])
            print(res['data']['fund'][key]['lastCurrentPercent'])
            print(res['data']['fund'][key]['stockPercentBalance'])
            print(res['data']['fund'][key]['currentPercentBalance'])
        else:
            print('300639')

# 基金重仓股
def sina_awkwardness(page):
    params = (
        ('p', page),
    )
    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jjzc/index.phtml',params=params, headers=headers, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//*[@id="dataTable"]/tr')
    selecet_sql = 'SELECT * from t_Fund_Shigekura where f_fund_code=%s'
    insert_sql = 'INSERT INTO t_Fund_Shigekura(f_year,f_month,f_fund_name,f_fund_code,f_deadline,f_num,f_period_shares,f_stock_percent,f_stock_percent_balance,f_current_stock_percent,f_current_percent_balance)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    f_year = u'2018年'
    f_month = u'一季报'
    for item in result[::2]:
        fund_code = item.xpath('td[1]/a/text()')[0]
        fund_name = item.xpath('td[2]/a/text()')[0]
        deadline = item.xpath('td[3]/text()')[0]
        num = item.xpath('td[4]/text()')[0]
        period_shares = item.xpath('td[5]/text()')[0]
        stock_percent = item.xpath('td[6]/text()')[0]
        stock_percent_balance = item.xpath('td[7]/text()')[0]
        current_stock_percent = item.xpath('td[8]/text()')[0]
        current_percent_balance = item.xpath('td[9]/text()')[0]

        flag = mysql.fetchOne(selecet_sql,fund_code)
        if not flag:
            mysql.execute(insert_sql,f_year,f_month,fund_name,fund_code,deadline,num,period_shares,stock_percent,stock_percent_balance,current_stock_percent,current_percent_balance)



def sina_awkwardness_moreinfo():
    params = (
        ('symbol', '000059'),
        ('orgtype', 'fund'),
        ('quarter', '20181'),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/api/jsonp.php/var%20details=/ComStockHoldService.getJGBigHoldDetail', headers=headers, params=params, cookies=cookies)
    res = re.findall(r'\(\((.+?\})\)',response.text)[0]
    
    res = res.replace(':','":').replace('{','{"').replace(',',',"').replace(',"{',',{')

    res = json.loads(res)   
    for item in res['data']:                
        print(item['orgCode'])
        print(item['orgName'])
        print(item['orgFullName'])
        print(item['stockAmount'])
        print(item['stockPercent'])
        print(item['stockPercentLast'])
        print(item['stockAmountBalance'])
        print(item['stockPercentBalance'])

# 社保重仓股
def sina_social_stock(page):
    params = (
        ('p', page),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/sbzc/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//*[@id="dataTable"]/tr')
    selecet_sql = 'SELECT * from t_security_Shigekura where f_security_code=%s'
    insert_sql = 'INSERT INTO t_security_Shigekura(f_year,f_month,f_security_name,f_security_code,f_deadline,f_num,f_period_shares,f_stock_percent,f_stock_percent_balance,f_current_stock_percent,f_current_percent_balance)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    f_year = u'2018年'
    f_month = u'一季报'
    for item in result[::2]:
        security_code = item.xpath('td[1]/a/text()')[0]
        security_name = item.xpath('td[2]/a/text()')[0]
        deadline = item.xpath('td[3]/text()')[0]
        num = item.xpath('td[4]/text()')[0]
        period_shares = item.xpath('td[5]/text()')[0]
        stock_percent = item.xpath('td[6]/text()')[0]
        stock_percent_balance = item.xpath('td[7]/text()')[0]
        current_stock_percent = item.xpath('td[8]/text()')[0]
        current_percent_balance = item.xpath('td[9]/text()')[0]

        flag = mysql.fetchOne(selecet_sql,security_code)
        if not flag:
            mysql.execute(insert_sql,f_year,f_month,security_name,security_code,deadline,num,period_shares,stock_percent,stock_percent_balance,current_stock_percent,current_percent_balance)


def sina_social_stock_moreinfo():
    params = (
        ('symbol', '603156'),
        ('orgtype', 'socialSecurity'),
        ('quarter', '20181'),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/api/jsonp.php/var%20details=/ComStockHoldService.getJGBigHoldDetail', headers=headers, params=params, cookies=cookies)
    res = re.findall(r'\(\((.+?\})\)',response.text)[0]
    
    res = res.replace(':','":').replace('{','{"').replace(',',',"').replace(',"{',',{')

    res = json.loads(res)   
    for item in res['data']:                
        print(item['orgCode'])
        print(item['orgName'])
        print(item['orgFullName'])
        print(item['stockAmount'])
        print(item['stockPercent'])
        print(item['stockPercentLast'])
        print(item['stockAmountBalance'])
        print(item['stockPercentBalance'])

# QFII重仓股
def sina_QFII_stock(page):
    params = (
        ('p', page),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/qfii/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//*[@id="dataTable"]/tr')
    selecet_sql = 'SELECT * from t_Qfii_Shigekura where f_qfii_code=%s'
    insert_sql = 'INSERT INTO t_Qfii_Shigekura(f_year,f_month,f_qfii_name,f_qfii_code,f_deadline,f_num,f_period_shares,f_stock_percent,f_stock_percent_balance,f_current_stock_percent,f_current_percent_balance)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    f_year = u'2018年'
    f_month = u'一季报'
    for item in result[::2]:
        qfii_code = item.xpath('td[1]/a/text()')[0]
        qfii_name = item.xpath('td[2]/a/text()')[0]
        deadline = item.xpath('td[3]/text()')[0]
        num = item.xpath('td[4]/text()')[0]
        period_shares = item.xpath('td[5]/text()')[0]
        stock_percent = item.xpath('td[6]/text()')[0]
        stock_percent_balance = item.xpath('td[7]/text()')[0]
        current_stock_percent = item.xpath('td[8]/text()')[0]
        current_percent_balance = item.xpath('td[9]/text()')[0]

        flag = mysql.fetchOne(selecet_sql,qfii_code)
        if not flag:
            mysql.execute(insert_sql,f_year,f_month,qfii_name,qfii_code,deadline,num,period_shares,stock_percent,stock_percent_balance,current_stock_percent,current_percent_balance)

def sina_QFII_stock_moreinfo():
    params = (
        ('symbol', '002285'),
        ('orgtype', 'qfii'),
        ('quarter', '20181'),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/api/jsonp.php/var%20details=/ComStockHoldService.getJGBigHoldDetail', headers=headers, params=params, cookies=cookies)
    res = re.findall(r'\(\((.+?\})\)',response.text)[0]
    
    res = res.replace(':','":').replace('{','{"').replace(',',',"').replace(',"{',',{')

    res = json.loads(res)   
    for item in res['data']:                
        print(item['orgCode'])
        print(item['orgName'])
        print(item['orgFullName'])
        print(item['stockAmount'])
        print(item['stockPercent'])
        print(item['stockPercentLast'])
        print(item['stockAmountBalance'])
        print(item['stockPercentBalance'])


# 股票综合评级
def sina_stock_level(page):
    params = (
        ('p', page),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vIR_SumRating/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//table[@class="list_table"]/tr[position()>1]')
    insert_sql = 'INSERT INTO t_Stock_Rate_copy(f_stock_name,f_stock_code,f_synthesize_rate,f_trade_name,f_buy_num,f_hold_num,f_neutral_num,f_reducing_num,f_sale_num)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if not result:
        logging.error('request error')
        return  
    for item in result:
        stock_code = item.xpath('td[1]/a/text()')[0]
        stock_name = item.xpath('td[2]/a/text()')[0]
        synthesize_rate = item.xpath('td[3]/text()')[0]
        trade_name = ''.join(item.xpath('td[4]/text()'))
        buy_num = item.xpath('td[5]/text()')[0]
        hold_num = item.xpath('td[6]/text()')[0]
        neutral_num = item.xpath('td[7]/text()')[0]
        reducing_num = item.xpath('td[8]/text()')[0].strip()
        sale_num = item.xpath('td[9]/text()')[0]

        mysql.execute(insert_sql,stock_name,stock_code,synthesize_rate,trade_name,buy_num,hold_num,neutral_num,reducing_num,sale_num)



# 机构关注度
def sina_department_attention(page):
    params = (
        ('p', page),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vIR_OrgCare/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//table[@class="list_table"]/tr[position()>1]')
    selecet_sql = 'SELECT * from t_Organization_Attention where f_organization_code=%s'
    insert_sql = 'INSERT INTO t_Organization_Attention(f_organization_name,f_organization_code,f_attention,f_mean_rate,f_newest_rate,f_trade_name,f_buy_num,f_hold_num,f_neutral_num,f_reducing_num,f_sale_num)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in result:
        organization_code = item.xpath('td[1]/a/text()')[0]
        organization_name = item.xpath('td[2]/a/span/text()')[0]
        attention = item.xpath('td[3]/text()')[0]
        mean_rate = item.xpath('td[4]/text()')[0]
        newest_rate = item.xpath('td[5]/text()')[0]
        buy_num = item.xpath('td[6]/text()')[0]
        hold_num = item.xpath('td[7]/text()')[0]
        neutral_num = item.xpath('td[8]/text()')[0]
        reducing_num = item.xpath('td[9]/text()')[0].strip()
        sale_num = item.xpath('td[10]/text()')[0]
        trade_name = ''.join(item.xpath('td[11]/text()'))

        flag = mysql.fetchOne(selecet_sql,organization_code)
        if not flag:
            mysql.execute(insert_sql,organization_name,organization_code,attention,mean_rate,newest_rate,trade_name,buy_num,hold_num,neutral_num,reducing_num,sale_num)


# 行业关注度
def sina_trade_attention(page):
    params = (
        ('p', page),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/q/go.php/vIR_IndustryCare/index.phtml', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//table[@class="list_table"]/tr[position()>1]')
    selecet_sql = 'SELECT * from t_Trade_Attention where f_trade_name=%s'
    insert_sql = 'INSERT INTO t_Trade_Attention(f_trade_name,f_attention,f_attention_num,f_buy_num,f_hold_name,f_neutral_num,f_reducing_num,f_sale_num)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in result:
        trade_name = item.xpath('td[1]/text()')[0]
        attention = item.xpath('td[2]/text()')[0]
        attention_num = item.xpath('td[3]/text()')[0]
        buy_num = item.xpath('td[4]/text()')[0]
        hold_name = item.xpath('td[5]/text()')[0]
        neutral_num = item.xpath('td[6]/text()')[0]
        reducing_num = item.xpath('td[7]/text()')[0]
        sale_num = item.xpath('td[8]/text()')[0]

        flag = mysql.fetchOne(selecet_sql,trade_name)
        if not flag:
            mysql.execute(insert_sql,trade_name,attention,attention_num,buy_num,hold_name,neutral_num,reducing_num,sale_num)
# 新股日历
def sina_new_stock_calendar(page):

    params = (
        ('page', page),
        ('cngem', '0'),
        ('orderBy', 'NetDate'),
        ('orderType', 'desc'),
    )

    response = requests.get('http://vip.stock.finance.sina.com.cn/corp/view/vRPD_NewStockIssue.php', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('GBK'))
    result = selector.xpath('//*[@id="NewStockTable"]/tr[position()>2]')
    selecet_sql = 'SELECT * from t_Stock_Issue where f_stock_code=%s'
    insert_sql = 'INSERT INTO t_Stock_Issue(f_stock_code,f_stock_code2,f_stock_name,f_start_time,f_time,f_num,f_num_balance,f_stock_price,f_pe_ratio,f_stock_limit,f_stock_price_balance,f_internet_number)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in result:
        code = item.xpath('td[1]/div/text()')[0]
        code_buy = item.xpath('td[2]/div/text()')[0]
        name = item.xpath('td[3]/div/a/text()')[0].strip()
        start_time = item.xpath('td[4]/div/text()')[0]
        if item.xpath('td[5]/div/text()'):
            listed_time = item.xpath('td[5]/div/text()')[0]
        else:
            listed_time = None
        publish_num = item.xpath('td[6]/div/text()')[0]
        publish_num_web = item.xpath('td[7]/div/text()')[0]
        price = item.xpath('td[8]/div/text()')[0]
        market_rate = item.xpath('td[9]/div/text()')[0]
        up_limit = item.xpath('td[10]/div/text()')[0]
        total_money = item.xpath('td[11]/div/text()')[0]
        internet_number = item.xpath('td[12]/div/text()')[0]

        flag = mysql.fetchOne(selecet_sql,code)
        if not flag:
            mysql.execute(insert_sql,code,code_buy,name,start_time,listed_time,publish_num,publish_num_web,price,market_rate,up_limit,total_money,internet_number)


if __name__ =='__main__': 
    #共20页
    for i in range(1,21): 
        logging.info(i)  
        time.sleep(8)
        sina_stock_department(str(i))
    #共15页
    for i in range(1,16): 
        logging.info(i)   
        time.sleep(8)
        sina_awkwardness(str(i))
    #共6页
    for i in range(1,7): 
        logging.info(i)    
        time.sleep(8)
        sina_social_stock(str(i))
    # # 共3页
    for i in range(1,4): 
        logging.info(i)  
        time.sleep(8)
        sina_QFII_stock(str(i))
    # 共1183页
    b = 'TRUNCATE TABLE t_Stock_Rate_copy'
    mysql.execute(b)
    for i in range(1,1184): 
        logging.info(i)  
        time.sleep(5)
        sina_stock_level(str(i))
    
    b = 'TRUNCATE TABLE t_Stock_Rate'
    mysql.execute(b)
    a = 'INSERT INTO t_Stock_Rate SELECT * FROM t_Stock_Rate_copy'
    mysql.execute(a)

    # 共41页
    for i in range(1,42): 
        logging.info(i)  
        time.sleep(10)
        sina_department_attention(str(i))

    #共2页
    for i in range(1,3): 
        # logging.info(i)  
        # time.sleep(10)
        sina_trade_attention(str(i))

    #共18页
    for i in range(1,19): 
        # logging.info(i)  
        time.sleep(5)
        sina_new_stock_calendar(str(i))





