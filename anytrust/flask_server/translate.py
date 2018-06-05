# -*- coding: utf-8 -*-
import requests
import execjs
import re
import hashlib        
import time
import random

# def get_token():

#     cookies = {
#         'BAIDUID': '575F0D695828A697A7211EC4A0C1EECA:FG=1',
#         'PSTM': '1509092091',
#         'BIDUPSID': '2915CDCED18DA0E5AC98DFCC59BE14DA',
#         'REALTIME_TRANS_SWITCH': '1',
#         'FANYI_WORD_SWITCH': '1',
#         'HISTORY_SWITCH': '1',
#         'SOUND_SPD_SWITCH': '1',
#         'SOUND_PREFER_SWITCH': '1',
#         '__cfduid': 'd69f8fe0231ddac0994a658d700b7dbb91516688643',
#         'MCITY': '-131%3A',
#         'BDUSS': 'JqUExlOUNoVVlJTlEyfmdhRHRYVDIwMTRnY1Rmb0NrUW4tMmJCOW5TWWEzdzliQVFBQUFBJCQAAAAAAAAAAAEAAAB5v4EszfXK6bPJMDExAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABpS6FoaUuhaZF',
#         'locale': 'zh',
#         'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574': '1523972532,1524821811,1524824929,1525496417',
#         'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574': '1525496417',
#         'to_lang_often': '%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D',
#         'from_lang_often': '%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D',
#         'BDRCVFR[feWj1Vr5u3D]': 'I67x6TjHwwYf0',
#         'PSINO': '1',
#         'H_PS_PSSID': '1446_18194_21103_20697_26350_26183_20719',
#         'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
#     }

#     headers = {
#         'Accept-Encoding': 'gzip, deflate, sdch',
#         'Accept-Language': 'zh-CN,zh;q=0.8',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Referer': 'https://www.baidu.com/link?url=2UpKq94Hkl9lIjZpyJUm8dMaymcP_QBBVJsXpijXMAQlc5oolLcYzykorq4rRxaI6b_hRgPINl8IGDz0XX-_F_&wd=&eqid=da916d280004604f000000035aed3a85',
#         'Connection': 'keep-alive',
#         'Cache-Control': 'max-age=0',
#     }

#     params = (
#         ('aldtype', '16047'),
#     )

#     response = requests.get('http://fanyi.baidu.com/', headers=headers, params=params, cookies=cookies)
#     token = re.findall(r"token: '(.+?)'",response.text)[0]
#     sign = re.findall(r"window.gtk = (.+?);",response.text)[0]
#     return token,sign

# token,sign = get_token()
# js = '''
# "use strict";
# function a(r) {
#     if (Array.isArray(r)) {
#         for (var o = 0, t = Array(r.length); o < r.length; o++)
#             t[o] = r[o];
#         return t
#     }
#     return Array.from(r)
# }
# function n(r, o) {
#     for (var t = 0; t < o.length - 2; t += 3) {
#         var a = o.charAt(t + 2);
#         a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
#         a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
#         r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
#     }
#     return r
# }
# function e(r) {
#     var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
#     if (null  === o) {
#         var t = r.length;
#         t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
#     } else {
#         for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
#             "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
#             C !== h - 1 && f.push(o[C]);
#         var g = f.length;
#         g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
#     }
#     var u = '''+sign+'''
#       , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
#     for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
#         var A = r.charCodeAt(v);
#         128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
#         S[c++] = A >> 18 | 240,
#         S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
#         S[c++] = A >> 6 & 63 | 128),
#         S[c++] = 63 & A | 128)
#     }
#     for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
#         p += S[b],
#         p = n(p, F);
#     return p = n(p, D),
#     p ^= s,
#     0 > p && (p = (2147483647 & p) + 2147483648),
#     p %= 1e6,
#     p.toString() + "." + (p ^ m)
# }
# var i = null ;
# ''' 
# ctx = execjs.compile(js)

