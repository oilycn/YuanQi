# -*- coding: utf-8 -*-
import pymysql
import redis
import json


def process_item():
	rediscli = redis.Redis (host='127.0.0.1', port=6379, db=0)
	# 1. 建立数据库的连接
	connect = pymysql.connect (
		# localhost连接的是本地数据库
		host='localhost',
		# mysql数据库的端口号
		port=3306,
		# 数据库的用户名
		user='root',
		# 本地数据库密码
		passwd='777',
		# 表名
		db='scrapyDB',
		# 编码格式
		charset='utf8'
	)
	# 2. 创建一个游标cursor, 是用来操作表。
	cursor = connect.cursor ()
	i = 0
	while True:
		# 将数据从redis里pop出来
		source, data = rediscli.blpop ("qc:items")
		item = json.loads (data)
		print (len (source))
		try:
			# 3. 将Item数据放入数据库
			sql = "INSERT INTO job(title,money,url,company,company_url,loc,time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
				item['title'], item['money'], item['url'], item['company'], item['company_url'], item['loc'],
				item['time'])
			cursor.execute (sql)
			# 4. 提交操作
			connect.commit ()
			# 5. 关闭游标
			# cursor.close()
			i += 1
			print ("已插入：" + str (i) + "条数据")
		except:
			pass


if __name__ == "__main__":
	process_item ()
