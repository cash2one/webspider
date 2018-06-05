import requests
import json
import re
import time
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import pymysql
import os
from lxml import etree

ZEROS_time = int(time.time()-60*60)*1000
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/xueqiu.log',
                )
mysql = MySQLWrapper('db_spider')
foldername = '/ROOT/www/spider_pic/xueqiu_pic/'+time.strftime("%Y-%m", time.localtime(time.time()))
if not os.path.exists(foldername):
    os.makedirs(foldername) 

cookies = {
    'xq_a_token': '229a3a53d49b5d0078125899e528279b0e54b5fe',
    'xq_a_token.sig': 'oI-FfEMvVYbAuj7Ho7Z9mPjGjjI',
    'xq_r_token': '8a43eb9046efe1c0a8437476082dc9aac6db2626',
    'xq_r_token.sig': 'Efl_JMfn071_BmxcpNvmjMmUP40',
    'u': '331524194801100',
    '__utma': '1.2001343840.1524194801.1524194801.1524194801.1',
    '__utmc': '1',
    '__utmz': '1.1524194801.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
    'device_id': '0bef57319378f6299c4b10afd8eb3370',
    's': 'ej11i3pklt',
    'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1524194801,1524194832',
    '__utmt': '1',
    'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1524196475',
    '__utmb': '1.21.10.1524194801',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://xueqiu.com/hq',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
s = requests.session()
def get_cookies():
    response = s.get('http://xueqiu.com/', headers=headers)

def get_paper_list(user_id):
    params = (
        ('page', '1'),
        ('user_id', user_id),
    )

    response = s.get('https://xueqiu.com/v4/statuses/user_timeline.json', headers=headers, params=params, cookies=cookies)
    res = response.json()
    parse_response(res)



def parse_response(res):

    insert_sql = 'INSERT INTO m_media_xueqiu_paper(f_id,f_user_id,f_user_name,f_title,f_update_time,f_source,f_content,f_picture,f_recomment_nums,f_comment_nums,f_like_nums,f_paper_url,f_content_html,f_paper_type)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for item in res['statuses']:
        if ZEROS_time>item['created_at']:
            return
        paper_id = str(item['user']['id']) 
        user_id =  str(item['id'])    
        user_name = item['user']['screen_name']
        title = item['title']
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(item['created_at']/1000)))
        source = item['source']       
        content_html = item['text']
        if content_html == u'转发':
            content_html = item['retweeted_status']['text']
        selector = etree.HTML(content_html)
        content = selector.xpath('//text()')
        content = '\n'.join(content)
        picture=item['pic']
        if picture:
            picture=picture.split(',')
            for i in range(len(picture)):
                picture[i] = picture[i].replace('!thumb.jpg','')
                filename = str(item['id'])+'_'+str(i)+'_'+picture[i].split('/')[-1]
                re_pic = requests.get(picture[i])
                with open(foldername+'/'+filename,'wb') as f:
                    f.write(re_pic.content)
                picture[i] = filename
            picture = ';'.join(picture)

        recomment_nums=item['retweet_count']
        comment_nums=item['reply_count']
        like_nums=item['like_count']
        paper_url =' https://xueqiu.com'+item['target']
        paper_type = item['type']       

        try:
            mysql.execute(insert_sql,paper_id,user_id,user_name,title,update_time,source,content,picture,recomment_nums,comment_nums,like_nums,paper_url,content_html,paper_type)
        except pymysql.err.IntegrityError as e:
            pass


def main():
    select_sql = 'SELECT f_id FROM m_media_xueqiu_user_v'
    result = mysql.fetchAll(select_sql)
    for item in result:
        time.sleep(2)
        get_paper_list(item['f_id'])

if __name__ == '__main__':
    get_cookies()
    main()

