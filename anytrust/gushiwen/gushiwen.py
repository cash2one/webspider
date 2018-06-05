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

headers = {
    'authority': 'www.gushiwen.org',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'ASP.NET_SessionId=t3ibwr0or4gpbshfeolwlbl5; Hm_lvt_04660099568f561a75456483228a9516=1524207386; Hm_lpvt_04660099568f561a75456483228a9516=1524208096',
}

def shiwen(url,Category):
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    response = s.get(url, headers=headers)
    selector = etree.HTML(response.text)

    result = selector.xpath('/html/body/div[2]/div[1]/div[@class="sons"]')
    for item in result:
        Name = item.xpath('div[1]/p[1]/a/b/text()')[0]
        Dynasty = item.xpath('div[1]/p[2]/a[1]/text()')[0]
        if item.xpath('div[1]/p[2]/a[2]/text()'):
            Author = item.xpath('div[1]/p[2]/a[2]/text()')[0]
        else:
            Author = None
        Shiwen_id = item.xpath('div[1]/p[1]/a/@href')[0].split('/')[-1].split('.')[0]
        Content = ''.join(item.xpath('div[1]/div[2]//text()')).replace('。','。\n').strip()
        if item.xpath('div[2]/div[@class="good"]/a/span/text()'):
            Like_nums = item.xpath('div[2]/div[@class="good"]/a/span/text()')[0].strip()
        else:
            Like_nums = None
        a = ''
        for tag in item.xpath('div[@class="tag"]//text()'):
            a += tag.strip()
        Tags = a
        try:
            insert_sql = 'INSERT INTO m_media_gushiwen(Shiwen_id,Name,Dynasty,Author,Content,Tags,Like_nums,Category) Values(%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,Shiwen_id,Name,Dynasty,Author,Content,Tags,Like_nums,Category)
        except Exception as e:
            logging.error(e)
            logging.error('Insert shi error,name:%s',Name)


# #诗 1000页 
# for i in range(2,1001):
#     logging.info('shi %s pages',str(i))
#     time.sleep(10)
#     shiwen('https://www.gushiwen.org/shiwen/default_4A1A'+str(i)+'.aspx',u'诗')
#词 1000页 
# for i in range(801,1001):
#     logging.info('ci %s pages',str(i))
#     time.sleep(10)
#     shiwen('https://www.gushiwen.org/shiwen/default_4A2A'+str(i)+'.aspx',u'词')
# #曲 133页 
# for i in range(2,134):
#     logging.info('qu %s pages',str(i))
#     time.sleep(10)
#     shiwen('https://www.gushiwen.org/shiwen/default_4A3A'+str(i)+'.aspx',u'曲')

# #文 59页 
# for i in range(2,60):
#     logging.info('wen %s pages',str(i))
#     time.sleep(10)
#     shiwen('https://www.gushiwen.org/shiwen/default_4A4A'+str(i)+'.aspx',u'文言文') 

def mingju(page):

    params = (
        ('p', page),
        ('c', ''),
        ('t', ''),
    )

    response = requests.get('https://so.gushiwen.org/mingju/Default.aspx', headers=headers, params=params)
    selector = etree.HTML(response.text)

    result = selector.xpath('/html/body/div[2]/div[1]/div[2]/div')
    for item in result:
        Content = item.xpath('a[1]/text()')[0]
        a = item.xpath('a[2]/text()')[0]
        Name_Author = a
        b = a.split('《')
        Author = b[0]
        Name = '《'+b[1]
        

        insert_sql = 'INSERT INTO m_media_gushiwen_mingju(Name,Author,Content,Name_Author) Values(%s,%s,%s,%s)'
        mysql.execute(insert_sql,Name,Author,Content,Name_Author)


# #名句 200页 
# for i in range(1,201):
#     time.sleep(3)
#     logging.info(i)
#     mingju(str(i))

