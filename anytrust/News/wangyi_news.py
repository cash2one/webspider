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

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/wangyi_new.log',
                )
mysql = MySQLWrapper('db_spider')
foldername = '/ROOT/www/spider_pic/wangyi/'+time.strftime("%Y-%m-%d", time.localtime(time.time()))
if not os.path.exists(foldername):
    os.makedirs(foldername) 

def wangyi_keji():
    headers = {
        'Referer': 'http://tech.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }


    response = requests.get('http://tech.163.com/special/00097UHL/tech_datalist_02.js', headers=headers)
    result = response.text.replace('data_callback(','')[:-1]
    result = json.loads(result)
    for item in result:
        if item['newstype'] == 'article' and item['label'] != u'其它':
            paper_id = item['docurl'].split('/')[-1].split('.')[0]
            title = item['title']
            tag = u'科技'
            paper_url = item['docurl']
            publish_time = item['time']
            label = item['label']
            for a in item['keywords']:
                label = label +';'+a['keyname']
            comments_nums = item['tienum']
            context,pic,author,content_html= get_context(paper_url)
            image_list = download_pic(paper_id,pic)
            avatar = ''
            account = u'网易'
            try:
                insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_source,f_publish_time,f_image_list,f_label,f_paper_url,f_avatar)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,author,publish_time,image_list,label,paper_url,avatar)
            except pymysql.err.IntegrityError as e:
                pass

def wangyi_finance():

    headers = {
        'Referer': 'http://money.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }

    response = requests.get('http://money.163.com/special/002557S5/newsdata_idx_index.js', headers=headers)
    result = response.text.replace('data_callback(','')[:-1]
    result = json.loads(result)
    for item in result:
        if item['newstype'] == 'article' and item['label'] != u'其它':
            paper_id = item['docurl'].split('/')[-1].split('.')[0]
            title = item['title']
            tag = u'财经'
            paper_url = item['docurl']
            publish_time = item['time']
            label = item['label']
            for a in item['keywords']:
                label = label +';'+a['keyname']
            comments_nums = item['tienum']
            context,pic,author,content_html= get_context(paper_url)
            image_list = download_pic(paper_id,pic)
            avatar = ''
            account = u'网易'
            try:
                insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_source,f_publish_time,f_image_list,f_label,f_paper_url,f_avatar)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,author,publish_time,image_list,label,paper_url,avatar)
            except pymysql.err.IntegrityError as e:
                pass
def wangyi_realty():

    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://bj.house.163.com/special/0007426Q/rollnews.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get('http://bj.house.163.com/special/0007426Q/rollnews.html', headers=headers)
    selector = etree.HTML(response.content.decode('gbk'))
    result = selector.xpath('//div[@class="list-item clearfix"]')
    for item in result:
        paper_id = item.xpath('h2/a/@href')[0].split('/')[-1].split('.')[0]
        title = item.xpath('h2/a/text()')[0]
        tag = u'房地产'
        paper_url = item.xpath('h2/a/@href')[0]
        publish_time = item.xpath('p/span/text()')[0]
        label = ''
        context,pic,author,comments_nums,content_html= get_context_only(paper_url)
        image_list = download_pic(paper_id,pic)
        avatar = ''
        account = u'网易'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_source,f_publish_time,f_image_list,f_label,f_paper_url,f_avatar)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,author,publish_time,image_list,label,paper_url,avatar)
        except pymysql.err.IntegrityError as e:
            pass

    response = requests.get('http://bj.house.163.com/special/0007426Q/rollnews_02.html', headers=headers)
    selector = etree.HTML(response.content.decode('gbk'))
    result = selector.xpath('//div[@class="list-item clearfix"]')
    for item in result:
        paper_id = item.xpath('h2/a/@href')[0].split('/')[-1].split('.')[0]
        title = item.xpath('h2/a/text()')[0]
        tag = u'房地产'
        paper_url = item.xpath('h2/a/@href')[0]
        publish_time = item.xpath('p/span/text()')[0]
        label = ''
        context,pic,author,comments_nums,content_html= get_context_only(paper_url)
        image_list = download_pic(paper_id,pic)
        avatar = ''
        account = u'网易'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_source,f_publish_time,f_image_list,f_label,f_paper_url,f_avatar)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,author,publish_time,image_list,label,paper_url,avatar)
        except pymysql.err.IntegrityError as e:
            pass

