import requests
import json
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import time


logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/fund.log',
                )
mysql = MySQLWrapper('db_finance_shares')

headers = {
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://fund.10jqka.com.cn/datacenter/sy/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
}

def run_gpx():
    urls = ['http://fund.ijijin.cn/data/Net/info/gpx_code_asc_0_0_1_9999_0_0_0_jsonp_g.html',
            'http://fund.ijijin.cn/data/Net/info/zqx_code_asc_0_0_1_9999_0_0_0_jsonp_g.html',
            'http://fund.ijijin.cn/data/Net/info/hhx_F009_desc_0_0_1_9999_0_0_0_jsonp_g.html',
           'http://fund.ijijin.cn/data/Net/info/ETF_F009_desc_0_0_1_9999_0_0_0_jsonp_g.html',
           'http://fund.ijijin.cn/data/Net/info/LOF_F009_desc_0_0_1_9999_0_0_0_jsonp_g.html', 
           'http://fund.ijijin.cn/data/Net/info/QDII_F009_desc_0_0_1_9999_0_0_0_jsonp_g.html',
           'http://fund.ijijin.cn/data/Net/info/bbx_F009_desc_0_0_1_9999_0_0_0_jsonp_g.html', 
           'http://fund.ijijin.cn/data/Net/info/zsx_F009_desc_0_0_1_9999_0_0_0_jsonp_g.html', 
           'http://fund.ijijin.cn/data/Net/info/dxx_F009_desc_0_0_1_9999_0_0_0_jsonp_g.html', ]
    for index,url in enumerate(urls, start=1):
        response = requests.get(url, headers=headers)
        res = response.text.replace('g(','')[:-1]
        res = json.loads(res)
        parse_response(res,str(index))


def parse_response(res,type_name):
    select_sql = 'SELECT * from t_shares_gmjj_new where unique_id=%s'
    insert_sql = 'INSERT INTO t_shares_gmjj_new(f_code,f_name,f_link,f_update_date,f_week_profit,f_month_profit,f_quarter_profit,f_year_profit,f_three_year_profit,f_days_profit,f_start_profit,f_type,f_create_time,unique_id)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    update_sql = 'UPDATE t_shares_gmjj_new SET f_name=%s,f_link=%s,f_update_date=%s,f_week_profit=%s,f_month_profit=%s,f_quarter_profit=%s,f_year_profit=%s,f_three_year_profit=%s,f_days_profit=%s,f_start_profit=%s,f_type=%s,f_create_time=%s where unique_id=%s'
    insert_sql_old = 'INSERT INTO t_shares_gmjj_old(f_code,f_name,f_link,f_update_date,f_week_profit,f_month_profit,f_quarter_profit,f_year_profit,f_three_year_profit,f_days_profit,f_start_profit,f_type,f_create_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for key in res['data']['data'].keys():
        fund_code = res['data']['data'][key]['code']
        fund_name = res['data']['data'][key]['name']
        fund_url = 'http://fund.10jqka.com.cn/'+str(fund_code)+'/pubnote.html'
        update_date = res['data']['data'][key]['SYENDDATE']
        week_income = res['data']['data'][key]['F003N_FUND33']
        if week_income:
            week_income += '%'
        month_income = res['data']['data'][key]['F008']
        if month_income:
            month_income += '%'
        quarter_income = res['data']['data'][key]['F009']
        if quarter_income:
            quarter_income += '%' 
        year_income = res['data']['data'][key]['F011']
        if year_income:
            year_income += '%'
        three_year_income = res['data']['data'][key]['F015N_FUND33']
        if three_year_income:
            three_year_income += '%'
        yestarday_income = res['data']['data'][key]['prerate']
        if yestarday_income:
            yestarday_income += '%'
        found_income = res['data']['data'][key]['F012']
        if found_income:
            found_income += '%'
        unique_id = str(fund_code) + '_' + str(type_name)
        create_time = int(time.time())
        flag = mysql.fetchOne(select_sql,unique_id)
        if flag:
            mysql.execute(update_sql,fund_name,fund_url,update_date,week_income,month_income,quarter_income,year_income,three_year_income,yestarday_income,found_income,type_name,create_time,unique_id)
        else:
            mysql.execute(insert_sql,fund_code,fund_name,fund_url,update_date,week_income,month_income,quarter_income,year_income,three_year_income,yestarday_income,found_income,type_name,create_time,unique_id)
        mysql.execute(insert_sql_old,fund_code,fund_name,fund_url,update_date,week_income,month_income,quarter_income,year_income,three_year_income,yestarday_income,found_income,type_name,create_time)

if __name__ == '__main__':
    run_gpx()


