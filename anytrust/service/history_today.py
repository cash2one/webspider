import requests
from lxml import etree
import time
import os
if os.name == 'nt':
    setting_path = './settings'
    log_path = 'log/house.log' 
    pic_path = 'today/'
else:
    setting_path = '/ROOT/www/spider/settings'
    log_path = '/ROOT/logs/house.log'
    pic_path = '/ROOT/www/spider_pic/today/'
import sys
sys.path.append(setting_path)
from mysql import MySQLWrapper
import logging

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename=log_path,
                )
mysql = MySQLWrapper('db_spider')

foldername = pic_path+time.strftime("%m", time.localtime(time.time()))
if not os.path.exists(foldername):
    os.makedirs(foldername)

def get_list():

    today  = time.localtime(time.time())
    today = str(today.tm_mon) + '/' + str(today.tm_mday) 
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'bdshare_firstime=1528090086646; UM_distinctid=163c94456f12f6-0e07fc0b6606d6-39614807-15f900-163c94456f223b; ASPSESSIONIDCCQCDAQT=PPKLFEPCJIEKILNLAKPEHFJH; CNZZDATA452871=cnzz_eid%3D731739664-1528085253-null%26ntime%3D1528158847; Hm_lvt_5ca35bf8a591fd43aee73e87a5bc0283=1528090089,1528162600; Hm_lpvt_5ca35bf8a591fd43aee73e87a5bc0283=1528162608',
        'Host': 'www.lssdjt.com',
        'Referer': 'http://www.lssdjt.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }

    response = requests.get('http://www.lssdjt.com/'+today+'/',headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    result = selector.xpath('//ul[@class="list clearfix"]/li')
    insert_sql = 'INSERT INTO m_media_history_today(f_today,f_uid,f_url,f_title,f_date,f_content,f_html,f_image)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in result:
        url = item.xpath('a/@href')[0]
        uid = url.split('/')[-1].split('.')[0]
        date = item.xpath('a/em/text()')[0]
        title = item.xpath('a/i/text()')[0]
        html,content,image = get_content(url)
        if image:
            image = download_pic(uid,image)
        mysql.execute(insert_sql,today,uid,url,title,date,content,html,image)




def get_content(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'bdshare_firstime=1528090086646; UM_distinctid=163c94456f12f6-0e07fc0b6606d6-39614807-15f900-163c94456f223b; ASPSESSIONIDCCQCDAQT=PPKLFEPCJIEKILNLAKPEHFJH; Hm_lvt_5ca35bf8a591fd43aee73e87a5bc0283=1528090089,1528162600; ASPSESSIONIDCASCDBQT=BNHFMIPCCNPLMINKGPHPGDGA; CNZZDATA452871=cnzz_eid%3D731739664-1528085253-null%26ntime%3D1528164248; Hm_lpvt_5ca35bf8a591fd43aee73e87a5bc0283=1528164921',
        'Host': 'www.lssdjt.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
    response = requests.get(url,headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    result = selector.xpath('//div[contains(@class,"post_public")]')[0]


    flag = result.xpath('h2/text()')

    if flag:
        res = result.xpath('h2[last()]/preceding-sibling::*//text()')
    else:
        res = result.xpath('p//text()')
    html = etree.tounicode(result)
    content = ''.join(res).replace('\xa0\xa0\xa0\xa0','\n\xa0\xa0').strip('\n')
    
    if result.xpath('p/img[not(@class)]/@src'):
        image = result.xpath('p/img[not(@class)]/@src')
    else:
        image = None
    return html,content,image

def download_pic(uid,image_list):
    picture = []
    for i in range(len(image_list)):
        if 'http' not in image_list[i]:
            url = 'http:'+image_list[i]
        else:
            url = image_list[i]
        response = requests.get(url,timeout=15)
        temp = url.split('/')
        a = temp[-3]
        if '.com' in a:
            a = ''
        b = temp[-2]
        temp = temp[-1]
        temp = temp.split('.')
        if len(temp)<=2:
            filename = uid+'_'+a+'_'+b+'_'+temp[0]+'.jpg'
        else:
            filename = uid+'_'+a+'_'+b+'_'+temp[-2]+'.jpg'
        picture.append(filename)
        with open(foldername+'/'+filename,'wb') as f:
            f.write(response.content)
    return ';'.join(picture) 


if __name__ == '__main__':
    get_list()
