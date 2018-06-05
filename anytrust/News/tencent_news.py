import requests
import re
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import os
import time
from lxml import etree
import json
import pymysql
import chardet

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/tencent_new.log',
                )
mysql = MySQLWrapper('db_spider')
foldername = '/ROOT/www/spider_pic/tencent/'+time.strftime("%Y-%m-%d", time.localtime(time.time()))
if not os.path.exists(foldername):
    os.makedirs(foldername)
today = time.strftime("%Y-%m-%d", time.localtime(time.time()))

requests.adapters.DEFAULT_RETRIES = 8
s = requests.session()
s.keep_alive = False
headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://tech.qq.com/articleList/rolls/',
    'Connection': 'keep-alive',
}
s.get('http://news.qq.com/',headers=headers)
def tencent_keji():

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://tech.qq.com/articleList/rolls/',
        'Connection': 'keep-alive',
    }

    params = (
        ('site', 'tech'),
        ('mode', '1'),
        ('cata', ''),
        ('date', today),
        ('page', '1'),
        ('_', str(int(time.time()*1000))),
    )

    response = s.get('http://roll.news.qq.com/interface/cpcroll.php', headers=headers, params=params,timeout=15)
    if response.status_code != 200:
        response = s.get('http://roll.news.qq.com/interface/cpcroll.php', headers=headers, params=params,timeout=15)
    res = response.json()
    
    for item in res['data']['article_info']:
        temp = item['url'].split('/')
        paper_id = temp[-2]+temp[-1].split('.')[0]
        title = item['title']
        tag = u'科技'
        paper_url = item['url']
        publish_time = item['time']
        context,pics,label,source,comments_nums,content_html = get_context(paper_url)
        if not context:      
            continue
        image_list = download_pic(paper_id,pics)
        comments_nums = get_comment_nums(comments_nums)
        account = u'腾讯'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_publish_time,f_image_list,f_label,f_paper_url,f_source)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,publish_time,image_list,label,paper_url,source)
        except pymysql.err.IntegrityError as e:
            pass
def tencent_finance():

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://finance.qq.com/articleList/rolls/',
    }

    params = (
        ('site', 'finance'),
        ('mode', '1'),
        ('cata', ''),
        ('date', today),
        ('page', '1'),
        ('_', str(int(time.time()*1000))),
    )

    response = s.get('http://roll.news.qq.com/interface/cpcroll.php', headers=headers, params=params,timeout=15)
    if response.status_code != 200:
        response = s.get('http://roll.news.qq.com/interface/cpcroll.php', headers=headers, params=params,timeout=15)
    res = response.json()
    
    for item in res['data']['article_info']:
        temp = item['url'].split('/')
        paper_id = temp[-2]+temp[-1].split('.')[0]
        title = item['title']
        tag = u'财经'
        paper_url = item['url']
        publish_time = item['time']
        context,pics,label,source,comments_nums,content_html = get_context(paper_url)
        if not context:      
            continue
        image_list = download_pic(paper_id,pics)
        comments_nums = get_comment_nums(comments_nums)
        account = u'腾讯'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_publish_time,f_image_list,f_label,f_paper_url,f_source)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,publish_time,image_list,label,paper_url,source)
        except pymysql.err.IntegrityError as e:
            pass

def tencent_realty():

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://finance.qq.com/articleList/rolls/',
    }

    params = (
        ('site', 'house'),
        ('mode', '1'),
        ('cata', 'zonghe'),
        ('date', today),
        ('page', '1'),
        ('_', str(int(time.time()*1000))),
    )


    response = s.get('http://roll.news.qq.com/interface/cpcroll.php', headers=headers, params=params)
    if response.status_code != 200:
        response = s.get('http://roll.news.qq.com/interface/cpcroll.php', headers=headers, params=params)
    res = response.json()
    if not res['data']:
        return
    for item in res['data']['article_info']:
        temp = item['url'].split('/')
        paper_id = temp[-2]+temp[-1].split('.')[0]
        title = item['title']
        tag = u'房地产'
        paper_url = item['url']
        publish_time = item['time']
        context,pics,label,source,comments_nums,content_html = get_context(paper_url)
        if not context:      
            continue
        image_list = download_pic(paper_id,pics)
        comments_nums = get_comment_nums(comments_nums)
        account = u'腾讯'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_publish_time,f_image_list,f_label,f_paper_url,f_source)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,publish_time,image_list,label,paper_url,source)
        except pymysql.err.IntegrityError as e:
            pass

