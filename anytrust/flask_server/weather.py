import requests
import re
import json
import time
import pickle

# format={"fa":图片1,"fb"：图片2,"fc":温度1,fd：温度2,fe:风向1,ff：风向2,fg:风力1,fh：风力2,fi:日出日落}; 
# 定义天气类型
weatherArr={
    "10": "暴雨", 
    "11": "大暴雨", 
    "12": "特大暴雨", 
    "13": "阵雪", 
    "14": "小雪", 
    "15": "中雪", 
    "16": "大雪", 
    "17": "暴雪", 
    "18": "雾", 
    "19": "冻雨", 
    "20": "沙尘暴", 
    "21": "小到中雨", 
    "22": "中到大雨", 
    "23": "大到暴雨", 
    "24": "暴雨到大暴雨", 
    "25": "大暴雨到特大暴雨", 
    "26": "小到中雪", 
    "27": "中到大雪", 
    "28": "大到暴雪", 
    "29": "浮尘", 
    "30": "扬沙", 
    "31": "强沙尘暴", 
    "53": "霾", 
    "99": "", 
    "00": "晴", 
    "01": "多云", 
    "02": "阴", 
    "03": "阵雨", 
    "04": "雷阵雨", 
    "05": "雷阵雨伴有冰雹", 
    "06": "雨夹雪", 
    "07": "小雨", 
    "08": "中雨", 
    "09": "大雨"
} 
# 定义风向数组 
fxArr={
    "0": "无持续风向", 
    "1": "东北风", 
    "2": "东风", 
    "3": "东南风", 
    "4": "南风", 
    "5": "西南风", 
    "6": "西风", 
    "7": "西北风", 
    "8": "北风", 
    "9": "旋转风"
}
# 定义风力数组 
flArr={
    "0": "微风", 
    "1": "3-4级", 
    "2": "4-5级", 
    "3": "5-6级", 
    "4": "6-7级", 
    "5": "7-8级", 
    "6": "8-9级", 
    "7": "9-10级", 
    "8": "10-11级", 
    "9": "11-12级"
}

WEEK_MAP={
    'Mon':'星期一',
    'Tue':'星期二',
    'Wed':'星期三',
    'Thu':'星期四',
    'Fri':'星期五',
    'Sat':'星期六',
    'Sun':'星期日',
}

