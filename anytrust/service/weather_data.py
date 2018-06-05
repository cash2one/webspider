import requests
import sys
sys.path.append("/ROOT/www/spider/settings")
from mysql import MySQLWrapper

mysql = MySQLWrapper('db_weather')

def run():
	select_sql = 'SELECT f_City FROM t_city  WHERE f_UID >= (SELECT MAX(f_UID) FROM t_city ) * RAND() LIMIT 5'
	result = mysql.fetchOne(select_sql)
    params = (
    	('city',result['f_City']),
    	)
    response = requests.get('10.0.0.26:8080/server/weather',params=params)
    res = response.json()

    insert_sql = 'INSERT INTO t_weather(f_City,f_Json)VALUES(%s,%s)'
    select_sql = 'SELECT * FROM t_weather WHERE f_City=%s'
    update_sql = 'UPDATE t_weather SET f_Json=%s WHERE f_City=%s'
    

    flag = mysql.fetchOne(select_sql,city)
    if flag:
        mysql.execute(update_sql,res,city)
    else:
        mysql.execute(insert_sql,city,json)

if __name__ == '__main__':
    run()