def tencent_car():

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://finance.qq.com/articleList/rolls/',
    }

    params = (
        ('site', 'auto'),
        ('mode', '1'),
        ('cata', 'industry'),
        ('date', today),
        ('page', '1'),
        ('_', str(int(time.time()*1000))),
    )

    response = s.get('http://roll.news.qq.com/interface/cpcroll.php', headers=headers, params=params)
    if response.status_code != 200:
        response = s.get('http://roll.news.qq.com/interface/cpcroll.php', headers=headers, params=params)
    res = response.json()
    if not res['data']:
        return
    for item in res['data']['article_info']:
        temp = item['url'].split('/')
        paper_id = temp[-2]+temp[-1].split('.')[0]
        title = item['title']
        tag = u'汽车'
        paper_url = item['url']
        publish_time = item['time']
        context,pics,label,source,comments_nums,content_html = get_context(paper_url)
        if not context:      
            continue
        image_list = download_pic(paper_id,pics)
        comments_nums = get_comment_nums(comments_nums)
        account = u'腾讯'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_publish_time,f_image_list,f_label,f_paper_url,f_source)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,publish_time,image_list,label,paper_url,source)
        except pymysql.err.IntegrityError as e:
            pass

def get_context(url):
    logging.info(url)
    headers = {
        'authority': 'finance.qq.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'referer': 'http://finance.qq.com/articleList/rolls/',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    response = s.get(url, headers=headers)
    try:
        selector = etree.HTML(response.content.decode(response.apparent_encoding))
    except:
        return '','','','','',''
    result = selector.xpath('//*[@id="Cnt-Main-Article-QQ"]//p//text()')
    if not result:
        result = selector.xpath('//*[@id="Cnt-Main-Article-QQ"]/text()')
    result = '\n'.join(result).strip()
    try:
        html = selector.xpath('//*[@id="Cnt-Main-Article-QQ"]')[0]
    except:
        return '','','','','',''
    html = etree.tounicode(html)
    # html = re.sub(r'src= ?"http(.+?)"','{$image location$}',html)
    picture = selector.xpath('//*[@id="Cnt-Main-Article-QQ"]/p//@src')
    label = ';'.join(selector.xpath('//*[@id="videokg"]/span/a/text()'))
    if selector.xpath('//*[@class="a_source"]/a/text()'):
        source = selector.xpath('//*[@class="a_source"]/a/text()')[0]
    else:
        source = ''.join(selector.xpath('//*[@class="a_source"]/text()'))
    try:
        num = re.findall(r'cmt_id = (\d+?);',response.content.decode(response.apparent_encoding))[0]
    except:
        return '','','','','',''
    return result,picture,label,source,num,html

def get_comment_nums(cid):

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://page.coral.qq.com/coralpage/comment/news.html',
        'Connection': 'keep-alive',
    }

    params = (
        ('_', str(int(time.time()*1000))),
    )
    response = s.get('http://coral.qq.com/article/'+cid+'/commentnum', headers=headers, params=params)
    return response.json()['data']['commentnum']

def download_pic(paper_id,image_list):
    picture = []
    for i in range(len(image_list)):
        if 'http' not in image_list[i]:
            url = 'http:'+image_list[i]
        elif '?' in image_list[i]:
            continue
        else:
            url = image_list[i]
        try:
            response = s.get(url,headers=headers,timeout=15)
        except:
            logging.error(url)
            response = s.get(url,headers=headers,timeout=15)
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
    tencent_finance()
    tencent_keji()
    tencent_realty()
    tencent_car()
    # get_context('http://house.qq.com/a/20180508/032863.htm')
    # get_comment_nums('2639024208')

if __name__ == '__main__':
    main()
