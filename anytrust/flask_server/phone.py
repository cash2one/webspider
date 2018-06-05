import requests
import time
import re
from lxml import etree
import json
import demjson

def baiduweishi_phone(phonenumber):
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://haoma.baidu.com/yellowPage',
        'Proxy-Connection': 'keep-alive',
    }

    params = (
        ('search', phonenumber),
        ('position', ''),
    )

    response = requests.get('http://haoma.baidu.com/phoneSearch', headers=headers, params=params)
    result = re.findall(r'<div class="upper_text">(.+?)</div>',response.text)
    res = []
    for item in result:
        res.append(item.replace('&nbsp;',''))
    # print(res)
    data = {}
    data['phone'] = re.findall(r'(\d{7,20})',res[1])[0]
    if u'电信' in res[0] or u'移动' in res[0] or u'联通' in res[0] or data['phone'][0]=='1':
        temp = res[0].split(' ')
        data['address'] = temp[0]
        data['operator'] = temp[1]
    else:
        data['address'] = res[0]
        data['operator'] = ''
    data['info'] = ''

    return data

def baidu_phone(phonenumber):
    data = {}
    data['phone'] =phonenumber
    m=re.findall(r"(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$",phonenumber)
    if not m:
        data['address'] = ''
        data['operator'] = ''
        data['info'] = u'没有找到该号码的信息'
        return data
    cookies = {
        'BAIDUID': '9FBB3DDF9C1043EC573390790B08EA9E:FG=1',
        'BIDUPSID': '9FBB3DDF9C1043EC573390790B08EA9E',
        'PSTM': '1523842582',
        'BD_UPN': '12314753',
        'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
        '__cfduid': 'dc50a3536ae2dfa84617d62f0ed220c001523846572',
        'ispeed_lsm': '0',
        'H_PS_PSSID': '26122_1435_21123_26181_20929',
        'BDSFRCVID': '2TtsJeC62CX4vEcAcJjB-qjKdfKmukvTH6aog4EkYtCMiBS4b8qhEG0PDx8g0Kubz7pbogKK0mOTHvbP',
        'H_BDCLCKID_SF': 'tJIDoIL2JC_3qn5zqROHhRIJhpo-KnLXKKOLV-_abPOkeq8CD6jHbT-tj4Q2BtTIH66BabbDWb6hVhc2y5jHhIuvKb6P3frmLb5MLC-hbPcpsIJMQh_WbT8U5fKL2lOzaKviaKJEBMb1fRoMe6Khj5O0jGujqb3HKC5XBRrjHDKaHPbvq4bohjnX3hOeBtQmJJrmhIbK3RONHpcFLCcaMxPOb4RL-4nqQg-q3R7jJp5OotbJXtrI0T0VehQ30x-jLgnOVn0MW-5DJC3x-4nJyUnQhtnnBn5aLnQ2QJ8BtKDaMC5P',
        'BD_CK_SAM': '1',
        'PSINO': '2',
        'BD_HOME': '0',
        'H_PS_645EC': '6a5foo0Pfc5LwgH8QJElAd9Bv4OrlQ7csmFlsRtZkXeLe%2BIpOF0Iol3JjNg',
        'BDSVRTM': '0',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }

    params = (
        ('ie', 'utf-8'),
        ('f', '8'),
        ('rsv_bp', '1'),
        ('rsv_idx', '1'),
        ('tn', 'baidu'),
        ('wd', phonenumber),
        ('oq', phonenumber),
        ('rsv_pq', 'c242fe8d0000d287'),
        ('rsv_t', 'a194q1p57q3UKhWcwjlBC4NRuKN/NJGkugOGv3zSP2Wjms+1Up/+qq7kQ3I'),
        ('rqlang', 'cn'),
        ('rsv_enter', '0'),
        ('inputT', '1489'),
        ('rsv_n', '2'),
        ('rsv_sug4', '1489'),
    )

    response = requests.get('http://www.baidu.com/s', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.text)
    result = selector.xpath('//*[@id="1"]/div/div[2]/div[1]/div/div[2]//text()')
    
    if not result:
        result = selector.xpath('//*[@id="1"]/div[1]/div/div[2]/div[1]//text()')
    res = []
    for i in result:
        res.append(i.strip())

    temp = '\n'.join(res).strip().replace(' ','').replace('\n',' ').replace('\xa0\xa0','  ') 
    # temp = re.sub(r'\xa0\xa0','  ',temp)
    temp = temp.split('  ')
    if len(temp)>=4:        
        data['address'] = temp[2]
        data['operator'] = ''
        data['info'] = temp[0]+';'+temp[3].strip()
    else:
        data['address'] = temp[1].replace('\xa0',' ')
        data['operator'] = temp[2]
        data['info'] = ''
    return data

