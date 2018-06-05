import time
import json
import requests


def baidu_IP(ip_address):
    data = {}
    data['IP'] = ip_address
    data['address'] = ''
    data['operator'] = ''
    temp = ip_address.split('.')
    for item in temp:
        if len(item)>3:
            data['info'] = u'ip地址输入有误'
            return data
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=ip&oq=%25E5%25AE%259C%25E6%2590%259C&rsv_pq=e53a474f00063077&rsv_t=9455WdTipRfqkrxglQ%2F4ResNP%2BAQDjQueJ90gBQa%2FZ9U3swXOA6s0i9%2FZsQ&rqlang=cn&rsv_enter=0&inputT=1511&rsv_sug3=57&rsv_sug1=58&rsv_sug7=100&rsv_sug2=0&rsv_sug4=1511',
        'Connection': 'keep-alive',
    }
    params = (
        ('query', ip_address),
        ('co', ''),
        ('resource_id', '6006'),
        ('t', str(int(time.time())*1000)),
        ('ie', 'utf8'),
        ('oe', 'gbk'),
        ('format', 'json'),
        ('tn', 'baidu'),
    )

    response = requests.get('https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php', headers=headers, params=params)
    res = response.json()
    
    if res['data']:
        temp = res['data'][0]['location'].split(' ')
        data['address'] = temp[0]
        if len(temp)==2:
            data['operator'] = temp[1]
        data['info'] = 'ok'        
    else:
        data['info'] = u'ip地址输入有误'
    return data

def sina_api(ip_address):
    temp = ip_address.split('.')
    data = {}
    data['IP'] = ip_address
    data['operator'] = ''
    data['address'] = ''
    data['info'] = 'ok'
    for item in temp:
        if len(item)>3:
            data['info'] = u'ip地址输入有误'
            return data
    params = (
        ('ip', ip_address),
        ('format', 'json'),
    )
    response = requests.get('http://int.dpool.sina.com.cn/iplookup/iplookup.php', params=params)
    res = response.json()

    if type(res) is int:
        data['info'] = u'ip地址输入有误'
        return data
    
    if res['ret'] == 1:
        data['address'] = res['country']+' '+res['province']+' '+res['city']
    elif res['ret'] == -1:
        data['operator'] = '内网'
    return data

def taobao_API_IP(ip_address):
    temp = ip_address.split('.')
    data = {}
    data['IP'] = ip_address
    data['info'] = 'ok'
    for item in temp:
        if len(item)>3:
            data['info'] = u'ip地址输入有误'
            data['operator'] = ''
            data['address'] = ''
            return data
    params = (
        ('ip', ip_address),
    )
    response = requests.get('http://ip.taobao.com/service/getIpInfo.php', params=params)
    res = response.json()
    if res['code'] != 0:
        data['info'] = u'ip地址输入有误'
        data['operator'] = ''
        data['address'] = ''
    else:
        data['operator'] = res['data']['isp']
        data['address'] = res['data']['country']+' '+res['data']['region']+' '+res['data']['city']
    return data

def tool_lu(ip_address):
    temp = ip_address.split('.')
    result = {}
    result['IP'] = ip_address
    result['info'] = 'ok'
    result['operator'] = ''
    for item in temp:
        if len(item)>3:
            result['info'] = u'ip地址输入有误'            
            result['address'] = ''
            return result
    headers = {
        'cookie': 'slim_session=^%^7B^%^22slim.flash^%^22^%^3A^%^5B^%^5D^%^7D; uuid=0a1998fe-0f00-4996-c987-c179c7607691; Hm_lvt_0fba23df1ee7ec49af558fb29456f532=1524022874,1524022939,1524022994; Hm_lpvt_0fba23df1ee7ec49af558fb29456f532=1524022994',
        'origin': 'https://tool.lu',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://tool.lu/ip',
        'authority': 'tool.lu',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = [
      ('ip', ip_address),
    ]

    response = requests.post('https://tool.lu/ip/ajax.html', headers=headers, data=data)
    res = json.loads(response.text)
    if res['status']:
        result['info'] = 'ok'            
        result['address'] = res['text']['ipip_location']
    else:
        result['info'] = u'ip地址输入有误'            
        result['address'] = ''
    return result

def afanda_API_IP(ip_address):
    temp = ip_address.split('.')
    result = {}
    result['IP'] = ip_address
    result['info'] = 'ok'
    result['operator'] = ''
    for item in temp:
        if len(item)>3:
            result['info'] = u'ip地址输入有误'            
            result['address'] = ''
            return result
    params = (
        ('ip', ip_address),
        ('key','c99f54521c3b4142b89de3c1c688ba49')
    )
    response = requests.get('http://api.avatardata.cn/IpLookUp/LookUp', params=params)
    res = response.json()
    if res['error_code'] != 0:
        result['info'] = res['reason']
        result['address'] = ''
    else:
        result['address'] = res['result']['area']
        result['operator'] = res['result']['location']
    return result


if __name__ == '__main__':
    print(afanda_API('192.168.1.93'))