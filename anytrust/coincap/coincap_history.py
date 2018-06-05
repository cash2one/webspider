import requests
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
                filename='/ROOT/logs/coincap.log',
                )
mysql = MySQLWrapper('db_cryptocurrency')

def get_exchange():
    select_sql = 'SELECT f_corrected_price FROM db_forex_source.t_whpj_source WHERE f_currency_name=%s'
    result = mysql.fetchOne(select_sql,u'美元')
    return float(result['f_corrected_price']/100)


def get_message(exchange):
    headers = {
        'Referer': 'http://coincap.io/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    }

    response = requests.get('http://coincap.io/front', headers=headers)

    for item in response.json():
        long_name = item['long']
        short_name = item['short']
        if long_name == 'Bitcoin':
            bt_price = item['price']
        mktcap = item['mktcap']
        price = item['price']
        price_cny = price*exchange
        price_bt = price/bt_price
        vwapData = item['vwapData']
        vwapData_cny = vwapData*exchange
        vwapData_bt = vwapData/bt_price
        supply = item['supply']
        usdVolume = item['usdVolume']
        cap24hrChange = item['cap24hrChange']
        write_into_db(long_name,short_name,mktcap,price,price_cny,price_bt,vwapData,vwapData_cny,vwapData_bt,supply,usdVolume,cap24hrChange)

def write_into_db(long_name,short_name,mktcap,price,price_cny,price_bt,vwapData,vwapData_cny,vwapData_bt,supply,usdVolume,cap24hrChange):
    f_Year = time.strftime("%Y", time.localtime(time.time()))
    f_Month = time.strftime("%m", time.localtime(time.time()))
    f_Day = time.strftime("%d", time.localtime(time.time()))
    insert_sql = 'INSERT INTO t_coincap_all(f_LongName,f_ShortName,f_MarketCap,f_USDPrice,f_CNYPrice,f_BTCPrice,f_USDVWAP,f_CNYVWAP,f_BTCVWAP,f_Supply,f_Volume,f_Rate,f_Year,f_Month,f_Day)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    mysql.execute(insert_sql,long_name,short_name,mktcap,price,price_cny,price_bt,vwapData,vwapData_cny,vwapData_bt,supply,usdVolume,cap24hrChange,f_Year,f_Month,f_Day)


    
if __name__ == '__main__':
    exchange = get_exchange()
    get_message(exchange)