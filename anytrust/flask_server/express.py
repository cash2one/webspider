import requests
import time


WEEK_MAP={
    'Mon':'星期一',
    'Tue':'星期二',
    'Wed':'星期三',
    'Thu':'星期四',
    'Fri':'星期五',
    'Sat':'星期六',
    'Sun':'星期日',
}
TYPE_MAP ={
    'yunda':'韵达快递',
    'shentong':'申通快递',
    'EMS':'EMS',
    'shunfeng':'顺丰快递',
    'yuantong':'圆通快递',
    'tiantian':'天天快递',
    'huitongkuaidi':'百世快递',
    'debangwuliu':'德邦'
}
# 快递100
def get_type(text):
    cookies = {
        'WWWID': 'WWW742078F1537945B172A36DDC192E80EA',
        'Hm_lvt_22ea01af58ba2be0fec7c11b25e88e6c': '1527484152',
        'Hm_lpvt_22ea01af58ba2be0fec7c11b25e88e6c': '1527484152',
    }

    headers = {
        'Origin': 'http://www.kuaidi100.com',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://www.kuaidi100.com/?from=openv',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Content-Length': '0',
    }

    params = (
        ('text', text),
    )

    response = requests.post('http://www.kuaidi100.com/autonumber/autoComNum', headers=headers, params=params, cookies=cookies)
    return response.json()['auto'][0]['comCode']



def get_text(num):
    data = {}
    a = get_type(num)
    data['type'] = TYPE_MAP.get(a,a)
    data['num'] = num
    data['msg'] = ''
    data['code'] = 'success'
    data['data'] = ''
    data['source'] = u'快递100'
    cookies = {
        'WWWID': 'WWW742078F1537945B172A36DDC192E80EA',
        'Hm_lvt_22ea01af58ba2be0fec7c11b25e88e6c': '1527484152',
        'Hm_lpvt_22ea01af58ba2be0fec7c11b25e88e6c': '1527484152',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://www.kuaidi100.com/?from=openv',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('type', a),
        ('postid', num),
    )

    response = requests.get('http://www.kuaidi100.com/query', headers=headers, params=params, cookies=cookies)
    res = response.json()

    if res['message'] != 'ok':
        data['msg'] = res['message']
        data['code'] = 'error'
    else:
        result = []
        for item in res['data']:
            temp = {}
            temp['time'] = item['time']
            temp['weekday'] = time.strftime("%a",time.strptime(item['time'], "%Y-%m-%d %H:%M:%S"))
            temp['weekday'] = WEEK_MAP[temp['weekday']]
            temp['context'] = item['context']
            result.append(temp)
        data['data'] = result
    return data


#百度
def get_text_baidu(num):
    data = {}
    data['type'] = ''
    data['num'] = num
    data['msg'] = ''
    data['code'] = 'success'
    data['data'] = ''
    data['source'] = 'baidu'
    cookies = {
        'BAIDUID': '9FBB3DDF9C1043EC573390790B08EA9E:FG=1',
        'BIDUPSID': '9FBB3DDF9C1043EC573390790B08EA9E',
        'PSTM': '1523842582',
        '__cfduid': 'dc50a3536ae2dfa84617d62f0ed220c001523846572',
        'MCITY': '-131%3A',
        'BAEID': 'CA794D88A016592C28E8243FB2D24BD5',
        'H_PS_PSSID': '1435_26458_21123_20929',
        'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
        'PSINO': '2',
        'locale': 'zh',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=3924730222456&oq=%25E5%25BF%25AB%25E9%2580%2592%25E6%259F%25A5%25E8%25AF%25A2&rsv_pq=a86b4d6b00050d1b&rsv_t=2e243HD650Mi%2BzA1jwo1EMUzy3BGJ0uvGi0Hyr9wzzUsr987qehtD59NcbM&rqlang=cn&rsv_enter=1&inputT=2980&rsv_sug1=86&rsv_sug7=100&rsv_n=2&rsv_sug3=112&bs=%E5%BF%AB%E9%80%92%E6%9F%A5%E8%AF%A2',
        'Connection': 'keep-alive',
    }

    params = (
        ('appid', '4001'),
        ('nu',num),
    )

    response = requests.get('https://sp0.baidu.com/9_Q4sjW91Qh3otqbppnN2DJv/pae/channel/data/asyncqury', headers=headers, params=params, cookies=cookies)
    res = response.json()
    if res['msg'] != '':
        data['msg'] = res['msg']
        data['code'] = 'error'
    else:
        data['type'] = res['data']['com']
        data['type'] = TYPE_MAP.get(data['type'],data['type'])
        result = []
        for item in res['data']['info']['context']:
            temp = {}
            temp['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(item['time'])))
            temp['weekday'] = time.strftime("%a",time.localtime(int(item['time'])))
            temp['weekday'] = WEEK_MAP[temp['weekday']]
            temp['context'] = item['desc']
            result.append(temp)
        data['data'] = result
    return data

def get_type_sougou(num):

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Referer': 'https://www.sogou.com/web?query=3924730222456&_asf=www.sogou.com&_ast=1527489026&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index&sut=1008&sst0=1527489026584&lkt=0%2C0%2C0&sugsuv=00042B8A7C417F8E5AD56BEACA18A693&sugtime=1527489026584',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('objid', '90000000'),
        ('type', '2'),
        ('url', 'http://detail.i56.taobao.com/call/guess_cp.do'),
        ('p_mailNo', num),
    )

    response = requests.get('https://www.sogou.com/reventondc/external', headers=headers, params=params)
    return response.json()['result'][0]

#搜狗
def get_text_sougou(num):
    data = {}
    a = get_type_sougou(num)
    data['type'] = TYPE_MAP.get(a,a)
    data['num'] = num
    data['msg'] = ''
    data['code'] = 'success'
    data['data'] = ''
    data['source'] = 'sogou'

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Referer': 'https://www.sogou.com/web?query=3924730222456&_asf=www.sogou.com&_ast=1527489026&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index&sut=1008&sst0=1527489026584&lkt=0%2C0%2C0&sugsuv=00042B8A7C417F8E5AD56BEACA18A693&sugtime=1527489026584',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('objid', '90000000'),
        ('type', '2'),
        ('url', 'http://detail.i56.taobao.com/call/query_trace_un_login.do'),
        ('p_mailNo', data['num']),
        ('p_cpCode', a),
    )

    response = requests.get('https://www.sogou.com/reventondc/external', headers=headers, params=params)

    if response.text == ' ':
        data['msg'] = u'订单号错误'
        data['code'] = 'error'
        return data
    res = response.json()
    if not res['success']:
        data['msg'] = res['debugDesc']
        data['code'] = 'error'
    else:
        result = []
        for item in res['detailList'][0]['detail']:
            temp = {}
            temp['time'] = item['time']          
            temp['weekday'] = time.strftime("%a",time.strptime(item['time'], "%Y-%m-%d %H:%M:%S"))
            temp['weekday'] = WEEK_MAP[temp['weekday']]
            temp['context'] = item['desc']
            result.append(temp)
        data['data'] = result
    return data

def run(num):
    result = get_text(num)
    if result['code'] == 'error':
        result = get_text_baidu(num)
        if result['code'] == 'error':
            result = get_text_sougou(num)
    return result

if __name__ == '__main__':
    num = '3924730222456'
    run(num)