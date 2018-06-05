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
                filename='/ROOT/logs/jisilu.log',
                )
mysql = MySQLWrapper('db_finance_shares')


cookies = {
    'kbzw__Session': 'sqqnev4iguu4m3o3unhsodmqb2',
    'Hm_lvt_164fe01b1433a19b507595a43bf58262': '1524041800',
    'kbz_newcookie': '1',
    'Hm_lpvt_164fe01b1433a19b507595a43bf58262': '1524043750',
}

headers = {
    'Origin': 'https://www.jisilu.cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://www.jisilu.cn/data/ha/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}


# 可转债
def jisilu_bonds():


    params = (
        ('___jsl', 'LST___t='+str(int(time.time()*1000))),
    )

    data = [
      ('qflag', 'Y'),
      ('rp', '50'),
    ]
    select_sql = 'SELECT * FROM t_shares_convertible_new WHERE f_code=%s'
    update_sql = 'UPDATE t_shares_convertible_new SET f_name=%s,f_price=%s,f_change=%s,f_stock_name=%s,f_stock_price=%s,f_stock_change=%s,f_pb=%s,f_convert_price=%s,f_convert_value=%s,'\
                        'f_premium_rate=%s,f_buyback_price=%s,f_force_buyback_price=%s,f_bond_percent=%s,f_expire_date=%s,'\
                        'f_left_time=%s,f_profit_before_tax=%s,f_profit_after_profit=%s,f_volume=%s,f_conversion_rate=%s,f_type_kzz=%s,f_type_kjhz=%s,f_type_canbuy=%s,f_create_time=%s WHERE f_code=%s'
    insert_sql = 'INSERT INTO t_shares_convertible_new(f_name,f_price,f_change,f_stock_name,f_stock_price,f_stock_change,f_pb,f_convert_price,f_convert_value,'\
                        'f_premium_rate,f_buyback_price,f_force_buyback_price,f_bond_percent,f_expire_date,'\
                        'f_left_time,f_profit_before_tax,f_profit_after_profit,f_volume,f_conversion_rate,f_type_kzz,f_type_kjhz,f_type_canbuy,f_create_time,f_code)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    response = requests.post('https://www.jisilu.cn/data/cbnew/cb_list/', headers=headers, params=params, cookies=cookies, data=data)
    for item in response.json()['rows']:
        res = []
        
        res.append(item['cell']['bond_nm'])                   #转债名称
        res.append(item['cell']['full_price'])                #转债现价
        res.append(item['cell']['increase_rt'])               #转债涨跌幅
        res.append(item['cell']['stock_nm'])                  #正股名称
        res.append(item['cell']['sprice'])                    #正股现价
        res.append(item['cell']['sincrease_rt'])              #正股涨跌幅
        res.append(item['cell']['pb'])                        #PB
        res.append(item['cell']['convert_price'])             #转股价
        res.append(item['cell']['convert_value'])             #转股价值
        res.append(item['cell']['premium_rt'])                #溢价率
        res.append(item['cell']['put_convert_price'])         #回售触发价
        res.append(item['cell']['force_redeem_price'])        #强赎触发价
        res.append(item['cell']['convert_amt_ratio'])         #转债占比
        res.append(item['cell']['short_maturity_dt'])         #到期时间
        res.append(item['cell']['year_left'])                 #年限
        res.append(item['cell']['ytm_rt'])                    #到期税前收益率
        res.append(item['cell']['ytm_rt_tax'])                #到期税后收益率
        res.append(item['cell']['volume'])                    #成交额
        res.append(item['cell']['repo_discount_rt'])          #折算
        if item['cell']['btype'] == 'C':
            res.append(1)
            res.append(0)
        else:
            res.append(0)
            res.append(1)

        res.append(1)
        res.append(int(time.time()))
        res.append(item['id'])                                #代码

        flag = mysql.fetchOne(select_sql,res[-1])
        if flag:
            mysql.execute_list(update_sql,res)
        else:            
            mysql.execute_list(insert_sql,res)

    data = [
      ('listed', 'Y'),
      ('rp', '50'),
    ]
    select_sql = 'SELECT * FROM t_shares_convertible_new WHERE f_code=%s'
    update_sql = 'UPDATE t_shares_convertible_new SET f_type_listed=%s WHERE f_code=%s'

    response = requests.post('https://www.jisilu.cn/data/cbnew/cb_list/', headers=headers, params=params, cookies=cookies, data=data)
    for item in response.json()['rows']:
                
        code_id = item['id']                                #代码
        flag = mysql.fetchOne(select_sql,code_id)       
        if flag:
            mysql.execute(update_sql,1,code_id)

    
    a = 'INSERT INTO t_shares_convertible_old SELECT * FROM t_shares_convertible_new'
    mysql.execute(a)
        

def jisilu_AH():   
    params = (
        ('___jsl', 'LST___t='+str(int(time.time()*1000))),
    )

    data = [
      ('rp', '25'),
      ('page', '1'),
    ]

    response = requests.post('https://www.jisilu.cn/data/ha/index2list/', headers=headers, params=params, cookies=cookies, data=data)
    for item in response.json()['rows']:
        res = []
        stock_name = item['cell']['stock_name']               #股票名称
        a_code = item['cell']['a_code']                       #A股代码
        h_code = item['cell']['h_code']                       #H股代码
        a_price = item['cell']['a_price']                     #A股价格
        a_increase_rt = item['cell']['a_increase_rt']         #A股涨跌幅
        a_free_shares = item['cell']['a_free_shares']         #A股自由流通
        h_price = item['cell']['h_price']                     #H股价格
        rmb_price = item['cell']['rmb_price']                 #H股价格
        h_increase_rt = item['cell']['h_increase_rt']         #H股涨跌幅
        h_free_shares = item['cell']['h_free_shares']         #H股自由流通
        ha_ratio = item['cell']['ha_ratio']                   #比价(H/A)
        create_time = int(time.time())

        select_sql = 'SELECT * FROM t_shares_ah_new WHERE f_code_a=%s'
        flag = mysql.fetchOne(select_sql,a_code)
        if flag:
            update_sql = 'UPDATE t_shares_ah_new SET f_name=%s,f_a_shares_price=%s,f_a_updown_rate=%s,f_a_free_float_price=%s,f_h_shares_price_h=%s,'\
                        'f_h_shares_price=%s,f_h_updown_rate=%s,f_h_free_float_price_h=%s,f_parity=%s,f_create_time=%s WHERE f_code_a=%s'
            mysql.execute(update_sql,stock_name,a_price,a_increase_rt,a_free_shares,h_price,rmb_price,h_increase_rt,h_free_shares,ha_ratio,create_time,a_code)
        else:
            insert_sql = 'INSERT INTO t_shares_ah_new(f_name,f_code_a,f_code_h,f_a_shares_price,f_a_updown_rate,f_a_free_float_price,f_h_shares_price_h,'\
                        'f_h_shares_price,f_h_updown_rate,f_h_free_float_price_h,f_parity,f_create_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,stock_name,a_code,h_code,a_price,a_increase_rt,a_free_shares,h_price,rmb_price,h_increase_rt,h_free_shares,ha_ratio,create_time)

        insert_sql_old = 'INSERT INTO t_shares_ah_old(f_name,f_code_a,f_code_h,f_a_shares_price,f_a_updown_rate,f_a_free_float_price,f_h_shares_price_h,'\
                        'f_h_shares_price,f_h_updown_rate,f_h_free_float_price_h,f_parity,f_create_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        mysql.execute(insert_sql_old,stock_name,a_code,h_code,a_price,a_increase_rt,a_free_shares,h_price,rmb_price,h_increase_rt,h_free_shares,ha_ratio,create_time)


def jisilu_fenhong(market):
    cookies = {
        'kbzw__Session': 'sqqnev4iguu4m3o3unhsodmqb2',
        'Hm_lvt_164fe01b1433a19b507595a43bf58262': '1524041800',
        'kbz_newcookie': '1',
        'Hm_lpvt_164fe01b1433a19b507595a43bf58262': '1524043750',
    }

    headers = {
        'Origin': 'https://www.jisilu.cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.jisilu.cn/data/ha/',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('___jsl', 'LST___t='+str(int(time.time()*1000))),
    )

    data = [
      ('rp', '500'),
      ('page', '1'),
      ('market', market),
    ]

    response = requests.post('https://www.jisilu.cn/data/stock/dividend_rate_list/', headers=headers, params=params, cookies=cookies, data=data)
    select_sql = 'SELECT * FROM t_shares_bonus_new WHERE f_code=%s'
    update_sql = 'UPDATE t_shares_bonus_new SET f_name=%s,f_price=%s,f_rose=%s,f_turnover=%s,f_market_value=%s,f_pe_ttm=%s,f_pe_degree=%s,f_pb=%s,'\
                        'f_pb_degree=%s,f_dividend_yield=%s,f_year_dividend_yield=%s,f_five_average=%s,f_year_roe=%s,f_five_average_roe=%s,f_five_revenue_growth=%s,'\
                        'f_five_profit_growth=%s,f_every_shares_increase=%s,f_interest_liabilities=%s,f_industry=%s,f_stype=%s,f_create_time=%s WHERE f_code=%s'
    insert_sql = 'INSERT INTO t_shares_bonus_new(f_name,f_price,f_rose,f_turnover,f_market_value,f_pe_ttm,f_pe_degree,f_pb,f_pb_degree,f_dividend_yield,'\
                        'f_year_dividend_yield,f_five_average,f_year_roe,f_five_average_roe,f_five_revenue_growth,'\
                        'f_five_profit_growth,f_every_shares_increase,f_interest_liabilities,f_industry,f_stype,f_create_time,f_code)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    insert_sql_old = 'INSERT INTO t_shares_bonus_old(f_name,f_price,f_rose,f_turnover,f_market_value,f_pe_ttm,f_pe_degree,f_pb,f_pb_degree,f_dividend_yield,'\
                        'f_year_dividend_yield,f_five_average,f_year_roe,f_five_average_roe,f_five_revenue_growth,'\
                        'f_five_profit_growth,f_every_shares_increase,f_interest_liabilities,f_industry,f_stype,f_create_time,f_code)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    for item in response.json()['rows']:
        res = []
        res.append(item['cell']['stock_nm'])                 #名称
        res.append(item['cell']['price'])                    #价格
        res.append(item['cell']['increase_rt']+'%')          #涨幅
        res.append(item['cell']['volume'])                   #成交额(万元)
        res.append(item['cell']['total_value'])              #市值(亿元)
        res.append(item['cell']['pe'])                       #PE
        res.append(item['cell']['pe_temperature'])           #PE温度
        res.append(item['cell']['pb'])                       #PB
        res.append(item['cell']['pb_temperature'])           #PB温度
        res.append(item['cell']['dividend_rate']+'%')        #TTM股息率
        res.append(item['cell']['dividend_rate2']+'%')       #去年股息率
        res.append(item['cell']['aft_dividend']+'%')         #5年平均股息率
        res.append(item['cell']['roe']+'%')                  #最新年报ROE
        res.append(item['cell']['roe_average']+'%')          #5年平均ROE
        res.append(item['cell']['revenue_average']+'%')      #5年营收复合增长率
        res.append(item['cell']['profit_average']+'%')       #5年利润复合增长率
        res.append(item['cell']['eps_growth_ttm']+'%')       #每股收益同比增长
        res.append(item['cell']['int_debt_rate']+'%')        #有息负债率
        # res.append(item['cell']['industry'])                 #行业
        res.append(item['cell']['industry_nm'])              #行业
        if market == 'sh':
            res.append('1')
        else:
            res.append('2')
        res.append(int(time.time()))
        res.append(item['cell']['stock_id'])                #股票代码

        

        flag = mysql.fetchOne(select_sql,res[-1])
        if flag:
            mysql.execute_list(update_sql,res)
        else:            
            mysql.execute_list(insert_sql,res)

        mysql.execute_list(insert_sql_old,res)


if __name__ =='__main__': 
    jisilu_AH()
    jisilu_fenhong('sh')
    jisilu_fenhong('sz')
