import time
import json
import requests
from lxml import etree

def baidu_code(code):
    cookies = {
        'BAIDUID': '9FBB3DDF9C1043EC573390790B08EA9E:FG=1',
        'BIDUPSID': '9FBB3DDF9C1043EC573390790B08EA9E',
        'PSTM': '1523842582',
        'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
        '__cfduid': 'dc50a3536ae2dfa84617d62f0ed220c001523846572',
        'BDSFRCVID': 'jdusJeC626l-GuTAcZPA-qjKdS1c_r3TH6aIoeU9A2gMFLesYaI6EG0PqM8g0KubLu7UogKK0mOTHU7P',
        'H_BDCLCKID_SF': 'tJAHVCtatD_3fP36qRbo5tk_hpJK2t-XKKOLVbONX-Okeq8CD4r45b0hXPQ2aRcNH66BabbHJ4nZjfo2y5jH36tEXHuO3fvgyRP80RobJqbpsIJMKfFWbT8U5f5KQqJNaKviaKJEBMb1SD3Me6K5D55bjaA8q-6-bITKQbK82RC3jRbGKU6qLT5XjxkL0bQn0C7zbpDE-RcveM8l-pnKDp0njxQA2-QPfmCH0h6IBn55oJjVjxonDh8LXH7MJUntKeJt_M5O5hvvhb6O3M7ljpOh-p52f6_jJJkJ3j',
        'H_PS_PSSID': '26122_1435_21123_26181_20929',
        'PSINO': '2',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }

    params = (
        ('wd', code),
    )

    response = requests.get('http://opendata.baidu.com/post/s', headers=headers, params=params, cookies=cookies)
    selector = etree.HTML(response.content.decode('gbk'))
    if selector.xpath('/html/body/section/article[1]/h3/text()'):
        res = selector.xpath('/html/body/section/article[1]/h3/text()')[0].replace('：','').strip()
        return res
    else:
        return '没有找到相关的邮政编码信息'

def baidu_location(location):

    cookies = {
    # 'PHPSESSID': 'm9uvdap9nqnohfndoir1p8nj85',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }

    params = (
        ('m', 'postsearch'),
        ('c', 'index'),
        ('a', 'ajax_addr'),
        ('searchkey', location),
    )

    response = requests.get('http://cpdc.chinapost.com.cn/web/index.php', headers=headers, params=params, cookies=cookies)
    res = response.json()
    result = {}
    for item in res['rs']:
        result[item['ADDR']] = item['POSTCODE']
    return result

def avatardata_code(code):
    params = (
        ('postnumber', code),
        ('key','ed634fcfee5c407d8f73f329bbd4a116')
    )
    response = requests.get('http://api.avatardata.cn/PostNumber/QueryPostnumber', params=params)
    res = response.json()
    if not res['result']:
        return '没有找到相关的邮政编码信息'
    return res['result'][0]['jd']

def avatardata_location(locition):
    params = (
        ('address', locition),
        ('key','ed634fcfee5c407d8f73f329bbd4a116')
    )
    response = requests.get('http://api.avatardata.cn/PostNumber/QueryAddress', params=params)
    res = response.json()
    if not res['result']:
        return '没有找到相关的邮政编码信息'

    result = {}
    for item in res['result']:
        result[item['jd']+item['address']] = item['postnumber']
    return result


# codes = ['102200','463800','243800']
# for code in codes:
#     print(avatardata_locition(code))
#     print('******************************')

adress = '江苏省南京市玄武区'
print(baidu_location(adress))