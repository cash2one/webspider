import requests
from lxml import etree
import sys
sys.path.append("/ROOT/www/spider/settings")
from langconv import *
from mysql import MySQLWrapper
import logging
import time


logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/ROOT/logs/stock.log',
                )
mysql = MySQLWrapper()




cookies = {
    '_ga': 'GA1.2.829106724.1523845461',
    '_gid': 'GA1.2.661814915.1523845464',
    '__utma': '131925965.829106724.1523845461.1523845497.1523845497.1',
    '__utmc': '131925965',
    '__utmz': '131925965.1523845497.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmt': '1',
    '__utmb': '131925965.7.10.1523845497',
}

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://stockq.org/market/asia.php',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

def stock_Asian():

    response = requests.get('http://stockq.org/market/asia.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr/td/font/b/text()')[0]
    print('title : %s,  %s'%(title,Converter('zh-hans').convert(title)))

    sub_title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr[2]/td')
    a = []
    for item in sub_title:
        a.append(item.xpath('font/text()')[0])

    print(' '.join(a))

    content = selector.xpath('/html/body/table/tr/td[2]/center/table//tr[position()>2]')
    for item in content:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        result.append(item.xpath('td[5]/text()')[0])
        result.append(item.xpath('td[6]/text()')[0])
        result.append(item.xpath('td[7]/text()')[0])
        result.append(item.xpath('td[8]/text()')[0])
        if item.xpath('td[9]/text()'):
            result.append(item.xpath('td[9]/text()')[0])
        else:
            result.insert(6,'NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_global():

    response = requests.get('http://stockq.org/market/return.php', headers=headers, cookies=cookies)
    selector = etree.HTML(response.content.decode('utf-8'))
    title = selector.xpath('/html/body/table/tr/td[2]/table[2]/tr[1]/td/h3/text()')[0]
    print(title)
    content = selector.xpath('//table[@class="returntable"]')
    for item in content[:12]:
        print(item.xpath('tr[1]/td/font/b/text()')[0]+' '+item.xpath('tr[1]/td/text()')[1].strip())
        res = item.xpath('tr[position()>2]')
        for ele in res:
            print(ele.xpath('td[1]/a/font/text()')[0]+' '+''.join(ele.xpath('td[2]//text()')))
    title = selector.xpath('/html/body/table/tr/td[2]/table[2]/tr[5]/td/h3/text()')[0]
    print(title)
    for item in content[12:]:
        print(item.xpath('tr[1]/td/font/b/text()')[0]+' '+item.xpath('tr[1]/td/text()')[1].strip())
        res = item.xpath('tr[position()>2]')
        for ele in res:
            print(ele.xpath('td[1]/a/font/text()')[0]+' '+''.join(ele.xpath('td[2]//text()')))

def stock_lowmarket():

    response = requests.get('http://stockq.org/market/lowmarket.php', headers=headers, cookies=cookies)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')[0]
    print(content.xpath('tr[1]/td/font/b/text()')[0])
    title = content.xpath('tr[2]/td')
    res = []
    for item in title:
        res.append(item.xpath('font/text()')[0])

    print('  '.join(res))
    res = content.xpath('tr[position()>2]')
    for item in res:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        if item.xpath('td[5]/text()'):
            result.append(item.xpath('td[5]/text()')[0])
        else:
            result.append('NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_highmarket():

    response = requests.get('http://stockq.org/market/highmarket.php', headers=headers, cookies=cookies)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')[0]
    print(content.xpath('tr[1]/td/font/b/text()')[0])
    title = content.xpath('tr[2]/td')
    res = []
    for item in title:
        res.append(item.xpath('font/text()')[0])

    print('  '.join(res))
    res = content.xpath('tr[position()>2]')
    for item in res:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        if item.xpath('td[5]/text()'):
            result.append(item.xpath('td[5]/text()')[0])
        else:
            result.append('NULL')

        print(Converter('zh-hans').convert(' '.join(result)))   

def stock_europe():

    response = requests.get('http://stockq.org/market/europe.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr/td/font/b/text()')[0]
    print('title : %s,  %s'%(title,Converter('zh-hans').convert(title)))

    sub_title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr[2]/td')
    a = []
    for item in sub_title:
        a.append(item.xpath('font/text()')[0])

    print(' '.join(a))

    content = selector.xpath('/html/body/table/tr/td[2]/center/table//tr[position()>2]')
    for item in content:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        result.append(item.xpath('td[5]/text()')[0])
        result.append(item.xpath('td[6]/text()')[0])
        result.append(item.xpath('td[7]/text()')[0])
        result.append(item.xpath('td[8]/text()')[0])
        if item.xpath('td[9]/text()'):
            result.append(item.xpath('td[9]/text()')[0])
        else:
            result.insert(6,'NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_america():

    response = requests.get('http://stockq.org/market/america.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr/td/font/b/text()')[0]
    print('title : %s,  %s'%(title,Converter('zh-hans').convert(title)))

    sub_title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr[2]/td')
    a = []
    for item in sub_title:
        a.append(item.xpath('font/text()')[0])

    print(' '.join(a))

    content = selector.xpath('/html/body/table/tr/td[2]/center/table//tr[position()>2]')
    for item in content:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        result.append(item.xpath('td[5]/text()')[0])
        result.append(item.xpath('td[6]/text()')[0])
        result.append(item.xpath('td[7]/text()')[0])
        result.append(item.xpath('td[8]/text()')[0])
        if item.xpath('td[9]/text()'):
            result.append(item.xpath('td[9]/text()')[0])
        else:
            result.insert(6,'NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_global_all():

    response = requests.get('http://stockq.org/market/global.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr/td/font/b/text()')[0]
    print('title : %s,  %s'%(title,Converter('zh-hans').convert(title)))

    sub_title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr[2]/td')
    a = []
    for item in sub_title:
        a.append(item.xpath('font/text()')[0])

    print(' '.join(a))

    content = selector.xpath('/html/body/table/tr/td[2]/center/table//tr[position()>2]')
    for item in content:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        result.append(item.xpath('td[5]/text()')[0])
        result.append(item.xpath('td[6]/text()')[0])
        result.append(item.xpath('td[7]/text()')[0])
        result.append(item.xpath('td[8]/text()')[0])
        if item.xpath('td[9]/text()'):
            result.append(item.xpath('td[9]/text()')[0])
        else:
            result.insert(6,'NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_commodity():

    response = requests.get('http://stockq.org/market/commodity.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')[0]
    print(content.xpath('tr[1]/td/a/b/text()')[0])
    title = content.xpath('tr[2]/td')
    res = []
    for item in title:
        res.append(item.xpath('font/text()')[0])

    print('  '.join(res))
    res = content.xpath('tr[position()>2]')
    for item in res:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        if item.xpath('td[5]/text()'):
            result.append(item.xpath('td[5]/text()')[0])
        else:
            result.append('NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_currency():
    response = requests.get('http://stockq.org/market/currency.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')[0]
    print(content.xpath('tr[1]/td/a/b/text()')[0])
    title = content.xpath('tr[2]/td')
    res = []
    for item in title:
        res.append(item.xpath('font/text()')[0])

    print('  '.join(res))
    res = content.xpath('tr[position()>2]')
    for item in res:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/span/text()')[0])
        result.append(item.xpath('td[4]/span/text()')[0])
        if item.xpath('td[5]/text()'):
            result.append(item.xpath('td[5]/text()')[0])
        else:
            result.append('NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_sector():
    response = requests.get('http://stockq.org/market/sector.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')[0]
    print(content.xpath('tr[1]/td/font/b/text()')[0])
    title = content.xpath('tr[2]/td')
    res = []
    for item in title:
        res.append(item.xpath('font/text()')[0])

    print('  '.join(res))
    res = content.xpath('tr[position()>2]')
    for item in res:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        if item.xpath('td[5]/text()'):
            result.append(item.xpath('td[5]/text()')[0])
        else:
            result.append('NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_msci():

    response = requests.get('http://stockq.org/market/msci.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr/td/font/b/text()')[0]
    print('title : %s,  %s'%(title,Converter('zh-hans').convert(title)))

    sub_title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr[2]/td')
    a = []
    for item in sub_title:
        a.append(item.xpath('font/text()')[0])

    print('      '.join(a))

    content = selector.xpath('//table[@class="marketdatatable"]')
    for ele in content:
        ele = ele.xpath('tr[position()>2]')
        for item in ele:
            result = []
            result.append(item.xpath('td[1]/a/text()')[0])
            result.append(item.xpath('td[2]/text()')[0])
            result.append(''.join(item.xpath('td[3]//text()')))
            result.append(''.join(item.xpath('td[4]//text()')))
            result.append(''.join(item.xpath('td[5]//text()')))
            result.append(''.join(item.xpath('td[6]//text()')))
            result.append(''.join(item.xpath('td[7]//text()')))
            result.append(''.join(item.xpath('td[8]//text()')))
            result.append(''.join(item.xpath('td[9]//text()')))
            if item.xpath('td[10]//text()'):
                result.append(''.join(item.xpath('td[10]//text()')))
            else:
                result.insert(6,'NULL')

            print(Converter('zh-hans').convert('   '.join(result)))

def stock_msci_gross():

    response = requests.get('http://stockq.org/market/msci_gross.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr/td/font/b/text()')[0]
    print('title : %s,  %s'%(title,Converter('zh-hans').convert(title)))

    sub_title = selector.xpath('/html/body/table/tr/td[2]/center/table/tr[2]/td')
    a = []
    for item in sub_title:
        a.append(item.xpath('font/text()')[0])

    print('      '.join(a))

    content = selector.xpath('//table[@class="marketdatatable"]')
    for ele in content:
        ele = ele.xpath('tr[position()>2]')
        for item in ele:
            result = []
            result.append(item.xpath('td[1]/a/text()')[0])
            result.append(item.xpath('td[2]/text()')[0])
            result.append(''.join(item.xpath('td[3]//text()')))
            result.append(''.join(item.xpath('td[4]//text()')))
            result.append(''.join(item.xpath('td[5]//text()')))
            result.append(''.join(item.xpath('td[6]//text()')))
            result.append(''.join(item.xpath('td[7]//text()')))
            result.append(''.join(item.xpath('td[8]//text()')))
            result.append(''.join(item.xpath('td[9]//text()')))
            if item.xpath('td[10]//text()'):
                result.append(''.join(item.xpath('td[10]//text()')))
            else:
                result.insert(6,'NULL')

            print(Converter('zh-hans').convert('   '.join(result)))

def stock_mscisector():
    response = requests.get('http://stockq.org/market/mscisector.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')[0]
    print(content.xpath('tr[1]/td/font/b/text()')[0])
    title = content.xpath('tr[2]/td')
    res = []
    for item in title:
        res.append(item.xpath('font/text()')[0])

    print('  '.join(res))
    res = content.xpath('tr[position()>2]')
    for item in res:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        result.append(item.xpath('td[5]/text()')[0])
        if item.xpath('td[6]/text()'):
            result.append(item.xpath('td[6]/text()')[0])
        else:
            result.append('NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_mscisector_gross():
    response = requests.get('http://stockq.org/market/mscisector_gross.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')[0]
    print(content.xpath('tr[1]/td/font/b/text()')[0])
    title = content.xpath('tr[2]/td')
    res = []
    for item in title:
        res.append(item.xpath('font/text()')[0])

    print('  '.join(res))
    res = content.xpath('tr[position()>2]')
    for item in res:
        result = []
        result.append(item.xpath('td[1]/a/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/text()')[0])
        result.append(item.xpath('td[4]/text()')[0])
        result.append(item.xpath('td[5]/text()')[0])
        if item.xpath('td[6]/text()'):
            result.append(item.xpath('td[6]/text()')[0])
        else:
            result.append('NULL')

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_indexfuture():
    response = requests.get('http://stockq.org/market/indexfuture.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')[0]
    print(content.xpath('tr[1]/td/font/b/text()')[0])
    title = content.xpath('tr[2]/td')
    res = []
    for item in title:
        res.append(item.xpath('font/text()')[0])

    print('  '.join(res))
    res = content.xpath('tr[position()>2]')
    for item in res:
        result = []
        result.append(item.xpath('td[1]/text()')[0])
        result.append(item.xpath('td[2]/text()')[0])
        result.append(item.xpath('td[3]/span/text()')[0])
        result.append(''.join(item.xpath('td[4]//text()')))
        if item.xpath('td[5]/text()'):
            result.append(item.xpath('td[5]/text()')[0])
        else:
            result.append('NULL')
        result.append(item.xpath('td[6]/text()')[0])
        result.append(item.xpath('td[7]/text()')[0])
        result.append(item.xpath('td[8]/text()')[0])

        print(Converter('zh-hans').convert(' '.join(result)))

def stock_bondindex():
    response = requests.get('http://stockq.org/bond/bondindex.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="bondindextable"]')
    for ele in content:
        res = ele.xpath('tr[position()>1]')
        for item in res:
            result = []
            result.append(item.xpath('td[1]/a/text()')[0])
            result.append(item.xpath('td[2]/text()')[0])
            result.append(item.xpath('td[3]/text()')[0])
            result.append(item.xpath('td[4]/text()')[0])
            result.append(item.xpath('td[5]/text()')[0])
            result.append(item.xpath('td[6]/text()')[0])
            result.append(item.xpath('td[7]/text()')[0])
            result.append(item.xpath('td[8]/text()')[0])
            print(Converter('zh-hans').convert(' '.join(result)))

def stock_bondindex2():
    response = requests.get('http://stockq.org/bond/bondindex2.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="bondindextable"]')
    for ele in content:
        res = ele.xpath('tr[position()>1]')
        for item in res:
            result = []
            result.append(item.xpath('td[1]/a/text()')[0])
            result.append(item.xpath('td[2]/text()')[0])
            result.append(item.xpath('td[3]/text()')[0])
            result.append(item.xpath('td[4]/text()')[0])
            result.append(item.xpath('td[5]/text()')[0])
            result.append(item.xpath('td[6]/text()')[0])
            result.append(item.xpath('td[7]/text()')[0])
            result.append(item.xpath('td[8]/text()')[0])
            result.append(item.xpath('td[9]/text()')[0])
            result.append(item.xpath('td[10]/text()')[0])
            print(Converter('zh-hans').convert(' '.join(result)))

def stock_treasury():
    response = requests.get('http://stockq.org/bond/treasury.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="economytable"]')
    for ele in content:
        res = ele.xpath('tr[position()>2]')
        for item in res:
            result = []
            result.append(item.xpath('td[1]/font/text()')[0])
            result.append(item.xpath('td[2]/font/text()')[0])
            result.append(item.xpath('td[3]/font/text()')[0])
            result.append(item.xpath('td[4]/font/text()')[0])
            result.append(item.xpath('td[5]/font/text()')[0])
            result.append(item.xpath('td[6]/font/text()')[0])
            result.append(item.xpath('td[7]/font/text()')[0])
            result.append(item.xpath('td[8]/font/text()')[0])
            result.append(item.xpath('td[9]/font/text()')[0])
            result.append(item.xpath('td[10]/font/text()')[0])
            result.append(item.xpath('td[11]/font/text()')[0])
            result.append(item.xpath('td[12]/font/text()')[0])
            print(Converter('zh-hans').convert(' '.join(result)))

def stock_bondrate():
    response = requests.get('http://stockq.org/bond/bondrate.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="bondratetable"]')
    for ele in content:
        res = ele.xpath('tr[position()>2]')
        for item in res:
            result = []
            result.append(item.xpath('td[1]/text()')[0])
            result.append(item.xpath('td[2]/text()')[0])
            result.append(item.xpath('td[3]/text()')[0])
            result.append(item.xpath('td[4]/text()')[0])
            result.append(item.xpath('td[5]/text()')[0])
            print(Converter('zh-hans').convert(' '.join(result)))

def stock_cds():
    response = requests.get('http://stockq.org/bond/cds.php', cookies=cookies, headers=headers)
    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')
    for ele in content:
        res = ele.xpath('tr[position()>2]')
        for item in res:
            result = []
            result.append(item.xpath('td[1]/a/text()')[0])
            result.append(item.xpath('td[2]/text()')[0])
            result.append(item.xpath('td[3]/text()')[0])
            result.append(item.xpath('td[4]/text()')[0])
            result.append(item.xpath('td[5]/text()')[0])
            print(Converter('zh-hans').convert(' '.join(result)))

def stock_all():
    f_Year = time.strftime("%Y", time.localtime(time.time()))
    f_Month = time.strftime("%m", time.localtime(time.time()))
    f_Day = time.strftime("%d", time.localtime(time.time()))
    f_CreateTime = time.strftime("%H:%M", time.localtime(time.time()))
    try:
        response = requests.get('http://stockq.org/', headers=headers, cookies=cookies)
    except Exception as e:
        logging.error(e)
        logging.error('requests stockq error')

    selector = etree.HTML(response.content.decode('utf-8'))
    content = selector.xpath('//table[@class="marketdatatable"]')

    # 亞洲股市指數行情
    res = content[0].xpath('tr[position()>2]')
    for item in res:
        f_Region = u'亚洲'
        f_Stock = Converter('zh-hans').convert(item.xpath('td[1]/a/text()')[0]).encode('utf-8')
        f_Index = item.xpath('td[2]/text()')[0]
        f_Fluctuation = item.xpath('td[3]/text()')[0]
        f_Rate = item.xpath('td[4]/text()')[0]
        f_CurrentTime = item.xpath('td[5]/text()')[0]
        
        update_t_global_index(f_Region,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime)

        try:
            insert_sql = 'INSERT INTO t_asia_index_all(f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
        except Exception as e:
            logging.error(e)
            logging.error('insert error,stock:%s',f_Stock)

    # 歐洲股市指數、非洲股市指數
    res = content[1].xpath('tr[position()>2]')
    for item in res:
        f_Region = u'欧非'
        f_Stock = Converter('zh-hans').convert(item.xpath('td[1]/a/text()')[0]).encode('utf-8')
        f_Index = item.xpath('td[2]/text()')[0]
        f_Fluctuation = item.xpath('td[3]/text()')[0]
        f_Rate = item.xpath('td[4]/text()')[0]
        f_CurrentTime = item.xpath('td[5]/text()')[0]
        
        update_t_global_index(f_Region,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime)

        try:
            insert_sql = 'INSERT INTO t_europe_africa_index_all(f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
        except Exception as e:
            logging.error(e)
            logging.error('insert error,stock:%s',f_Stock)
    
    # 美洲股市指數行情
    res = content[2].xpath('tr[position()>2]')
    for item in res:
        f_Region = u'美洲'
        f_Stock = Converter('zh-hans').convert(item.xpath('td[1]/a/text()')[0]).encode('utf-8')
        f_Index = item.xpath('td[2]/text()')[0]
        f_Fluctuation = item.xpath('td[3]/text()')[0]
        f_Rate = item.xpath('td[4]/text()')[0]
        f_CurrentTime = item.xpath('td[5]/text()')[0]
        
        update_t_global_index(f_Region,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime)

        try:
            insert_sql = 'INSERT INTO  t_america_index_all(f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
        except Exception as e:
            logging.error(e)
            logging.error('insert error,stock:%s',f_Stock)


    # 分類指數行情
    for table in content[3:6]:
        res = table.xpath('tr[position()>2]')
        for item in res:
            f_Region = u'分类指数'
            f_Stock = Converter('zh-hans').convert(item.xpath('td[1]/a/text()')[0]).encode('utf-8')
            f_Index = item.xpath('td[2]/text()')[0]
            f_Fluctuation = item.xpath('td[3]/text()')[0]
            f_Rate = item.xpath('td[4]/text()')[0]
            f_CurrentTime = item.xpath('td[5]/text()')[0]
            
            update_t_global_index(f_Region,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime)

            try:
                insert_sql = 'INSERT INTO  t_sub_index_all(f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mysql.execute(insert_sql,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
            except Exception as e:
                logging.error(e)
                logging.error('insert error,stock:%s',f_Stock)

    # 全球期貨指數
    res = content[9].xpath('tr[position()>2]')
    for item in res:
        f_Region = u'全球期货指数'
        f_Stock = Converter('zh-hans').convert(item.xpath('td[1]/text()')[0]).encode('utf-8')
        f_Index = item.xpath('td[2]/text()')[0]
        f_Fluctuation = item.xpath('td[3]/span/text()')[0]
        f_Rate = ''.join(item.xpath('td[4]//text()'))
        if item.xpath('td[5]/text()'):
            f_CurrentTime = item.xpath('td[5]/text()')[0]
        else:
            f_CurrentTime = ''
        
        update_t_global_index(f_Region,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime)

        try:
            insert_sql = 'INSERT INTO  t_futures_index_all(f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
        except Exception as e:
            logging.error(e)
            logging.error('insert error,stock:%s',f_Stock)

    # 商品价格
    res = content[6].xpath('tr[position()>2]')
    for item in res:
        f_Commodity = Converter('zh-hans').convert(item.xpath('td[1]/a/text()')[0]).encode('utf-8')
        f_BuyPrice = item.xpath('td[2]/text()')[0]
        f_Fluctuation = item.xpath('td[3]/text()')[0]
        f_Rate = item.xpath('td[4]/text()')
        if item.xpath('td[5]/text()'):
            f_CurrentTime = item.xpath('td[5]/text()')[0]
        else:
            f_CurrentTime = None

        if len(f_Commodity) >=9:
            f_Region = u'商品期货'
            try:
                insert_sql = 'INSERT INTO  t_commodity_futures_all(f_Commodity,f_BuyPrice,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mysql.execute(insert_sql,f_Commodity,f_BuyPrice,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
            except Exception as e:
                logging.error(e)
                logging.error('insert error,Commodity:%s',f_Commodity)
        else:
            f_Region = u'大宗商品'
            try:
                insert_sql = 'INSERT INTO  t_commodity_goods_all(f_Commodity,f_BuyPrice,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mysql.execute(insert_sql,f_Commodity,f_BuyPrice,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
            except Exception as e:
                logging.error(e)
                logging.error('insert error,Commodity:%s',f_Commodity)


        select_sql = 'SELECT * FROM t_commodity where f_Commodity=%s and f_Region=%s'
        result = mysql.fetchOne(select_sql,f_Commodity,f_Region)
        
        if not result:
            try:
                insert_sql = 'INSERT INTO t_commodity(f_Commodity,f_Region,f_BuyPrice,f_Fluctuation,f_Rate,f_CurrentTime) VALUES(%s,%s,%s,%s,%s,%s)'
                mysql.execute(insert_sql,f_Commodity,f_Region,f_BuyPrice,f_Fluctuation,f_Rate,f_CurrentTime)
            except Exception as e:
                logging.error(e)
                logging.error('insert error,Commodity:%s',f_Commodity)
        else:
            try:
                update_sql = 'UPDATE t_commodity SET f_Commodity=%s,f_BuyPrice=%s,f_Region=%s,f_Fluctuation=%s,f_Rate=%s,f_CurrentTime=%s where f_UID=%s'
                mysql.execute(insert_sql,f_Commodity,f_BuyPrice,f_Region,f_Fluctuation,f_Rate,f_CurrentTime,result['f_UID'])
            except Exception as e:
                logging.error(e)
                logging.error('update error,Commodity:%s',f_Commodity)
        
        try:
            insert_sql = 'INSERT INTO  t_commodity_all(f_Commodity,f_BuyPrice,f_Fluctuation,f_Region,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,f_Commodity,f_BuyPrice,f_Fluctuation,f_Region,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
        except Exception as e:
            logging.error(e)
            logging.error('insert error,Commodity:%s',f_Commodity)

    # 全球汇率
    res = content[7].xpath('tr[position()>2]')
    for item in res:
        f_Currency = Converter('zh-hans').convert(item.xpath('td[1]/a/text()')[0]).encode('utf-8')
        f_Exchange = item.xpath('td[2]/text()')[0]
        f_Fluctuation = item.xpath('td[3]/span/text()')[0]
        f_Rate = ''.join(item.xpath('td[4]//text()'))
        if item.xpath('td[5]/text()'):
            f_CurrentTime = item.xpath('td[5]/text()')[0]
        else:
            f_CurrentTime = ''
        
        select_sql = 'SELECT * FROM t_global_exchange where f_Currency=%s'
        result = mysql.fetchOne(select_sql,f_Currency)
        if not result:
            try:
                insert_sql = 'INSERT INTO t_global_exchange(f_Currency,f_Exchange,f_Fluctuation,f_Rate,f_CurrentTime) VALUES(%s,%s,%s,%s,%s)'
                mysql.execute(insert_sql,f_Currency,f_Exchange,f_Fluctuation,f_Rate,f_CurrentTime)
            except Exception as e:
                logging.error(e)
                logging.error('insert error,Currency:%s',f_Currency)
        else:
            try:
                update_sql = 'UPDATE t_global_exchange SET f_Currency=%s,f_Exchange=%s,f_Fluctuation=%s,f_Rate=%s,f_CurrentTime=%s where f_UID=%s'
                mysql.execute(insert_sql,f_Currency,f_Exchange,f_Fluctuation,f_Rate,f_CurrentTime,result['f_UID'])
            except Exception as e:
                logging.error(e)
                logging.error('update error,Currency:%s',f_Currency)
        try:
            insert_sql = 'INSERT INTO  t_global_exchange_all(f_Currency,f_Exchange,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,f_Currency,f_Exchange,f_Fluctuation,f_Rate,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
        except Exception as e:
            logging.error(e)
            logging.error('insert error,Currency:%s',f_Currency) 

    # MSCI指數
    res = content[8].xpath('tr[position()>2]')
    for item in res:
        f_Msci = Converter('zh-hans').convert(item.xpath('td[1]/a/text()')[0]).encode('utf-8')
        f_Index = item.xpath('td[2]/text()')[0]
        f_OneDay = ''.join(item.xpath('td[3]//text()'))
        f_OneMonth = ''.join(item.xpath('td[4]//text()'))
        f_OneYear = ''.join(item.xpath('td[5]//text()'))
        
        select_sql = 'SELECT * FROM t_msci_index where f_Msci=%s'
        result = mysql.fetchOne(select_sql,f_Msci)
        if not result:
            try:
                insert_sql = 'INSERT INTO t_msci_index(f_Msci,f_Index,f_OneDay,f_OneMonth,f_OneYear) VALUES(%s,%s,%s,%s,%s)'
                mysql.execute(insert_sql,f_Msci,f_Index,f_OneDay,f_OneMonth,f_OneYear)
            except Exception as e:
                logging.error(e)
                logging.error('insert error,Msci:%s',f_Msci)
        else:
            try:
                update_sql = 'UPDATE t_msci_index SET f_Msci=%s,f_Index=%s,f_OneDay=%s,f_OneMonth=%s,f_OneYear=%s where f_UID=%s'
                mysql.execute(insert_sql,f_Msci,f_Index,f_OneDay,f_OneMonth,f_OneYear,result['f_UID'])
            except Exception as e:
                logging.error(e)
                logging.error('update error,Msci:%s',f_Msci)
        try:
            insert_sql = 'INSERT INTO  t_msci_index_all(f_Msci,f_Index,f_OneDay,f_OneMonth,f_OneYear,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,f_Msci,f_Index,f_OneDay,f_OneMonth,f_OneYear,f_Year,f_Month,f_Day,f_CreateTime)
        except Exception as e:
            logging.error(e)
            logging.error('insert error,Msci:%s',f_Msci)    
    
    # 债券指数
    content = selector.xpath('//table[@class="bonddatatable"]')[0]
    res = content.xpath('tr[position()>2]')
    for item in res:
        f_IndexName = Converter('zh-hans').convert(item.xpath('td[1]/a/text()')[0]).encode('utf-8')
        f_ClosePrice = item.xpath('td[2]/text()')[0]
        f_Rate = item.xpath('td[3]/text()')[0]
        f_YieldRate = item.xpath('td[4]/text()')[0]
        f_Spreads = item.xpath('td[5]/text()')[0]
        f_CurrentTime = item.xpath('td[6]/text()')[0]
        
        select_sql = 'SELECT * FROM t_bond_index where f_IndexName=%s'
        result = mysql.fetchOne(select_sql,f_IndexName)
        if not result:
            try:
                insert_sql = 'INSERT INTO t_bond_index(f_IndexName,f_ClosePrice,f_Rate,f_YieldRate,f_Spreads,f_CurrentTime) VALUES(%s,%s,%s,%s,%s,%s)'
                mysql.execute(insert_sql,f_IndexName,f_ClosePrice,f_Rate,f_YieldRate,f_Spreads,f_CurrentTime)
            except Exception as e:
                logging.error(e)
                logging.error('insert error,IndexName:%s',f_IndexName)
        else:
            try:
                update_sql = 'UPDATE t_bond_index SET f_IndexName=%s,f_ClosePrice=%s,f_Rate=%s,f_YieldRate=%s,f_Spreads=%s,f_CurrentTime=%s where f_UID=%s'
                mysql.execute(insert_sql,f_IndexName,f_ClosePrice,f_Rate,f_YieldRate,f_Spreads,f_CurrentTime,result['f_UID'])
            except Exception as e:
                logging.error(e)
                logging.error('update error,IndexName:%s',f_IndexName)
        try:
            insert_sql = 'INSERT INTO  t_bond_index_all(f_IndexName,f_ClosePrice,f_Rate,f_YieldRate,f_Spreads,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,f_IndexName,f_ClosePrice,f_Rate,f_YieldRate,f_Spreads,f_CurrentTime,f_Year,f_Month,f_Day,f_CreateTime)
        except Exception as e:
            logging.error(e)
            logging.error('insert error,IndexName:%s',f_IndexName)    

def update_t_global_index(f_Region,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime):
    select_sql = 'SELECT * FROM t_global_index where f_Stock=%s and f_Region=%s'
    result = mysql.fetchOne(select_sql,f_Stock,f_Region)
    if not result:
        try:
            insert_sql = 'INSERT INTO t_global_index(f_Region,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime) VALUES(%s,%s,%s,%s,%s,%s)'
            mysql.execute(insert_sql,f_Region,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime)
        except Exception as e:
            logging.error(e)
            logging.error('insert error,stock:%s',f_Stock)
    else:
        try:
            update_sql = 'UPDATE t_global_index SET f_Region=%s,f_Stock=%s,f_Index=%s,f_Fluctuation=%s,f_Rate=%s,f_CurrentTime=%s where f_UID=%s'
            mysql.execute(update_sql,f_Region,f_Stock,f_Index,f_Fluctuation,f_Rate,f_CurrentTime,result['f_UID'])
        except Exception as e:
            logging.error(e)
            logging.error('update error,stock:%s',f_Stock)

        


stock_all()