def so360_phone(phonenumber):
    data = {}
    data['phone'] = phonenumber
    data['info'] = ''
    data['operator'] = ''
    data['address'] = ''
    cookies = {
        '__guid': '15484592.2475563352341483500.1523931217270.383',
        '__huid': '11O4PhDCUgFq4SCTMeu1dL8DpWfXr1g2fhm6j%2BLaqS0jo%3D',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q=13520449135',
        'Connection': 'keep-alive',
    }

    params = (
        ('callback', 'jQuery183008166310233889829_1523941291355'),
        ('query', phonenumber),
        ('url', 'mobilecheck'),
        ('num', '1'),
        ('type', 'mobilecheck'),
        ('src', 'onebox'),
        ('tpl', '1'),
    )

    response = requests.get('http://open.onebox.so.com/dataApi', headers=headers, params=params, cookies=cookies)
    a = response.text[:-1].replace('jQuery183008166310233889829_1523941291355(','').strip()
    if a == "''":
        data['info'] = u'没有找到该号码的信息'
        return data
    a = json.loads(a)
    result = re.findall(r'mh-detail">(.+?)</p>',a['html'],re.DOTALL)[0].replace('&nbsp;','').replace('\t','').replace('\n',' ')
    if '>' in result and '<' in result:
        result = ''.join(re.findall(r'>(.+?)<',result)[:-2])
    result = re.sub(r' {3,10}','  ',result).strip()  
    
    temp = result.split('  ')
    data['address'] = temp[1]
    if len(temp)>4:
        data['operator'] = temp[2]
        data['info'] = temp[3]+';'+temp[4]
    elif len(temp)==4 and data['phone'][0] != '1':
        data['operator'] = ''
        data['info'] = temp[2]+';'+temp[3]
    elif len(temp)==3:
        data['operator'] = temp[2]

    return data

def sogou_phnoe(phonenumber):

    data = {}
    data['phone'] = phonenumber
    data['info'] = ''
    cookies = {
        'SMYUV': '1523935966491178',
        'SUV': '00042B8A7C417F8E5AD56BEACA18A693',
        'ABTEST': '0|1524014679|v17',
        'IPLOC': 'CN1100',
        'SUID': '8E7F417C2013940A000000005AD69E57',
        'browerV': '3',
        'osV': '1',
        'sct': '1',
        'SNUID': 'E819271B66630D73357C9C7967A8125C',
        'sst0': '738',
        'ld': '9kllllllll2zCIiKlllllVrQXIylllllK9V@0kllllwlllll9klll5@@@@@@@@@@',
        'LSTMV': '616%2C343',
        'LCLKINT': '133956',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.sogou.com/',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }

    params = (
        ('query', phonenumber),
        ('_asf', 'www.sogou.com'),
        ('_ast', '1524014691'),
        ('w', '01019900'),
        ('p', '40040100'),
        ('ie', 'utf8'),
        ('from', 'index-nologin'),
        ('s_from', 'index'),
        ('sut', '3777'),
        ('sst0', '1524014690738'),
        ('lkt', '0,0,0'),
        ('sugsuv', '00042B8A7C417F8E5AD56BEACA18A693'),
    )

    response = requests.get('https://www.sogou.com/web', headers=headers, params=params, cookies=cookies)
    m=re.findall(r"(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$",phonenumber)
    if m:
        res = []
        res.append(re.findall(r"queryphoneinfo = '(.*?)：?\d?'.replace",response.text)[0]) 
        res.append(re.findall(r'"'+phonenumber+r'(.+?)"\)',response.text)[0].strip())
        data['info'] = res[0]
        if phonenumber[0] == '1' or u'电信' in res[1] or u'移动' in res[1] or u'联通' in res[1]:
            temp = res[1].split(' ')
            data['operator'] = temp[1]
            data['address'] = temp[0]
        else:
            data['operator'] = ''
            data['address'] = res[1]
    else:
        res = re.findall(r'tpl491\(491,(.+?)\);',response.text)
        if res:
            temp = res[0].split(',')[-1].replace('"','').split('\t')
            data['operator'] = ''
            data['address'] = temp[1]
        else:
            data['operator'] = ''
            data['address'] = ''
            data['info'] = u'没有找到该号码的信息'
    return data

def taobao_API(phonenumber):
    params = (
        ('tel', phonenumber),
    )
    response = requests.get('https://tcc.taobao.com/cc/json/mobile_tel_segment.htm', params=params)
    res = re.findall(r"carrier:'(.+?)'",response.text)
    data = {}
    data['phone'] = phonenumber
    data['info'] = ''
    data['operator'] = ''.join(re.findall(r"catName:'(.+?)'",response.text))
    data['address'] = ''.join(re.findall(r"province:'(.+?)'",response.text))
     
    return data

if __name__ == '__main__':
    phone = ['13520449134']
    for i in phone:
        print(baiduweishi_phone(i))
        # print(baidu_phone(i))
        # print(so360_phone(i))
        # print(sogou_phnoe(i))
        # print(taobao_API(i))
        print('***************************************')