def zuozhe(page):

    headers = {
        'authority': 'so.gushiwen.org',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'Hm_lvt_04660099568f561a75456483228a9516=1524531675,1524621018,1526951571; ASP.NET_SessionId=mstib4zbljhp0pixrrsyz2iz; Hm_lpvt_04660099568f561a75456483228a9516=1526952460',
    }

    response = requests.get('https://so.gushiwen.org/author_'+page+'.aspx', headers=headers)
    selector = etree.HTML(response.text)
    if selector.xpath('//div[@class="sonspic"]/div[1]/h1/span[1]/b/text()'):
        author = selector.xpath('//div[@class="sonspic"]/div[1]/h1/span[1]/b/text()')[0]
    else:
        return

    # 简介
    if selector.xpath('//div[@class="sonspic"]/div[1]/p/text()'):
        intro = selector.xpath('//div[@class="sonspic"]/div[1]/p/text()')[0]
    else:
        intro = None

    # like
    if selector.xpath('//*[@id="agoodAuthor'+page+'"]/span/text()'):
        likenum = selector.xpath('//*[@id="agoodAuthor'+page+'"]/span/text()')[0]
        likenum = re.findall(r'(\d+)',likenum)[0]
    else:
        likenum = 0

    # image    
    if selector.xpath('//div[@class="sonspic"]/div[1]/div/img/@src'):
        image = selector.xpath('//div[@class="sonspic"]/div[1]/div/img/@src')[0]
        image = download_pic(image)
    else:
        image = None

    result = selector.xpath('//div[@class="contyishang"]')
    works = []
    anecdote = []
    achievement = []
    story = []
    commemorate = []
    life = []
    family = []
    other = []

    for item in result:
        if not item.xpath('div[2]/h2/span/text()'):
            title = item.xpath('div[1]/h2/span/text()')[0]
            if u'作品' in title:
                works.append(title)
                works.append(''.join(item.xpath('text()')).strip()[:-1])            
            elif u'典故' in title or u'轶闻' in title:
                anecdote.append(title)
                anecdote.append(''.join(item.xpath('text()')).strip()[:-1]) 
            elif u'成就' in title:
                achievement.append(title)
                achievement.append(''.join(item.xpath('text()')).strip()[:-1]) 
            elif u'故事' in title:
                story.append(title)
                story.append(''.join(item.xpath('text()')).strip()[:-1]) 
            elif u'纪念' in title:
                commemorate.append(title)
                commemorate.append(''.join(item.xpath('text()')).strip()[:-1]) 
            elif u'人物' in title:
                life.append(title)
                life.append(''.join(item.xpath('text()')).strip()[:-1]) 
            elif u'家庭' in title:
                family.append(title)
                family.append(''.join(item.xpath('text()')).strip()[:-1]) 
            else:
                other.append(title)
                family.append(''.join(item.xpath('text()')).strip()[:-1]) 
        else:
            title = item.xpath('div[2]/h2/span/text()')[0]
            sid = item.xpath('div[1]/@onclick')[0]
            sid = re.findall(r'(\d+)',sid)[0]

            if u'作品' in title:
                works.append(get_content(title,sid))             
            elif u'典故' in title or u'轶闻' in title:
                anecdote.append(get_content(title,sid))
            elif u'成就' in title:
                achievement.append(get_content(title,sid))
            elif u'故事' in title:
                story.append(get_content(title,sid))
            elif u'纪念' in title:
                commemorate.append(get_content(title,sid))
            elif u'人物' in title:
                life.append(get_content(title,sid))
            elif u'家庭' in title:
                family.append(get_content(title,sid))
            else:
                other.append(get_content(title,sid))

    works = '\n'.join(works)
    anecdote = '\n'.join(anecdote)
    achievement = '\n'.join(achievement)
    story = '\n'.join(story)
    commemorate = '\n'.join(commemorate)
    life = '\n'.join(life)
    family = '\n'.join(family)
    other  = '\n'.join(other)
    
    select_sql = 'SELECT * from t_Author where f_Author=%s'
    flag = mysql.fetchOne(select_sql,author)
    if flag:
        update_sql = 'UPDATE t_Author SET f_image=%s,f_author_likenum=%s,f_introduction=%s,f_anecdote=%s,f_family=%s,f_commemorate=%s,f_achievement=%s,f_life=%s,f_works=%s,f_story=%s,f_other=%s where f_Author=%s'
        mysql.execute(update_sql,image,likenum,intro,anecdote,family,commemorate,achievement,life,works,story,other,author)
    else:
        insert_sql = 'INSERT INTO t_Author(f_image,f_author_likenum,f_introduction,f_anecdote,f_family,f_commemorate,f_achievement,f_life,f_works,f_story,f_other,f_Author)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        mysql.execute(insert_sql,image,likenum,intro,anecdote,family,commemorate,achievement,life,works,story,other,author)

def download_pic(url):

    if 'http' not in url:
        url = 'http:'+url

    response = requests.get(url,timeout=15)
    temp = url.split('/')[-1]
    temp = temp.split('.')
    if len(temp)<=2:
        filename = temp[0]+'.jpg'
    else:
        filename = temp[-2]+'.jpg'

    with open(foldername+'/'+filename,'wb') as f:
        f.write(response.content)
    return filename


def get_content(title,sid):
    headers = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'accept': '*/*',
        'referer': 'https://so.gushiwen.org/authorv_85097dd0c645.aspx',
        'authority': 'so.gushiwen.org',
        'cookie': 'Hm_lvt_04660099568f561a75456483228a9516=1524531675,1524621018,1526951571; ASP.NET_SessionId=mstib4zbljhp0pixrrsyz2iz; Hm_lpvt_04660099568f561a75456483228a9516=1526955088',
    }

    params = (
        ('id', sid),
    )

    response = requests.get('https://so.gushiwen.org/authors/ajaxziliao.aspx', headers=headers, params=params)
    time.sleep(4)
    selector = etree.HTML(response.content.decode('utf-8'))
    length = len(selector.xpath('//div[@class="contyishang"]/p'))
    result = []
    if length:
        for i in range(1,length+1):
            content = ''.join(selector.xpath('//div[@class="contyishang"]/p['+str(i)+']//text()'))
            content = content.replace('\u3000\u3000','\n\u3000\u3000').replace('\n\n\u3000\u3000','\n\u3000\u3000').strip()
            result.append(content)
        result = [title]+result
    else:
        content = ''.join(selector.xpath('//div[@class="contyishang"]//text()'))
        content = content.replace('\u3000\u3000','\n\u3000\u3000').replace('\n\n\u3000\u3000','\n\u3000\u3000')
        result.append(content)

    return '\n'.join(result).strip()[:-1]

# print(get_content('369'))

#作者 3337页 
for i in range(161,3338):
    print(i)
    zuozhe(str(i))

def guwen(page):

    params = (
         ('p', '22'),
    )

    response = requests.get('https://so.gushiwen.org/guwen/Default.aspx', headers=headers, params=params)
    selector = etree.HTML(response.text)
    result = selector.xpath('/html/body/div[2]/div[1]/div[@class="sonspic"]')
    for item in result:
        print(item.xpath('div[1]/p[1]/a/b/text()')[0])
        print(item.xpath('div[1]/p[1]/a/@href')[0])
        print(item.xpath('div[1]/p[2]/text()')[0])
        print(item.xpath('div[2]/div[@class="good"]/a/span/text()')[0])
        if item.xpath('div[1]/div/a/img/@src'):
            print(item.xpath('div[1]/div/a/img/@src')[0])
        print('**************************************************')

# #作者 22页 
# for i in range(1,23):
#   guwen(str(i))