class Translate():

    def run(self,text='',Type='en'):
        self.text = text
        self.type = Type
        result = []

        # result['baidu'] = self.baidu_translate()        
        result.append(self.google_translate())
        result.append(self.sogou_translate())
        result.append( self.baidu_app())
        result.append(self.so360())
        result.append(self.youdao())
        result.append(self.tencent())
        return result

    def baidu_translate(self):
        result = {}
        result['text'] = self.text
        result['info'] = 'ok'
        result['fromdata'] = 'baidu'

        cookies = {
            'BAIDUID': '575F0D695828A697A7211EC4A0C1EECA:FG=1',
            'PSTM': '1509092091',
            'BIDUPSID': '2915CDCED18DA0E5AC98DFCC59BE14DA',
            'REALTIME_TRANS_SWITCH': '1',
            'FANYI_WORD_SWITCH': '1',
            'HISTORY_SWITCH': '1',
            'SOUND_SPD_SWITCH': '1',
            'SOUND_PREFER_SWITCH': '1',
            '__cfduid': 'd69f8fe0231ddac0994a658d700b7dbb91516688643',
            'MCITY': '-131%3A',
            'BDUSS': 'JqUExlOUNoVVlJTlEyfmdhRHRYVDIwMTRnY1Rmb0NrUW4tMmJCOW5TWWEzdzliQVFBQUFBJCQAAAAAAAAAAAEAAAB5v4EszfXK6bPJMDExAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABpS6FoaUuhaZF',
            'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
            'BDRCVFR[feWj1Vr5u3D]': 'I67x6TjHwwYf0',
            'PSINO': '1',
            'H_PS_PSSID': '1446_18194_21103_20697_26350_26183_20719',
            'locale': 'zh',
            'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574': '1523972532,1524821811,1524824929,1525496417',
            'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574': '1525496417',
            'to_lang_often': '%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D',
            'from_lang_often': '%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D',
        }

        headers = {
            'Origin': 'http://fanyi.baidu.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Referer': 'http://fanyi.baidu.com/?aldtype=16047',
            'X-Requested-With': 'XMLHttpRequest',
        }
        if self.type == 'en':
            data = [
              ('from', 'zh'),
              ('to', 'en'),
              ('query', self.text),
              ('simple_means_flag', '3'),
              ('sign', ctx.call('e',self.text)),
              ('token', token),
            ]
        else:
            data = [
              ('from', 'en'),
              ('to', 'zh'),
              ('query', self.text),
              ('simple_means_flag', '3'),
              ('sign', ctx.call('e',self.text)),
              ('token', token),
            ]

        response = requests.post('http://fanyi.baidu.com/v2transapi', headers=headers, cookies=cookies, data=data)
        
        result['dst'] = response.json()['trans_result']['data'][0]['dst']
        return result
    # 手机端
    def baidu_app(self): 
    
        result = {}
        result['text'] = self.text
        result['info'] = 'ok'
        result['fromdata'] = 'baidu'
        headers = {  
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}  
        url = 'http://fanyi.baidu.com/basetrans'  
        
        if self.type == 'en':
            data = {'query': self.text,  
                    'from': 'zh',  
                    'to': 'en'}
        else:
            data = {'query': self.text,  
                    'from': 'en',  
                    'to': 'zh'}
          
        response = requests.post(url, headers=headers, data=data)  
        result['dst'] = response.json()['trans'][0]['dst'] 
        return result

    def sogou_translate(self):
        result = {}
        result['text'] = self.text
        result['info'] = 'ok'
        result['fromdata'] = 'sogou'
        headers = {
            'Origin': 'http://fanyi.sogou.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json',
            'Referer': 'http://fanyi.sogou.com/',
            'X-Requested-With': 'XMLHttpRequest',
        }

        data = [
          ('from', 'auto'),
          ('to', 'en'),
          ('text', self.text),
        ]

        response = requests.post('http://fanyi.sogou.com/reventondc/translate', headers=headers, data=data)
        result['dst'] = response.json()['translate']['dit']
        return result

    def so360(self):
        result = {}
        result['text'] = self.text
        result['info'] = 'ok'
        result['fromdata'] = 'so360'
        headers = {
            'Origin': 'http://fanyi.so.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://fanyi.so.com/',
            'X-Requested-With': 'XMLHttpRequest',
        }
        if self.type == 'en':
            data = [
              ('query', self.text),
              ('eng', '0'),
            ]
        else:
            data = [
              ('query', self.text),
              ('eng', '1'),
            ]

        response = requests.post('http://fanyi.so.com/index/search', headers=headers, data=data)
        result['dst'] = response.json()['data']['fanyi']
        return result

    def google_translate(self):
        result = {}
        result['text'] = self.text
        result['info'] = 'ok'  
        result['dst'] =  ''
        result['fromdata'] = 'google'
        if len(self.text) > 4891:      
            result['info'] = u"翻译的长度超过限制！！！"
            result['dst'] = ''
            return result

        ctx = execjs.compile(""" 
            function TL(a) { 
            var k = ""; 
            var b = 406644; 
            var b1 = 3293161072; 
             
            var jd = "."; 
            var $b = "+-a^+6"; 
            var Zb = "+-3^+b+-f"; 

            for (var e = [], f = 0, g = 0; g < a.length; g++) { 
                var m = a.charCodeAt(g); 
                128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
                e[f++] = m >> 18 | 240, 
                e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
                e[f++] = m >> 6 & 63 | 128), 
                e[f++] = m & 63 | 128) 
            } 
            a = b; 
            for (f = 0; f < e.length; f++) a += e[f], 
            a = RL(a, $b); 
            a = RL(a, Zb); 
            a ^= b1 || 0; 
            0 > a && (a = (a & 2147483647) + 2147483648); 
            a %= 1E6; 
            return a.toString() + jd + (a ^ b) 
            }; 

            function RL(a, b) { 
            var t = "a"; 
            var Yb = "+"; 
            for (var c = 0; c < b.length - 2; c += 3) { 
                var d = b.charAt(c + 2), 
                d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
                d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
                a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
            } 
            return a 
            } 
            """)
        headers = {
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'zh-CN,zh;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.1431 Safari/537.36',
            'accept': '*/*',
            'referer': 'https://translate.google.cn/',
            'authority': 'translate.google.cn',
            'cookie': '_ga=GA1.3.458864498.1520130457; _gid=GA1.3.701687849.1525507788; 1P_JAR=2018-5-5-8; NID=129=Q_pcAzAGQ9bjNEBDNcldu6xplQHtjuO7XgOz9zWVujtk0s6Rs_3_Q0m_2BXt4U3FsYmlnaKVfqRwZwwmS9cu1Y3sYGX-i1cDhWy2L9PsS6LpXfL7TlPaljDKfNEE0oh1',
        }
        if self.type == 'en':   
            params = (
                ('client', 't'),
                ('sl', 'zh-CN'),
                ('tl', 'en'),
                ('hl', 'zh-CN'),
                ('dt', ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't']),
                ('ie', 'UTF-8'),
                ('oe', 'UTF-8'),
                ('source', 'btn'),
                ('ssel', '0'),
                ('tsel', '0'),
                ('kc', '0'),
                ('tk', ctx.call("TL",self.text)),
                ('q', self.text),
            )
        else:
            params = (
                ('client', 't'),
                ('sl', 'en'),
                ('tl', 'zh-CN'),
                ('hl', 'zh-CN'),
                ('dt', ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't']),
                ('ie', 'UTF-8'),
                ('oe', 'UTF-8'),
                ('source', 'btn'),
                ('ssel', '0'),
                ('tsel', '0'),
                ('kc', '0'),
                ('tk', ctx.call("TL",self.text)),
                ('q', self.text),
            )

      
        response = requests.get('https://translate.google.cn/translate_a/single', headers=headers, params=params)
      
        #返回的结果为Json，解析为一个嵌套列表
        for item in response.json()[0]:
            if not item[0]:
                break
            result['dst'] += item[0]

        return result
    def youdao(self):
        result = {}
        result['text'] = self.text
        result['info'] = 'ok'
        result['dst'] = ''
        result['fromdata'] = 'youdao'
        cookies = {
            'OUTFOX_SEARCH_USER_ID': '918711871@10.169.0.84',
            'SESSION_FROM_COOKIE': 'sogou-inc',
            'JSESSIONID': 'aaadFw_iuOcuM9jfECVmw',
            'fanyi-ad-id': '43155',
            'fanyi-ad-closed': '1',
            '___rl__test__cookies': '1525509358844',
        }

        headers = {
            'Origin': 'http://fanyi.youdao.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://fanyi.youdao.com/',
            'X-Requested-With': 'XMLHttpRequest',
        }

        params = (
            ('smartresult', ['dict', 'rule']),
        )
        c = 'ebSeFb%=XZ%T[KZ)c(sy!'
        f = str(int(time.time()*1000)+random.randint(1,10))
        sign = hashlib.md5(('fanyideskweb' + self.text + f + c).encode('utf-8')).hexdigest()
        data = [
          ('i', self.text),
          ('from', 'AUTO'),
          ('to', 'AUTO'),
          ('client', 'fanyideskweb'),
          ('salt', f),
          ('sign', sign),
          ('version', '2.1'),
          ('keyfrom', 'fanyi.web'),
        ]

        response = requests.post('http://fanyi.youdao.com/translate_o', headers=headers, params=params, cookies=cookies, data=data)
        try:
            res = response.json()
        except:
            result['info'] = u'IP被封'
            return result
        for item in response.json()['translateResult'][0]:
            result['dst'] += ' '+item['tgt']
        result['dst'] = result['dst'].strip()
        return result

    def tencent(self):
        result = {}
        result['text'] = self.text
        result['info'] = 'ok'
        result['dst'] = ''
        result['fromdata'] = 'tencent'

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Connection': 'keep-alive',
            'Content-Length': str(len(self.text)),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'pgv_pvi=9432833024; pgv_pvid=696146472; pt2gguin=o1587321194; RK=KmjFU/5Feb; ptcz=43b52536e102f04affcaa5195f2759b963184e8aadecc4f0a27f91f7c6dab551; o_cookie=1587321194; pac_uid=1_1587321194; fy_guid=0bbb1e9b-7445-48f3-9af2-cb20e4ffb719; qtv=ba3ee1066bd2db5e; qtk=TivQcEjWIptgqk0N9/acu+5CqcstMtagb8HZd/N9r05J+3sbh98+7KQepq/63yM2mnZZX+7YSN9Rbnu/oWqxF8/Gsxa3GQQhZkPqO7KvvVPpTg4CC64Q5EFVPDfwc1YiUn6aUhvzJXjM2T5oYeNlpw==; pgv_info=ssid=s16002504; ts_last=fanyi.qq.com/; ts_refer=www.baidu.com/link; ts_uid=2762457210; openCount=1',
            'Host': 'fanyi.qq.com',
            'Origin': 'http://fanyi.qq.com',
            'Referer': 'http://fanyi.qq.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        f = str(int(time.time()*1000)+random.randint(100,1000))
        data = [
            ('source', 'auto'),
            # ('target', 'en'),
            ('sourceText', self.text),
            ('sessionUuid', 'translate_uuid'+f),

        ]
        
        response = requests.post('http://fanyi.qq.com/api/translate', headers=headers, data=data)
        try:
            res = response.json()
        except:
            result['info'] = u'IP被封'
            return result
        if not res['translate']['records']:
            result['info'] = u'访问过于频繁，请稍后尝试。'
            return result
        for item in res['translate']['records']:
            result['dst'] += ' '+item['targetText']
        result['dst'] = result['dst'].strip()
        return result
        
if __name__ == '__main__':
    t = Translate()
    print(t.run(u'没钱就别买车。贷款其实就是饮鸩止渴的做法。买车不能给你带来更多利润的情况下千万不要贷款买车。'))
    print(t.run('hello,world','zh'))
