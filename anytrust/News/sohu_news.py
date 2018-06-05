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
                filename='/ROOT/logs/sohu_new.log',
                )
mysql = MySQLWrapper('db_spider')
foldername = '/ROOT/www/spider_pic/sohu/'+time.strftime("%Y-%m-%d", time.localtime(time.time()))
if not os.path.exists(foldername):
    os.makedirs(foldername)
today = time.strftime("%Y-%m-%d", time.localtime(time.time()))

def sohu_keji():

    cookies = {
        'SUV': '1804161104523719',
        'IPLOC': 'CN1100',
        'gidinf': 'x099980109ee0daf482328c23000e7ee9c44449b8a3b',
        'ppinf': '2|1524625801|1525835401|bG9naW5pZDowOnx1c2VyaWQ6Mjc6OTg4OTc4NDA4MTE1NjIxODg4QHNvaHUuY29tfHNlcnZpY2V1c2U6MzA6MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwfGNydDoxMDoyMDE4LTA0LTI1fGVtdDoxOjB8YXBwaWQ6NjoxMDEzMDV8dHJ1c3Q6MToxfHBhcnRuZXJpZDoxOjB8cmVsYXRpb246MDp8dXVpZDoxNjpzYzBjMDlkZTIxZTVlZWYwfHVpZDoxNjpzYzBjMDlkZTIxZTVlZWYwfHVuaXFuYW1lOjA6fA',
        'pprdig': 'IWJPTf1oqTpyoJ-7cYZlIWMcTZCsuTp3CKgVigA9NIbeShLFGc74Q8pOUtnmQkajbRx1fRilhARZ8EB6BDgi2DFJxjrdOMGpwfxj1MA--OfhMfmI0oBOYBfGm4FLTJi7Kn6EeLUqvQpkespx5gos7nOGkWAXU9CAFxg6CCeQHH8',
        'mailinfo': '988978408115621888@sohu.com:python_warning@sohu.com:6afaa3ba8ce93017f22d836d62c7834d',
        'reqtype': 'pc',
        'ppmdig': '152577456000000042cd58469ec4b1646b34fdd69d5df4fd',
        't': '1525774570575',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://it.sohu.com/',
        'Connection': 'keep-alive',
    }

    params = (
        ('scene', 'CHANNEL'),
        ('sceneId', '30'),
        ('page', '1'),
        ('size', '20'),
    )

    response = requests.get('http://v2.sohu.com/public-api/feed', headers=headers, params=params, cookies=cookies)
    res = response.json()
    for item in res:
        paper_id = str(item['id'])
        title = item['title']
        tag = u'科技'
        label = []
        for a in item['tags']:
            label.append(a['name'])

        label = ';'.join(label)
        paper_url = 'http://www.sohu.com/a/'+paper_id+'_'+str(item['authorId'])        
        publish_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item['publicTime']//1000))
        source = item['authorName']       
        content,pics,content_html = get_context(paper_url)
        if not content:      
            continue
        read_nums = get_read_nums(paper_id)
        comments_nums,participate_nums = get_comment_nums(paper_id)
        
        image_list = download_pic(paper_id,pics)
        avatar = item['picUrl']
        account = u'搜狐'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_read_nums,f_participate_nums,f_publish_time,f_image_list,f_label,f_paper_url,f_source)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,content,content_html,comments_nums,read_nums,participate_nums,publish_time,image_list,label,paper_url,source)
        except pymysql.err.IntegrityError as e:
            pass
    
