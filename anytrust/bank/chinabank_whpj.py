import requests
from lxml import etree
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import time
import json
import re

mysql = MySQLWrapper('db_forex_source')

def run():
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.boc.cn/sourcedb/whpj/index_1.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get('http://www.boc.cn/sourcedb/whpj/index.html', headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    result = selector.xpath('/html/body/div/div[3]/div[1]/div[2]/table/tr[position()>1]')
    select_sql = 'SELECT * FROM t_whpj_source WHERE f_currency_name=%s '
    insert_sql = 'INSERT INTO t_whpj_source(f_currency_name,f_spot_buy_price,f_oof_buy_price,f_spot_sale_price,f_oof_sale_price,f_foreign_rate_price,f_corrected_price,f_start_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    update_sql = 'UPDATE t_whpj_source SET f_spot_buy_price=%s,f_oof_buy_price=%s,f_spot_sale_price=%s,f_oof_sale_price=%s,f_foreign_rate_price=%s,f_corrected_price=%s,f_start_time=%s where f_currency_name=%s'
    insert_sql_old = 'INSERT INTO t_whpj_source_copy(f_currency_name,f_spot_buy_price,f_oof_buy_price,f_spot_sale_price,f_oof_sale_price,f_foreign_rate_price,f_corrected_price,f_start_time)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in result:
        name = item.xpath('td[1]/text()')[0]
        buy_price = get_text_from_xpath(item,'td[2]/text()')
        buy_price_chao = get_text_from_xpath(item,'td[3]/text()')
        sell_price = get_text_from_xpath(item,'td[4]/text()')
        sell_price_chao = get_text_from_xpath(item,'td[5]/text()')
        converted_price = get_text_from_xpath(item,'td[6]/text()')
        update_time = item.xpath('td[7]/text()')[0]+' '+item.xpath('td[8]/text()')[0]

        flag = mysql.fetchOne(select_sql,name)
        if flag:
            mysql.execute(update_sql,buy_price,buy_price_chao,sell_price,sell_price_chao,converted_price,converted_price,update_time,name)
        else:
            mysql.execute(insert_sql,name,buy_price,buy_price_chao,sell_price,sell_price_chao,converted_price,converted_price,update_time)
        mysql.execute(insert_sql_old,name,buy_price,buy_price_chao,sell_price,sell_price_chao,converted_price,converted_price,update_time)
def get_text_from_xpath(item,xpath):
    if item.xpath(xpath):
        return item.xpath(xpath)[0]
    else:
        return None

if __name__ == '__main__':
    run()

