# 数据库帮助类
import pymysql
from book import *

__metaclass__ = type
class BookHelper:
	def getCon(self):
		# 获取操作数据库的curcor即游标，首先的建立连接，需要服务器地址，端口号，用户名，密码和数据库名
		# 为了能用中文，加上编码方式
		conn = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "123456", db = "图书馆管理系统", charset = "utf8", autocommit = 1)
		return conn

	def insertBook(self, book):
		# 向数据库中book表插入书本信息，book为Book类对象，包含书本基本信息
		sql = "insert into 图书(书号, 书名, 作者, 出版社, 可借状态, 可约状态) values(%s, %s, %s, %s, %s, %s)"

		conn = self.getCon()
		if conn ==None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (book.getBookid(), book.getBookName(), book.getAuthor(), book.getPublish(), book.getBorrow(), book.getOrder()))


		conn.commit()
		cursor.close()
		conn.close()
		return

	def getAllBook(self):
		# 返回数据库中，book表中所有的书本信息
		sql = "select *from 图书"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		# 执行并返回找到的行数
		rownum = cursor.execute(sql)

		# 获取查询结果
		rows = cursor.fetchall()
		list = []

		for item in rows:
			bitem = (item[0], item[1], item[2], item[3], item[4], item[5])
			list.append(bitem)

		conn.commit()
		cursor.close()
		conn.close()

		return list

	def getBookById(self, bookid):
		# 根据书本id值来寻找书本信息

		sql = "select * from 图书  where 书号 = %s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (bookid, ))                     # 参数以元组形式给出
		row = cursor.fetchone()                               # 取到一条匹配结果

		conn.commit()
		cursor.close()
		conn.close()

		return row                                          # 返回该书本信息

	def getBookByName(self, bookName):
		# 根据书名来寻找书本信息
		sql = "select * from 图书 where 书名 = %s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (bookName, ))
		# row是一个二维元组
		row = cursor.fetchall()                             # 取到全部匹配结果

		conn.commit()
		cursor.close()
		conn.close()

		return row

	def getBookByBoth(self, bookid, bookName):
		# 根据书名来寻找书本信息
		sql = "select * from 图书 where 书号 = %s and 书名 = %s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (bookid, bookName, ))
		row = cursor.fetchone()                             # 取到全部匹配结果

		conn.commit()
		cursor.close()
		conn.close()

		return row

	def saveUpdate(self, bookid, book):
		# 用book对象来修改id为bookid的书本信息
		sql = "update 图书 set 图书.书号=%s, 图书.书名=%s, 图书.作者=%s, 图书.出版社=%s, 图书.可借状态=%s, 图书.可约状态=%s where 图书.书号=%s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (book.getBookid(), book.getBookName(), book.getAuthor(), book.getPublish(), book.getBorrow(), book.getOrder(), bookid))

		conn.commit()
		cursor.close()
		conn.close()

	def deleteBook(self, bookid):
		# 根据书本id来删除书籍
		sql_1 = "update 读者 set 已借图书数 = 已借图书数 - 1, 可借图书数 = 可借图书数 + 1 where 学号 = (select 学号 from 借阅信息 where 书号 = %s)"
		sql_2 = "delete from 借阅信息 where 借阅信息.书号 = %s"
		sql_3 = "delete from 预约信息 where 预约信息.书号 = %s"
		sql_4 = "delete from 图书 where 图书.书号 = %s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql_1, (bookid,))
		cursor.execute(sql_2, (bookid,))
		cursor.execute(sql_3, (bookid,))
		cursor.execute(sql_4, (bookid,))

		conn.commit()
		cursor.close()
		conn.close()



if __name__ == '__main__':
	db = BookHelper()
	list = db.getAllBook()
	for item in list:
		print(item)