def wangyi_car():
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'X-DevTools-Emulate-Network-Conditions-Client-Id': '58058A668D4251D689C569937B29B878',
        'Referer': 'http://auto.163.com/special/2016carnews/',
    }

    response = requests.get('http://auto.163.com/news/', headers=headers)
    selector = etree.HTML(response.content.decode('gbk'))
    result = selector.xpath('//*[@id="auto_pull_dataset"]/div')
    for item in result:
        paper_id = item.xpath('div/h3/a/@href')[0].split('/')[-1].split('.')[0]
        title = item.xpath('div/h3/a/text()')[0]
        tag = u'汽车'
        paper_url = item.xpath('div/h3/a/@href')[0]
        publish_time = item.xpath('div/div[2]/span[1]/text()')[0]
        label = ';'.join(item.xpath('div/div[1]/a/text()'))
        comments_nums = item.xpath('div/div[2]/span[2]/text()')[0]
        context,pic,author,content_html= get_context(paper_url)
        image_list = download_pic(paper_id,pic)
        avatar = ''
        account = u'网易'
        try:
            insert_sql = 'INSERT INTO m_media_news(f_account,f_paper_id,f_title,f_tag,f_content,f_content_html,f_comments_nums,f_source,f_publish_time,f_image_list,f_label,f_paper_url,f_avatar)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,account,paper_id,title,tag,context,content_html,comments_nums,author,publish_time,image_list,label,paper_url,avatar)
        except pymysql.err.IntegrityError as e:
            pass

def get_context(url):
    logging.info(url)
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://tech.163.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.content.decode('gbk'))
    length = len(selector.xpath('//*[@id="endText"]/p'))
    result = selector.xpath('//*[@id="endText"]')[0]
    html = etree.tounicode(result)
    # html = re.sub(r'src= ?"http(.+?)"','{$image location$}',html)
    text = []
    for i in range(length):
        text.append(''.join(result.xpath('p['+str(i)+']//text()')))

    result = '\n'.join(text).replace('\n\n','\n').strip()
    author = get_author(selector)
    picture = selector.xpath('//*[@id="endText"]//@src')
    for pic in picture:
        if u'/css13/'in pic:
            picture.remove(pic)
    return result,picture,author,html

def get_context_only(url):
    logging.info(url)
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://tech.163.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.content.decode('gbk'))
    length = len(selector.xpath('//*[@id="endText"]/p'))
    result = selector.xpath('//*[@id="endText"]')[0]
    html = etree.tounicode(result)
    # html = re.sub(r'src= ?"http(.+?)"','{$image location$}',html)
    text = []
    for i in range(length):
        text.append(''.join(result.xpath('p['+str(i)+']//text()')))
    author = get_author(selector)
    result = '\n'.join(text).replace('\n\n','\n').strip()
    picture = selector.xpath('//*[@id="endText"]//@src')
    for pic in picture:
        if u'/css13/'in pic:
            picture.remove(pic)
    if selector.xpath('//*[@id="post_comment_area"]/div[2]/div[3]/a/text()'): 
        nums = selector.xpath('//*[@id="post_comment_area"]/div[2]/div[3]/a/text()')[0]+selector.xpath('//*[@id="post_comment_area"]/div[2]/div[2]/a/text()')[0]
    else:
        nums = 0
        
    return result,picture,author,nums,html
def get_author(selector):
    author = selector.xpath('//*[@id="endText"]/div[4]/span[1]/text()')
    if not author:
        author = selector.xpath('//*[@id="endText"]/div[3]/span[1]/text()')
    if not author:
       author = selector.xpath('//*[@id="endText"]/div[2]/span[1]/text()') 
    author = ' '.join(author).strip()
    author = author.replace(u'本文来源：','')
    return author
def download_pic(paper_id,image_list):
    picture = []
    for i in range(len(image_list)):
        if 'http' not in image_list[i]:
            url = 'http:'+image_list[i]
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
    wangyi_keji()
    wangyi_finance()
    wangyi_realty()
    wangyi_car()
    
    # get_context('http://tech.163.com/18/0508/09/DH9AHTG200097U7R.html')

if __name__ == '__main__':
    main()
