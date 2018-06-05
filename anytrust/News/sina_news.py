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
                filename='/ROOT/logs/sina_new.log',
                )
mysql = MySQLWrapper('db_spider')
foldername = '/ROOT/www/spider_pic/sina/'+time.strftime("%Y-%m-%d", time.localtime(time.time()))
if not os.path.exists(foldername):
    os.makedirs(foldername) 
top_time = time.strftime("%Y%m%d", time.localtime(time.time()))
def sina_keji():
    cookies = {
        'UOR': 'www.baidu.com,tech.sina.com.cn,',
        'SINAGLOBAL': '124.65.127.142_1524019116.251870',
        'lxlrtst': '1524018574_o',
        'U_TRS1': '0000000e.9b596696.5ad6b174.e0ad695d',
        'SUB': '_2AkMti4cKf8NxqwJRmPEWyWLmaIhwyAvEieKb13bRJRMyHRl-yD9jqmEFtRB6Bgup5YMNtB-TEyu-nkxXQWgGzwuU3Ky1',
        'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF35Qze6fUbJOG2MZ-LDWgD',
        'SGUID': '1524190832023_b7934c13',
        'vjuids': '59b6dafec.16300527dc2.0.a85630912c362',
        'Apache': '124.65.127.142_1525676778.569481',
        'ULV': '1525676782077:17:6:2:124.65.127.142_1525676778.569481:1525676778973',
        'lxlrttp': '1525444416',
        'U_TRS2': '0000008e.9dcdb64.5aeffaf2.189019d6',
        'hqEtagMode': '0',
        'vjlast': '1525678172',
        'ArtiFSize': '14',
        'rotatecount': '8',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://news.sina.com.cn/hotnews/',
        'Connection': 'keep-alive',
    }

    params = (
        ('top_type', 'day'),
        ('top_cat', 'tech_news_suda'),
        ('top_time', top_time),
        ('top_show_num', '20'),
        ('top_order', 'DESC'),
        ('js_var', 'channel_'),
    )

    response = requests.get('http://top.tech.sina.com.cn/ws/GetTopDataList.php', headers=headers, params=params, cookies=cookies)
    result = response.content.decode('utf-8').replace('var channel_ =','').strip()[:-1]
    res = json.loads(result)
    
    for item in res['data']:
        paper_id = item['url'].split('/')[-1].split('.')[0]
        title = item['title']
        tag = u'科技'
        author = item['author']
        paper_url = item['url']
        publish_time = item['create_date']+' '+item['create_time']
        comments_nums = item['top_num'].replace(',','')
        context,pics,label,content_html,channel,newsid = get_context(paper_url)
        if not context:
            continue
        participate_nums,comments_nums = get_nums(channel,newsid)
        image_list = download_pic(paper_id,pics)
        account = u'新浪'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_participate_nums,f_comments_nums,f_source,f_publish_time,f_image_list,f_label,f_paper_url)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,participate_nums,author,publish_time,image_list,label,paper_url)
        except pymysql.err.IntegrityError as e:
            pass
def sina_finance():

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://news.sina.com.cn/hotnews/',
        'Connection': 'keep-alive',
    }

    params = (
        ('top_type', 'day'),
        ('top_cat', 'finance_0_suda'),
        ('top_time', top_time),
        ('top_show_num', '20'),
        ('top_order', 'DESC'),
        ('js_var', 'channel_'),
    )

    response = requests.get('http://top.finance.sina.com.cn/ws/GetTopDataList.php', headers=headers, params=params)
    result = response.content.decode('utf-8').replace('var channel_ =','').strip()[:-1]
    res = json.loads(result)
    
    for item in res['data']:
        paper_id = item['url'].split('/')[-1].split('.')[0]
        title = item['title']
        tag = u'财经'
        author = item['author']
        paper_url = item['url']
        publish_time = item['create_date']+' '+item['create_time']
        context,pics,label,content_html,channel,newsid = get_context(paper_url)
        if not context:
            continue
        participate_nums,comments_nums = get_nums(channel,newsid)
        image_list = download_pic(paper_id,pics)
        account = u'新浪'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_participate_nums,f_comments_nums,f_source,f_publish_time,f_image_list,f_label,f_paper_url)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,participate_nums,author,publish_time,image_list,label,paper_url)
        except pymysql.err.IntegrityError as e:
            pass


def get_context(url):
    logging.info(url)
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://news.sina.com.cn/hotnews/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.content.decode(response.apparent_encoding))
    if selector.xpath('//*[@id="J_Article_Player"]'):
        return '','','','','',''
    html = selector.xpath('//*[@id="artibody"]')[0]
    html = etree.tostring(html, encoding=response.apparent_encoding)
    # html = re.sub(r'src= ?"http(.+?)"','{$image location$}',html)
    result = selector.xpath('//*[@id="artibody"]//p/text()')
    result = '\n'.join(result)
    
    picture = selector.xpath('//*[@id="artibody"]//*[@alt]/@src')
    label = ';'.join(selector.xpath('//*[@id="article-bottom"]/div[1]/a/text()')).replace(u'我要反馈','')

    channel = re.findall(r"channel: ?'(.+?)',",response.content.decode(response.apparent_encoding))[0]
    newsid = re.findall(r"newsid: ?'(.+?)',", response.content.decode(response.apparent_encoding))[0]


    return result,picture,label,html,channel,newsid

def get_nums(channel,newsid):

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    params = (
        ('channel', channel),
        ('newsid', newsid),
    )

    response = requests.get('http://comment5.news.sina.com.cn/page/info', headers=headers, params=params)
    res = response.json()
    return res['result']['count']['total'],res['result']['count']['show']


def download_pic(paper_id,image_list):
    picture = []
    for i in range(len(image_list)):
        if 'http' not in image_list[i]:
            url = 'http:'+image_list[i]
        elif '?' in image_list[i]:
            continue
        else:
            url = image_list[i]
        response = requests.get(url,timeout=15)
        temp = image_list[i].split('/')[-1]
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
    sina_finance()
    sina_keji()

if __name__ == '__main__':
    main()