def sohu_finance():
    cookies = {
        'SUV': '1804161104523719',
        'IPLOC': 'CN1100',
        'gidinf': 'x099980109ee0daf482328c23000e7ee9c44449b8a3b',
        'reqtype': 'pc',
        't': '1525929116181',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://business.sohu.com/',
        'Connection': 'keep-alive',
    }

    params = (
        ('scene', 'CHANNEL'),
        ('sceneId', '15'),
        ('page', '1'),
        ('size', '20'),
    )

    response = requests.get('http://v2.sohu.com/public-api/feed', headers=headers, params=params, cookies=cookies)
    res = response.json()
    for item in res:
        paper_id = str(item['id'])
        title = item['title']
        tag = u'财经'
        label = []
        for a in item['tags']:
            label.append(a['name'])

        label = ';'.join(label)
        paper_url = 'http://www.sohu.com/a/'+paper_id+'_'+str(item['authorId'])        
        publish_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item['publicTime']//1000))
        source = item['authorName']       
        content,pics,content_html = get_context(paper_url)
        if not content:      
            continue
        read_nums = get_read_nums(paper_id)
        comments_nums,participate_nums = get_comment_nums(paper_id)
        
        image_list = download_pic(paper_id,pics)
        avatar = item['picUrl']
        account = u'搜狐'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_read_nums,f_participate_nums,f_publish_time,f_image_list,f_label,f_paper_url,f_source)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,content,content_html,comments_nums,read_nums,participate_nums,publish_time,image_list,label,paper_url,source)
        except pymysql.err.IntegrityError as e:
            pass

def sohu_realty():
    cookies = {
        'focus_pc_city_p': 'house',
        'focus_city_p': 'house',
        'focus_city_c': '110100',
        'focus_city_s': 'bj',
        'pc_ad_feed': '0',
        'sohu_CID': '1804161104523719',
        'IPLOC': 'CN1100',
        'SUV': '180510132229U8OD',
        'ad_strw': '2e',
        'gr_user_id': '807bfdb3-14b2-48fe-ab65-234c662a2c8b',
        'gr_session_id_87a4bcbf0b1ea517': '905acbdb-8727-4311-85ef-2841d6f3f400_true',
        'focusbels': '1',
    }

    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://house.focus.cn/zixun/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get('https://house.focus.cn/zixun', headers=headers, cookies=cookies)
    selector = etree.HTML(response.text)
    res = selector.xpath('//*[@id="bd-left"]/div[1]/ul/li')

    for item in res:
        paper_url = item.xpath('div/a/@href')[0]
        paper_id = paper_url.split('/')[-1].split('.')[0]
        title = item.xpath('div/a/@title')[0]
        tag = u'房地产'
        source = item.xpath('div/p/a[2]/text()')[0]
        publish_time = item.xpath('div/p/span[1]/text()')[0]
        
        label = None
                
        content,pics,content_html,topic_source_id = get_context_only(paper_url)
        if not content:      
            continue
        read_nums = None
        comments_nums,participate_nums = get_comment_nums_only('cy2zl3dw1MzA',paper_url,topic_source_id)
        
        image_list = download_pic(paper_id,pics)
        avatar = None
        account = u'搜狐'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_read_nums,f_participate_nums,f_publish_time,f_image_list,f_label,f_paper_url,f_source)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,content,content_html,comments_nums,read_nums,participate_nums,publish_time,image_list,label,paper_url,source)
        except pymysql.err.IntegrityError as e:
            pass

def sohu_car():


    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://auto.sohu.com/qichexinwen.shtml',
        'Connection': 'keep-alive',
    }



    response = requests.get('http://api.db.auto.sohu.com/restful/news/list/news/3/20.json', headers=headers)
    res = response.json()
    for item in res['result']:
        paper_id = str(item['id'])
        title = item['title']
        tag = u'汽车'        
        paper_url = item['url']     
        publish_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item['pbdate']//1000))
        content,pics,content_html = get_context_car(paper_url)
        if not content:      
            continue
        source = item['media'] 
        label = ''
        topic_source_id = paper_url.split('/')[-1].split('.')[0][1:]     
        read_nums = get_read_nums(paper_id)
        comments_nums,participate_nums = get_comment_nums_only('cyqemw6s1',paper_url,topic_source_id)
        
        image_list = download_pic(paper_id,pics)
        avatar = ''
        account = u'搜狐'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_read_nums,f_participate_nums,f_publish_time,f_image_list,f_label,f_paper_url,f_source)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,content,content_html,comments_nums,read_nums,participate_nums,publish_time,image_list,label,paper_url,source)
        except pymysql.err.IntegrityError as e:
            pass