def weather_search(city):
    f = open('city_id.pkl','rb')
    city_map = pickle.load(f)
    f.close()
    data = {}
    data['msg'] = ''
    data['code'] = 'success'
    data['data'] = {}

    cookies = {
        'vjuids': '32e204124.1630bb95d43.0.fa4551a590659',
        'UM_distinctid': '1630bb95d8151e-0582959a28b44b-3961430f-15f900-1630bb95d82c8e',
        'f_city': '%E5%8C%97%E4%BA%AC%7C101010100%7C',
        '__auc': '8c8a1da21630bbbab00e2cfe8e4',
        'Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b': '1524910962,1524911025,1524911355,1525239617',
        'vjlast': '1524910087.1525239617.13',
        'Wa_lvt_1': '1524910962,1524911025,1524911355,1525239617',
        'Wa_lpvt_1': '1525239764',
        'Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b': '1525239794',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://www.weather.com.cn/',
        'Connection': 'keep-alive',
    }

    params = (
        ('_', str(int(time.time()*1000))),
    )

    response = requests.get('http://d1.weather.com.cn/weather_index/'+city_map[city]+'.html', headers=headers, params=params, cookies=cookies)
    result = response.content.decode('utf-8')
    temp = re.findall(r'"weatherinfo":(.+?)};var',result)[0]
    
    data['data']['city'] = city
    # 当天
    res = json.loads(temp)
    today = {}
    today['high'] = res['temp']
    today['low'] = res['tempn']
    today['weather'] = res['weather']
    today['wd'] = res['wd']
    today['ws'] = res['ws']
    data['data']['today'] = today

    # 当前时刻
    temp = re.findall(r'var dataSK =(.+?);var',result)[0]
    res = json.loads(temp)
    current = {}
    current['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    current['temp'] = res['temp']
    current['weather'] = res['weather']
    current['wd'] = res['WD']
    current['ws'] = res['WS']
    current['sd'] = res['SD']
    current['pm'] = res['aqi_pm25']
    data['data']['current'] = current

    # 温馨提示

    temp = re.findall(r'var dataZS=(.+?);var',result)[0]
    res = json.loads(temp)
    res = res['zs']
    index = []

    index.append(res['ac_name']+':'+res['ac_hint']+','+res['ac_des_s'])
    index.append(res['ag_name']+':'+res['ag_hint']+','+res['ag_des_s'])
    index.append(res['cl_name']+':'+res['cl_hint']+','+res['cl_des_s'])
    index.append(res['co_name']+':'+res['co_hint']+','+res['co_des_s'])
    index.append(res['ct_name']+':'+res['ct_hint']+','+res['ct_des_s'])
    index.append(res['dy_name']+':'+res['dy_hint']+','+res['dy_des_s'])
    index.append(res['fs_name']+':'+res['fs_hint']+','+res['fs_des_s'])
    index.append(res['gj_name']+':'+res['gj_hint']+','+res['gj_des_s'])
    index.append(res['gl_name']+':'+res['gl_hint']+','+res['gl_des_s'])
    index.append(res['gm_name']+':'+res['gm_hint']+','+res['gm_des_s'])
    index.append(res['hc_name']+':'+res['hc_hint']+','+res['hc_des_s'])
    index.append(res['jt_name']+':'+res['jt_hint']+','+res['jt_des_s'])
    index.append(res['lk_name']+':'+res['lk_hint']+','+res['lk_des_s'])
    index.append(res['ls_name']+':'+res['ls_hint']+','+res['ls_des_s'])
    index.append(res['mf_name']+':'+res['mf_hint']+','+res['mf_des_s'])
    index.append(res['nl_name']+':'+res['nl_hint']+','+res['nl_des_s'])
    index.append(res['pj_name']+':'+res['pj_hint']+','+res['pj_des_s'])
    index.append(res['pk_name']+':'+res['pk_hint']+','+res['pk_des_s'])
    index.append(res['pl_name']+':'+res['pl_hint']+','+res['pl_des_s'])
    index.append(res['pp_name']+':'+res['pp_hint']+','+res['pp_des_s'])
    index.append(res['tr_name']+':'+res['tr_hint']+','+res['tr_des_s'])
    index.append(res['uv_name']+':'+res['uv_hint']+','+res['uv_des_s'])
    index.append(res['yd_name']+':'+res['yd_hint']+','+res['yd_des_s'])
    index.append(res['yh_name']+':'+res['yh_hint']+','+res['yh_des_s'])
    index.append(res['ys_name']+':'+res['ys_hint']+','+res['ys_des_s'])
    index.append(res['zs_name']+':'+res['zs_hint']+','+res['zs_des_s'])
    data['data']['index'] = '\n'.join(index)



    # 七天预报
    temp = re.findall(r'var fc=(.+?]})',result)[0]
    res = json.loads(temp)
    res = res['f']
    future = []
    i = 0
    for item in res:
        temp = {}
        temp['high'] = item['fc']
        temp['low'] = item['fd']
        temp['wd'] = item['fe']
        temp['ws'] = item['fg']
        temp['weather'] = weatherArr[item['fa']]
        temp['date'] = item['fi']
        if i == 0:
            temp['weekday'] = u'今天'
        elif i == 1:
            temp['weekday'] = u'明天'
        else:
            temp['weekday'] = time.strftime("%a",time.strptime('2018/'+item['fi'], "%Y/%m/%d"))
            temp['weekday'] = WEEK_MAP[temp['weekday']]
        i += 1
        future.append(temp)

    data['data']['future'] = future

    # 未来24小时  
    data['data']['hourly'] = get_hours_weather(city_map[city])
    return data
    

def get_hours_weather(city):

    res = []

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get('http://www.weather.com.cn/weathern/'+city+'.shtml', headers=headers)
    except:
        return res
    temp = re.findall(r'var hour3data=(.+?);var hour3week',response.text)[0]
    result = json.loads(temp)
    for item in result[0]:
        hourly = {}
        hourly['temperature'] = item['jb']
        hourly['weather'] = weatherArr[item['ja']]
        hourly['time'] = item['jf'][:4]+'-'+item['jf'][4:6]+'-'+item['jf'][6:8]+' '+item['jf'][8:]+':00:00'
        hourly['wd'] = fxArr[item['jd']]
        hourly['ws'] = flArr[item['jc']]
        res.append(hourly)
    return res

    

if __name__ == '__main__':
    print(weather_search('南京'))