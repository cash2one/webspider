import requests
import re
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import os
import time

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/toutiao.log',
                )
mysql = MySQLWrapper('db_spider')

foldername = '/ROOT/www/spider_pic/toutiao/'+time.strftime("%Y-%m-%d", time.localtime(time.time()))
if not os.path.exists(foldername):
    os.makedirs(foldername) 

requests.adapters.DEFAULT_RETRIES = 8
s = requests.session()
s.keep_alive = False

headers = {
    'cookie': 'tt_webid=6552668637491627533; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=163388baac7396-0d6d0e85905875-3961430f-15f900-163388baac819e; CNZZDATA1259612802=755731384-1525658188-https%253A%252F%252Fwww.baidu.com%252F%7C1525658188; __tasessionId=ttkg9wke71525662067583; tt_webid=6552668637491627533; uuid="w:d7420c65046c4f528a69a9f568ebff1b"',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'authority': 'www.toutiao.com',
    'x-requested-with': 'XMLHttpRequest',
}

def toutiao_keji():
    params = (
        ('category', 'news_tech'),
        ('utm_source', 'toutiao'),
        ('widen', '1'),
        ('max_behot_time', '0'),
        ('max_behot_time_tmp', '0'),
        ('tadrequire', 'true'),
        ('as', 'A1F51A3E6F7DDFA'),
        ('cp', '5AEF4D0D2FBA4E1'),
        ('_signature', 'aL14KwAAMlXCkjirlim1fmi9eD'),
    )


    response = s.get('https://www.toutiao.com/api/pc/feed/', headers=headers, params=params,timeout=15)
    res = response.json()
    parse_response(res)

def toutiao_finance():
    params = (
        ('category', 'news_finance'),
        ('utm_source', 'toutiao'),
        ('widen', '1'),
        ('max_behot_time', '0'),
        ('max_behot_time_tmp', '0'),
        ('tadrequire', 'true'),
        ('as', 'A1759A2E5F9F715'),
        ('cp', '5AEF5FB7D1E53E1'),
        ('_signature', 'EYPkdwAAS3C7rKT3RVUAHhGD5G'),
    )

    response = s.get('https://www.toutiao.com/api/pc/feed/', headers=headers, params=params)
    res = response.json()
    parse_response(res)
          
def toutiao_car():
    params = (
        ('category', 'news_car'),
        ('utm_source', 'toutiao'),
        ('widen', '1'),
        ('max_behot_time', '0'),
        ('max_behot_time_tmp', '0'),
        ('tadrequire', 'true'),
        ('as', 'A1858ABE4F3F9B6'),
        ('cp', '5AEF2FD92B86EE1'),
        ('_signature', 'FOL5nQAAThG-zbkduzsyehTi-Y'),
    )

    response = s.get('https://www.toutiao.com/api/pc/feed/', headers=headers, params=params)
    res = response.json()
    parse_response(res)
    
def parse_response(res):
    
    for item in res['data']:
        if item.get('article_genre','')=='article':
            paper_id = 'a'+item['item_id']
            logging.info(paper_id)
            title = item['title']
            tag = item.get('chinese_tag',u'科技')
            comments_nums = item.get('comments_count','0')
            source = item.get('source',None)
            # source_url = item['source_url']
            publish_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item['behot_time']))
            if 'image_url' in item.keys():
                avatar = paper_id+'_'+item['image_url'].split('/')[-1]+'.jpg'
            else:
                avatar = None
            image_list = download_pic(paper_id,item.get('image_list',[]))
            content,content_html = get_content(paper_id)
            label = ';'.join(item.get('label',[]))
            account = u'今日头条'
            paper_url = 'https://www.toutiao.com/'+paper_id+'/'

            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_source,f_publish_time,f_avatar,f_image_list,f_label,f_paper_url)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,content,content_html,comments_nums,source,publish_time,avatar,image_list,label,paper_url)

def get_content(paper_id):
    logging.info('https://www.toutiao.com/'+paper_id+'/')
    response = s.get('https://www.toutiao.com/'+paper_id+'/', headers=headers)
    result = re.findall(r'BASE_DATA = ({.+?});',response.text,re.DOTALL)[0].replace('\n','')
    content = re.findall(r"content: '(.+?);'",response.text,re.DOTALL)[0].replace('&lt;','<').replace('&gt;','>').replace('&#x3D;','=').replace('&quot;',' ').replace('&gt','>')
    html = content
    # html = re.sub(r'src= http://p\d\.pstatp\.com/large/pgc-image/.+?  ','{$image location$}',html)
    content = re.findall(r">(.*?)<",content)

    res = []
    for item in content:
        if len(item)>2:
            res.append(item)
    return '\n'.join(res),html

def download_pic(paper_id,image_list):
    picture = []
    for i in range(len(image_list)):
        if 'http' not in image_list[i]['url']:
            url = 'http:'+image_list[i]['url']
        elif '?' in image_list[i]['url']:
            continue
        else:
            url = image_list[i]['url']
        response = requests.get(url,timeout=15)
        temp = url.split('/')[-1]
        temp = temp.split('.')
        if len(temp)<=2:
            filename = temp[0]+'.jpg'
        else:
            filename = temp[-2]+'.jpg'
        filename = paper_id+'_'+str(i)+'_'+filename
        picture.append(filename)
        with open(foldername+'/'+filename,'wb') as f:
            f.write(response.content)
    return ';'.join(picture) 


def main():
    try:
        toutiao_car()
    except:
        time.sleep(2)
        toutiao_car()
    toutiao_finance()
    toutiao_keji()
    # get_content('a6552467899489976836')

if __name__ == '__main__':
    main()