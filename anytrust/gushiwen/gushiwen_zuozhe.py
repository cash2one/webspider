import requests
from lxml import etree
import re
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import time
import os

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/gushiwen.log',
                )
mysql = MySQLWrapper('db_GuShiWen')
foldername = '/ROOT/www/spider_pic/author/'+time.strftime("%Y-%m", time.localtime(time.time()))
if not os.path.exists(foldername):
    os.makedirs(foldername) 


def run(page):
    cookies = {
        'Hm_lvt_4c1638db937a6ad4a0e6a8bdfa32146f': '1526977913,1526977946',
        'Hm_lpvt_4c1638db937a6ad4a0e6a8bdfa32146f': '1526977998',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.shicimingju.com/chaxun/zuozhe/13.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get('http://www.shicimingju.com/chaxun/zuozhe/'+page+'.html', headers=headers, cookies=cookies)
    selector = etree.HTML(response.text)
    if selector.xpath('//div[@class="zuozhe-header www-shadow-card"]'):
        result = selector.xpath('//div[@class="zuozhe-header www-shadow-card"]')[0]
    else:
        return

    author = result.xpath('h2/a/text()')[0]
    if result.xpath('h2/span/text()'):
        alias = result.xpath('h2/span/text()')[0]
    else:
        alias = None
 
    nickname = ''.join(result.xpath('div[1]/h6/a/text()'))

    if result.xpath('div[2]/text()'):
        YEAR = result.xpath('div[2]/text()')[0]
    else:
        YEAR = None
    numbers = result.xpath('div[3]/text()')[0].replace(u'首','')

    if result.xpath('div[4]//text()'):
        desp = ''.join(result.xpath('div[4]//text()')).strip()
    else:
        desp = ''

    if result.xpath('div[4]/img/@src'):
        image = result.xpath('div[4]/img/@src')[0]
        image = download_pic(page,image)
    else:
        image = None

    insert_sql = 'INSERT INTO t_Author_copy(f_author,f_alias,f_label,f_image,f_year,f_nums,f_introduction)VALUES(%s,%s,%s,%s,%s,%s,%s)'
    mysql.execute(insert_sql,author,alias,nickname,image,YEAR,numbers,desp)


def download_pic(page,url):

    if 'http' not in url:
        url = 'http:'+url

    response = requests.get(url,timeout=15)
    
    with open(foldername+'/'+page+'.jpg','wb') as f:
        f.write(response.content)
    return page+'.jpg'

def main():
    for i in range(490,3400):
        time.sleep(3)
        print(i)
        run(str(i))

if __name__ == '__main__':
    main()

