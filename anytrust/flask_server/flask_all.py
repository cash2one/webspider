from flask import Flask
from flask import request
from flask import Response
from phone import *
from IPsearch import *
import express
from weather import *
from translate import *
import json
app = Flask(__name__)

@app.route('/server/phone', methods=['GET', 'POST'])
def phone_parse():
	if request.method == 'GET':
		phone_number = request.args.get('phonenumber')
		result = {}
		# result['baiduweishi'] = baiduweishi_phone(phone_number)
		result['baidu'] = baidu_phone(phone_number)
		result['so360'] = so360_phone(phone_number)
		result['taobao'] = taobao_API(phone_number)
		result['sogou'] = sogou_phnoe(phone_number)
		return json.dumps(result)

@app.route('/server/IP', methods=['GET', 'POST'])
def IP_parse():
	if request.method == 'GET':
		IP = request.args.get('IP')
		result = {}
		result['baidu'] = baidu_IP(IP)
		result['sina'] = sina_api(IP)
		result['taobao'] = taobao_API_IP(IP)
		result['tool'] = tool_lu(IP)
		result['afanda'] = afanda_API_IP(IP)
		return json.dumps(result)

@app.route('/server/express', methods=['GET', 'POST'])
def express_parse():
	if request.method == 'GET':
		num = request.args.get('num')
		result = express.run(num)
		return json.dumps(result)

@app.route('/server/weather', methods=['GET', 'POST'])
def weather_parse():
	if request.method == 'GET':
		city = request.args.get('city')
		result = weather_search(city)
		return json.dumps(result)

@app.route('/server/translate', methods=['GET', 'POST'])
def translate_parse():
	if request.method == 'GET':
		text = request.args.get('text')
		t_type = request.args.get('type')
		t = Translate()
		result = t.run(text,t_type)
		resp = Response(json.dumps(result))
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp
		# return json.dumps(result)
		# return "trans("+json.dumps(result)+")"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080,debug=True)
