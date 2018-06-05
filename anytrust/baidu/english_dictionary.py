import requests
from lxml import etree
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper
import logging
import time
import re

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/word.log',
                )
mysql = MySQLWrapper('db_spider')

sys.setrecursionlimit(50000) #例如这里设置为一百万   
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False

MAP_WORD={
    'word_adj':u'形容词',
    'word_adv':u'副词',
    'word_conn':u'连接词',
    'word_done':u'过去分词',
    'word_er':u'比较级',
    'word_est':u'最高级',
    'word_ing':u'现在分词',
    'word_noun':u'名词',
    'word_past':u'过去式',
    'word_pl':u'复数',
    'word_prep':u'介词',
    'word_third':u'第三人称单数',
    'word_verb':u'动词',
}


def get_word_info(word):
    logging.info(word)
    select_sql = 'SELECT * FROM m_media_english_word WHERE f_word=%s'

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Referer': 'http://www.iciba.com/break',
        'X-Requested-With': 'XMLHttpRequest',

    }

    params = (
        ('a', 'getWordMean'),
        ('c', 'search'),
        ('word', word),
    )

    response = s.get('http://www.iciba.com/index.php', headers=headers, params=params)
    res = response.json()
    if 'baesInfo' not in res.keys() or 'symbols' not in res['baesInfo'].keys():
        return
    # 美国音标
    ph_am = res['baesInfo']['symbols'][0]['ph_am']
    # 英国音标
    ph_en = res['baesInfo']['symbols'][0]['ph_en']
    # 汉语释义
    temp = res['baesInfo']['symbols'][0]['parts']
    word_meaning = []
    for item in temp: 
        word_meaning.append(item['part']+' '+';'.join(item['means']))

    word_zh = '\n'.join(word_meaning)

    # 变形
    exchange = []
    temp = res['baesInfo']['exchange']
    for key in temp.keys():
        if temp[key]:
            exchange.append(MAP_WORD[key]+':'+';'.join(temp[key]))

    exchange = ';'.join(exchange)
    # 标签
    # tags = get_tags(word)
    tags = ''
    # 例句
    # sentence = [{例1},{例2},{例3},...]
    # {例1}={
    # Network_cn:"记住：保持乐观的心态，好事自然会发生。"  
    # Network_en : "Remember, keep a positive attitude and good things will happen."
    # Network_id : "2264505"
    # source_id:0
    # source_title:"普通双语例句"
    # source_type :0
    # tts_mp3:"http://res-tts.iciba.com/tts_new_dj//dailysentence/2014-05-13.mp3"
    # tts_size:"25K"}

    sentence = str(res.get('sentence',''))
    # 句式用法
    # sentence = [{例1},{例2},{例3},...]
    # {例1}={
    # chinese:"记住：保持乐观的心态，好事自然会发生。"  
    # english : "Remember, keep a positive attitude and good things will happen."
    # mp3:"http://res-tts.iciba.com/tts_new_dj//dailysentence/2014-05-13.mp3"}
    jushi = str(res.get('jushi',''))
    # 权威例句
    # sentence = [{例1},{例2},{例3},...]
    # cache_status: "1"
    # content:"Several species being replaced by one is never good."
    # diff:"2"
    # id:"1009"
    # link:"http://www.bbc.co.uk/news/magazine-18672728"
    # oral:"0"
    # res_content:"Several species being replaced by one is never <b>good</b>."
    # res_content_con:"Several species being replaced by one is never good."
    # res_key:"21a5ab0b748eafea2978f3070375b59a"
    # score:"1"
    # short_link:"http://www.bbc.co.uk/jza23"
    # source:"BBC"
    # source_id:0
    # source_title:"普通权威例句"
    # source_type:0
    # tts_mp3:"http://res-tts.iciba.com/tts_authority/2/1/a/21a5ab0b748eafea2978f3070375b59a.mp3"
    # tts_size:"17.0"
    auth_sentence = str(res.get('auth_sentence',None))
    # 柯林斯高阶英汉双解学习词典
    # sentence = [{例1},{例2},{例3},...]
    # def:"Good means pleasant or enjoyable."
    # example:[
    #     0:{
    #         ex:"We had a really good time together..."
    #         tran:"我们一起玩得真痛快。"
    #         tts_mp3:"http://res-tts.iciba.com/tts_dj/e/8/4/e84dbefbf104b00dba31cd1b82f781d4.mp3"
    #         tts_size:"10K"
    #     }
    #     1:{ex: "I know they would have a better life here...", tran: "我知道他们在这里会生活得更好。",…}
    # posp:"ADJ-GRADED"
    # tran:"愉快的；有趣的；令人愉快的"
    if 'collins' in res.keys():
        collins = str(res['collins'][-1]['entry'])
    else:
        collins = None
    # 四级
    cetFour = res.get('cetFour',None)
    if cetFour:
        # cetFour_json = [{例1},{例2},{例3},...]
        # me:"出自-2014年6月听力原文"  
        # sentence: 
        cetFour_json = str(cetFour['Sentence'])
        cetFour_nums = cetFour['count']
    else:
        cetFour_json = None
        cetFour_nums = None
    # 六级
    cetSix = res.get('cetFour',None)
    if cetSix:
        # cetSix_json = [{例1},{例2},{例3},...]
        # me:"出自-2014年6月听力原文"  
        # sentence: 
        cetSix_json = str(cetSix['Sentence'])
        cetSix_nums = cetSix['count']
    else:
        cetSix_json = None
        cetSix_nums = None
    # 词组搭配
    #     cizu_name:"all to the good"
    # jx:[{jx_en_mean: "to be welcomed without qualification", jx_cn_mean: "无条件地受到欢迎", lj: []}]
    phrase = str(res.get('phrase',''))
    # 百科
    encyclopedia = res.get('encyclopedia',None)
    if encyclopedia:
        encyclopedia = res['encyclopedia']['content']
    flag = mysql.fetchOne(select_sql,word)
    if not flag:
        insert_mysql = 'INSERT INTO m_media_english_word(f_word,f_ph_am,f_ph_en,f_word_zh,f_exchange,f_tags,f_cetFour,f_cetFour_nums,f_cetSix,f_cetSix_nums,f_sentence,f_jushi,f_auth_sentence,f_collins,f_phrase,f_encyclopedia)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        mysql.execute(insert_mysql,word,ph_am,ph_en,word_zh,exchange,tags,cetFour_json,cetFour_nums,cetSix_json,cetSix_nums,sentence,jushi,auth_sentence,collins,phrase,encyclopedia)

    next_words = re.findall(r'[a-z]+',res['sentence'][-1]['Network_en'].lower())

    for next_word in next_words:
        flag = mysql.fetchOne(select_sql,next_word)
        if not flag:
            time.sleep(10)
            get_word_info(next_word)


   
def get_tags(word):


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.iciba.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get('http://www.iciba.com/'+word, headers=headers)
    selector = etree.HTML(response.text)
    temp = []
    for item in selector.xpath('//div[@class="base-level"]/p/span/text()'):
        temp.append(item.replace('\xa0/','').strip())
    return ';'.join(temp)


if __name__ == '__main__':
    get_word_info('replace')




