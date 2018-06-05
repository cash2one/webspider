import requests
from lxml import etree
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import time
import jieba
import pickle
import re

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/zici.log',
                )
mysql = MySQLWrapper('db_spider')
  
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False


def get_info(word): 
    select_sql = 'SELECT * FROM m_media_ciyu WHERE f_Word=%s'
    res = mysql.fetchOne(select_sql,word)
    if res:
        return

    cookies = {
        'BAIDUID': '9FBB3DDF9C1043EC573390790B08EA9E:FG=1',
        'BIDUPSID': '9FBB3DDF9C1043EC573390790B08EA9E',
        'PSTM': '1523842582',
        '__cfduid': 'dc50a3536ae2dfa84617d62f0ed220c001523846572',
        'MCITY': '-131%3A',
        'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
        'H_PS_PSSID': '1435_21123_26309_26181_20929',
        'PSINO': '2',
        'Hm_lvt_010e9ef9290225e88b64ebf20166c8c4': '1525246073',
        'Hm_lpvt_010e9ef9290225e88b64ebf20166c8c4': '1525246084',
    }

    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://hanyu.baidu.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    params = (
        ('wd', word),
        ('ptype', 'zici'),
    )

    response = s.get('https://hanyu.baidu.com/s', headers=headers, params=params, cookies=cookies)
    try:
        res = response.content.decode(response.apparent_encoding)
    except:
        return
    if u'抱歉：百度汉语中没有收录' in res:
        logging.error('no this word :%s',word)
        return
    selector = etree.HTML(res)

    if selector.xpath('//*[@id="pinyin"]/h2/span/b/text()'):
        word_pinyin = selector.xpath('//*[@id="pinyin"]/h2/span/b/text()')[0]
    else:
        logging.info(word)
        return 
    # 基本释义
    if selector.xpath('//*[@id="basicmean-wrapper"]/div[1]/dl/dd/p/text()'):
        basic_info = '\n'.join(selector.xpath('//*[@id="basicmean-wrapper"]/div[1]/dl/dd/p/text()')).strip()
    else:
        basic_info = None
    # 详细释义
    a = selector.xpath('//*[@id="detailmean-wrapper"]/div[1]/dl/dd/ol/li')
    detailed_info = []
    for item in a :
        detailed_info.append('@@@'.join(item.xpath('p/text()')))

    detailed_info = '\n'.join(detailed_info).strip()
    #近义词
    if selector.xpath('//*[@id="synonym"]/div/a/text()'):
        word_similar = ','.join(selector.xpath('//*[@id="synonym"]/div/a/text()'))
    else:
        word_similar = None
    #反义词
    if selector.xpath('//*[@id="antonym"]/div/a/text()'):
        word_opposite = ','.join(selector.xpath('//*[@id="antonym"]/div/a/text()'))
    else:
        word_opposite = None

    # baike
    if selector.xpath('//*[@id="baike-wrapper"]/div[2]/p/text()'):
        baike_info = selector.xpath('//*[@id="baike-wrapper"]/div[2]/p/text()')[0].strip()
    else:
        baike_info = None

    #英文翻译
    if selector.xpath('//*[@id="fanyi-wrapper"]/div/dl/dt/text()'):
        word_en = selector.xpath('//*[@id="fanyi-wrapper"]/div/dl/dt/text()')[0]
    else:
        word_en = None

    insert_sql = 'INSERT INTO m_media_ciyu(f_Word,f_Word_Pinyin,f_Basic_Info,f_Detailed_Info,f_Word_Similar,f_Word_Opposite,f_Word_EN,f_Baike_info)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    mysql.execute(insert_sql,word,word_pinyin,basic_info,detailed_info,word_similar,word_opposite,word_en,baike_info)
    return True
 
def get_word():
    select_sql = 'SELECT f_content FROM m_media_news WHERE TO_DAYS(NOW())-TO_DAYS(create_time) <= 1'
    data = mysql.fetchAll(select_sql)
    with open('stopwords.pkl','rb') as f:
        stopwords = pickle.load(f)
    for res in data:
        result = re.sub(r'\d+\.?\d*%?','',res['f_content'])
        text = jieba.cut(result)       
        for word in text:  
            if word not in stopwords and len(word)>=2: 
                if get_info(word):
                    time.sleep(2)
    

if __name__ == '__main__':  
    get_word()