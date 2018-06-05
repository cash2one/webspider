# -*- coding: utf-8 -*-

#!/usr/bin/env python
# Author: yaoqiang.xing(sandiego1895@gmail.com)
# Created Time: Tue Jun 13 10:54:01 2017

#
# 对 pymysql 进行重连的封装
#

import time
import logging
import pymysql
from pymysql.err import OperationalError
from pymysql.err import ProgrammingError

# logging.basicConfig(level=logging.INFO,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%d %b %Y %H:%M:%S',
#                 filename='log/mysql.log',
#                 )

# 初始化的时候传入参数 online type: Bool 区分线上还是线下库

class MySQLWrapper(object):
    def __init__(self, database='db_finance_economics'):
        self.database = database
        self.reconnect()

    # 当连接断开的时候就重新连接
    def reconnect(self):
        try:
           self.mysql = pymysql.connect(
                host='10.0.0.26',
                user='root',
                password='Anytrust_DB_51chacha=%.?',
                db=self.database,
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor,
                use_unicode=True,
                autocommit=True,
            )
        except Exception as e:
            logging.error("Connection mysql error")
            time.sleep(1)
            self.reconnect()

    # 只取一条记录
    def fetchOne(self, sql, *args):
        with self.mysql.cursor() as cursor:
            try:
                cursor.execute(sql, args)
            except OperationalError as e:
                logging.error("Lost connection from mysql, reconnect")
                self.reconnect()
                self.fetchOne(sql, args)

            try:
                result = cursor.fetchone()
                return result
            except ProgrammingError as e:
                logging.error("Lost connection from mysql, reconnect")
                self.reconnect()
                self.fetchOne(sql, args)

    # 取所有的记录，返回结果的 list
    def fetchAll(self, sql, *args):
        with self.mysql.cursor() as cursor:
            try:
                cursor.execute(sql, args)
            except OperationalError as e:
                logging.error("Lost connection from mysql, reconnect")
                self.reconnect()
                self.fetchAll(sql, args)

            try:
                results = cursor.fetchall()
                return results
            except ProgrammingError as e:
                logging.error("Lost connection from mysql, reconnect")
                self.reconnect()
                self.fetchAll(sql, args)

    # 执行 insert 或者 update 语句, 没有返回值
    def execute(self, sql, *args):
        with self.mysql.cursor() as cursor:
            try:
                cursor.execute(sql, args)
            except OperationalError as e:
                logging.error("Lost connection from mysql, reconnect")
                self.reconnect()
                self.execute(sql, args)

        # 执行 insert 语句, 返回 lastrowid
    def execute_insert(self, sql, *args):
        with self.mysql.cursor() as cursor:
            try:
                cursor.execute(sql, args)
                return cursor.lastrowid
            except OperationalError as e:
                logging.error("Lost connection from mysql, reconnect")
                self.reconnect()
                self.execute_insert(sql, args)
    # 执行 insert 或者 update 语句, 输入是元组，没有返回值
    def execute_list(self, sql, *args):
        with self.mysql.cursor() as cursor:
            try: 
                cursor.execute(sql, args[0])
            except OperationalError as e:
                logging.error("Lost connection from mysql, reconnect")
                self.reconnect()
                self.execute(sql, args)

def main():
    mysql = MySQLWrapper()
    for x in xrange(1,100):
        sql = "SELECT * FROM `m_article_state` WHERE `id` = %s"
        result = mysql.fetchOne(sql, 1)
        print (result)
        time.sleep(4)

if __name__ == '__main__':
    main()