def get_context(url):
    logging.info(url)
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)

    html = selector.xpath('//*[@id="mp-editor"]')[0]
    html = etree.tounicode(html)
    # html = re.sub(r'src= ?"http(.+?)"','{$image location$}',html)
    result = selector.xpath('//*[@id="mp-editor"]//p/text()')
    result = '\n'.join(result)

    picture = selector.xpath('//*[@id="mp-editor"]//@src')

    return result,picture,html

def get_read_nums(cid):

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://www.sohu.com/a/230884417_797912',
    }


    response = requests.get('http://v2.sohu.com/public-api/articles/'+cid+'/pv', headers=headers)
    return response.text

def get_comment_nums(cid):
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
    }

    params = (
        ('page_size', '10'),
        ('topic_id', '4618771'),
        ('page_no', '2'),
        ('source_id', 'mp_'+cid),
    )

    response = requests.get('http://apiv2.sohu.com/api/topic/load', headers=headers, params=params)
    result = response.json()
    if not result['jsonObject']:
        return 0,0
    comments_nums = result['jsonObject']['cmt_sum']
    participate_nums = result['jsonObject']['participation_sum']
    return comments_nums,participate_nums

def get_context_only(url):
    logging.info(url)
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)
    html = selector.xpath('//*[@id="bd-left"]/div[2]/div[1]/div[3]')[0]
    html = etree.tounicode(html)
    # html = re.sub(r'src= ?"http(.+?)"','{$image location$}',html)
    result = selector.xpath('//*[@id="bd-left"]/div[2]/div[1]/div[3]//p/text()')
    result = '\n'.join(result).strip()  
    picture = selector.xpath('//*[@id="bd-left"]/div[2]/div[1]/div[3]//@src')
    topic_source_id = selector.xpath('//*[@id="bd-left"]/div[2]/@data-news_id')[0]
    return result,picture,html,topic_source_id

def get_comment_nums_only(client_id,url,topic_source_id):
    headers = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'accept': '*/*',
        'authority': 'changyan.sohu.com',
     }

    params = (
        ('client_id', client_id),
        ('topic_url', url),
        ('page_size', '5'),
        ('hot_size', '5'),
        ('topic_source_id', topic_source_id),
    )

    response = requests.get('https://changyan.sohu.com/api/3/topic/liteload', headers=headers, params=params)
    result = response.json()
    comments_nums = result['cmt_sum']
    participate_nums = result['participation_sum']
    return comments_nums,participate_nums

def get_context_car(url):
    logging.info(url)
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://auto.sohu.com/qichexinwen.shtml',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.content.decode('gbk'))
    html = selector.xpath('//*[@id="contentText"]')[0]
    html = etree.tounicode(html)

    result = selector.xpath('//*[@id="contentText"]')[0]
    text = []
    length = len(selector.xpath('//*[@id="contentText"]/p'))


    for i in range(1,length+1):
        text.append(''.join(result.xpath('p['+str(i)+']//text()')))

    result = '\n'.join(text).strip() 

    picture = selector.xpath('//*[@id="contentText"]//@src')
    return result,picture,html

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
    sohu_keji()
    sohu_finance()
    sohu_realty()
    sohu_car()
    # get_context_car('http://auto.sohu.com/20171229/n526698930.shtml')
    # print(get_context_only('https://house.focus.cn/zixun/51aa9a1d62ae76fb.html'))
    # print(get_comment_nums_only('https://house.focus.cn/zixun/6a46db1e083230ed.html'))
    # get_context('http://www.sohu.com/a/230884417_797912')
    # print(get_read_nums('230884417'))
    # print(get_comment_nums('231029898'))

if __name__ == '__main__':
    main()
