# 数据库帮助类
import datetime
import pymysql
from book import *
from reader import *

__metaclass__ = type

class BorrowHelper:
	def getCon(self):
		# 获取操作数据库的curcor即游标，首先的建立连接，需要服务器地址，端口号，用户名，密码和数据库名
		# 为了能用中文，加上编码方式
		conn = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "123456", db = "图书馆管理系统", charset = "utf8", autocommit = 1)
		return conn

	def delete_record(self, readerid, bookid):
		# 根据书本id和读者id从借书表中删除借书记录
		sql = "delete from 借阅信息 where 借阅信息.学号 = %s and 借阅信息.书号 = %s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (readerid, bookid, ))

		conn.commit()
		cursor.close()
		conn.close()

	def pre_bookborrow(self, bookid):
		# 根据书本id从图书表中找到该图书的预约状态
		sql = "select 可约状态 from 图书 where 图书.书号 = %s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (bookid, ))

		row = cursor.fetchone()

		conn.commit()
		cursor.close()
		conn.close()

		return row[0]

	def pre_reader(self, readerid):
		sql = "select 已借图书数, 可借图书数 from 读者 where 读者.学号 = %s"
		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (readerid,))

		row = cursor.fetchone()

		conn.commit()
		cursor.close()
		conn.close()

		return row

	def update_book(self, bookid) :
		# 用book对象来修改id为bookid的书本信息
		sql = "update 图书 set 图书.可借状态 = %s, 图书.可约状态 = %s where 图书.书号=%s"

		conn = self.getCon()
		if conn == None:
			 return

		cursor = conn.cursor()
		cursor.execute(sql, (str(1), str(0), bookid))


		conn.commit()
		cursor.close()
		conn.close()

	def update_reader(self, readerid, borrow_num, able_num ):
		# 用reader对象来修改id为readerid的读者信息
		sql = "update 读者 set 读者.已借图书数 = %s, 读者.可借图书数 = %s where 读者.学号=%s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (borrow_num, able_num, readerid))

		conn.commit()
		cursor.close()
		conn.close()

	def change_time(self, bookid):
		sql = 'update 预约信息 set 预约信息.取书日期 = %s where 预约信息.书号 = %s'
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, (datetime.date.today()+datetime.timedelta(days=3), bookid))
		conn.commit()
		cursor.close()
		conn.close()

	