#author = liuwei date = 2017-06-02
#数据库帮助类
import pymysql
from book import *
import datetime

__metaclass__ = type
class DBHelper:
	def __init__(self):
		# 获取操作数据库的curcor即游标，首先的建立连接，需要服务器地址，端口号，用户名，密码和数据库名
		# 为了能用中文，得加上编码方式
		conn = pymysql.connect(host="localhost", port=3306, user="root", password="Li123456!", db='图书馆管理系统',
		                       charset="utf8", autocommit=1)
		cursor = conn.cursor()
		self.conn = conn
		self.cursor = cursor

	def insertBook(self, book):
		'''向数据库中book表插入书本信息，book为Book类对象，包含书本基本信息'''
		sql = "insert into 图书(书名, 作者) values(%s, %s)"

		self.cursor.execute(sql, (book.getBookName(), book.getAuthor()))

		self.conn.commit()

		new_id = self.cursor.lastrowid
		print("新插入键值id为:", new_id)

		return new_id

	def getAllBook(self):
		'''返回数据库中，book表中所有的书本信息'''
		sql = "select *from 图书"

		rownum = self.cursor.execute(sql)              #执行并返回找到的行数

		#获取查询结果
		rows = self.cursor.fetchall()
		list = []

		for item in rows:
			bitem = (item[0], item[1], item[2], item[3], item[4], item[5])

			list.append(bitem)

		self.conn.commit()

		return list

	def getBookById(self, bookid):
		# 根据书本id值来寻找书本信息

		sql = "select * from 图书  where 书号=%s"

		self.cursor.execute(sql, (bookid,))                     #参数以元组形式给出
		row = self.cursor.fetchone()                             #取到第一个结果

		self.conn.commit()

		return row                                          #返回该书本信息

	def getStudentById(self, studentid):
		
		sql = "select * from 读者 where 学号=%s"

		self.cursor.execute(sql, (studentid,))                     #参数以元组形式给出
		row = self.cursor.fetchone()                             #取到第一个结果

		self.conn.commit()

		return row

	def bookOwned(self, studentid):
		sql = "select * from 借阅信息 where 学号=%s"

		self.cursor.execute(sql, (studentid,))                     #参数以元组形式给出
		rows = self.cursor.fetchall()                             #取到第一个结果

		list = []

		for row in rows:
			book = self.getBookById(row[1])
			data = (row[1], book[1], str(row[2]), str(row[3]), row[4])
			list.append(data)

		self.conn.commit()

		return list

	def saveUpdate(self, bookid, book):
		# 用book对象来修改id为bookid的书本信息
		sql = "update 图书 set 图书.书名=%s, 图书.作者=%s where 图书.书号=%s"

		self.cursor.execute(sql, (book.getBookName(), book.getAuthor(), bookid))

		self.conn.commit()

	def deleteBook(self, bookid):
		# 根据书本id来删除书籍
		sql = "delete from 图书 where 图书.书号 = %s"

		self.cursor.execute(sql, (bookid, ))

		self.conn.commit()

	def getBookByName(self, bookName):

		sql = "select 书号, 可借状态, 可约状态 from 图书 where 书名 = %s"

		rownum = self.cursor.execute(sql, bookName)              #执行并返回找到的行数

		#获取查询结果
		rows = self.cursor.fetchall()
		list = []

		for row in rows:
			data = (row[0], bookName, row[1], row[2])
			list.append(data)

		self.conn.commit()

		return list

	def borrowbook(self, bookid, studentid):

		sql = "select 可借状态 from 图书 where 书号 = %s"

		self.cursor.execute(sql, bookid)

		row = self.cursor.fetchone()

		sql = "select  * from 借阅信息 where 书号 = %s"
		self.cursor.execute(sql, bookid)
		book_status = self.cursor.fetchone()
		sql = "select 学号 from 预约信息 where 书号 = %s"
		self.cursor.execute(sql, bookid)
		reader_order = self.cursor.fetchone()
		if row[0] == 1:
			sql = "select  已借图书数, 罚款 from 读者 where 学号 = %s"
			self.cursor.execute(sql, studentid)
			status = self.cursor.fetchone()
			if status[0] == 3:
				return 2
			if status[1] > 0:
				return 3 
			sql = "update 图书 set 图书.可借状态 = 0, 图书.可约状态 = 1 where 书号 = %s"
			self.cursor.execute(sql, (bookid))
			sql = "update 读者 set 已借图书数 = 已借图书数 + 1 where 学号 = %s"
			self.cursor.execute(sql, studentid)
			sql = "update 读者 set 可借图书数 = 可借图书数 - 1 where 学号 = %s"
			self.cursor.execute(sql, studentid)
			sql = "select curdate()"
			self.cursor.execute(sql)
			time = str(self.cursor.fetchone())
			time = time.strip('(datetime.date(').strip('),)').replace(', ','-').replace('-1-','-01-').replace('-2-','-02-').replace('-3-','-03-').replace('-4-','-04-').replace('-5-','-05-').replace('-6-','-06-').replace('-7-','-07-').replace('-8-','-08-').replace('-9-','-09-')
			realtime = datetime.date(*map(int,time.split('-')))
			delytime = realtime+datetime.timedelta(days=30)
			sql = "insert into 借阅信息(学号,书号,借书日期,还书日期,续借状态) values(%s,%s,%s,%s,%s)"
			self.cursor.execute(sql, (studentid,bookid,realtime,delytime,0))
			return 0
		elif reader_order is None:
			return 1
		elif book_status is None and reader_order[0] == studentid:
			sql = "select 已借图书数, 罚款 from 读者 where 学号 = %s"
			self.cursor.execute(sql, studentid)
			status = self.cursor.fetchone()
			if status[0] == 3:
				return 2
			if status[1] > 0:
				return 3
			sql = "delete from 预约信息 where 学号 = %s and 书号 = %s"
			self.cursor.execute(sql, (studentid, bookid))
			sql = "update 图书 set 图书.可借状态 = 0, 图书.可约状态 = 1 where 书号 = %s"
			self.cursor.execute(sql, (bookid))
			sql = "update 读者 set 已借图书数 = 已借图书数 + 1 where 学号 = %s"
			self.cursor.execute(sql, studentid)
			sql = "update 读者 set 可借图书数 = 可借图书数 - 1 where 学号 = %s"
			self.cursor.execute(sql, studentid)
			sql = "select curdate()"
			self.cursor.execute(sql)
			time = str(self.cursor.fetchone())
			time = time.strip('(datetime.date(').strip('),)').replace(', ', '-').replace('-1-', '-01-').replace('-2-','-02-').replace('-3-', '-03-').replace('-4-', '-04-').replace('-5-', '-05-').replace('-6-', '-06-').replace('-7-','-07-').replace('-8-', '-08-').replace('-9-', '-09-')
			realtime = datetime.date(*map(int, time.split('-')))
			delytime = realtime + datetime.timedelta(days=30)
			sql = "insert into 借阅信息(学号,书号,借书日期,还书日期,续借状态) values(%s,%s,%s,%s,%s)"
			self.cursor.execute(sql, (studentid, bookid, realtime, delytime, 0))
			return 4
		else:
			return 1

	def renewBook(self, bookid):

		sql1 = "select 续借状态 from 借阅信息 where 书号 = %s"
		sql2 = "select date_add(还书日期, interval 1 month)from 借阅信息 where 借阅信息.书号 = %s"
		sql3 = "update 借阅信息 set 续借状态 = 1, 还书日期 = %s where 书号 = %s"
		sql4 = "select 可约状态 from 图书 where 书号  = %s"
		conn = self.getCon()

		self.cursor.execute(sql4, bookid)
		a = self.cursor.fetchone()
		if a[0] == 0:
			return 2
		self.cursor.execute(sql1, bookid)
		status = self.cursor.fetchone()
		if status[0] == '1':
			return 1
		else:
			self.cursor.execute(sql2, bookid)
			date = self.cursor.fetchone()
			self.cursor.execute(sql3, (date, bookid))
			return str(date).strip('(datetime.date(').strip('),)').replace(', ', '-').replace('-1-', '-01-').replace(
				'-2-', '-02-').replace('-3-', '-03-').replace('-4-', '-04-').replace('-5-', '-05-').replace('-6-',
																											'-06-').replace(
				'-7-', '-07-').replace('-8-', '-08-').replace('-9-', '-09-')
	def getReservedBook(self, studentid):

		sql1 = "select 书号 from 预约信息 where 学号 = %s"

		self.cursor.execute(sql1, studentid)
		book = self.cursor.fetchone()
		if book is None:
			return '无'
		sql2 = "select 书名 from 图书 where 书号 = %s"
		self.cursor.execute(sql2, book[0])
		bookname = self.cursor.fetchone()

		return bookname[0]

	def payFine(self,studentid):

		sql_1 = "update 读者 set 罚款 = 0 where 学号 = %s"
		sql_2 = "update 借阅信息 set 还书日期 = %s where 学号 = %s"

		self.cursor.execute(sql_1, (studentid,))
		self.cursor.execute(sql_2, (datetime.date.today(), studentid))

		self.conn.commit()

	def quitreserve(self, studentid):
		sql1 = "select 书号 from 预约信息 where 学号 = %s"
		sql2 = "delete from 预约信息 where 学号 = %s"

		self.cursor.execute(sql1, (studentid,))
		bookid = self.cursor.fetchone()

		if bookid is None:
			return 0
		else:
			self.cursor.execute(sql2,(studentid,))

			sql3 = "update 图书 set 可约状态 = 1 where 书号 = %s"
			self.cursor.execute(sql3, (bookid[0],))

			self.conn.commit()
			return 1

	def login_A(self, book):
		sql = "select 密码 from 管理员 where 管理员.账号 = %s"

		self.cursor.execute(sql,(book.getpersonalid()))
		password = str(self.cursor.fetchone())
		password = password.strip("('").strip(",)'")
		self.conn.commit()
		return password

	def login_R(self, book):
		sql = "select 密码 from 读者 where 读者.学号 = %s"

		self.cursor.execute(sql,(book.getpersonalid()))
		password = str(self.cursor.fetchone())
		password = password.strip("('").strip(",)'")
		self.conn.commit()
		return password
		
	def time_update(self, nowtime):
		sql = 'select 当前时间 from 时间表 where 时间表.时间 = "time"'
		self.cursor.execute(sql)
		ntime = str(self.cursor.fetchone())
		ntime = ntime.strip('(datetime.date(').strip('),)').replace(', ','-').replace('-1-','-01-').replace('-2-','-02-').replace('-3-','-03-').replace('-4-','-04-').replace('-5-','-05-').replace('-6-','-06-').replace('-7-','-07-').replace('-8-','-08-').replace('-9-','-09-')
		if ntime != nowtime:
			sql1 = 'update 时间表 set 时间表.当前时间 = %s where 时间表.时间="time"'
			self.cursor.execute(sql1, nowtime)
			print("时间更新了！")
			return 1
		self.conn.commit()
		return 0
	
	def getBookRend(self, bookid):
		sql = 'select 可借状态 from 图书 where 图书.书号 = %s'
		sql1 = 'select 可约状态 from 图书 where 图书.书号 = %s'

		self.cursor.execute(sql, bookid)
		rend = str(self.cursor.fetchone()).strip('(').strip(',)')
		self.cursor.execute(sql1, bookid)
		appoint = str(self.cursor.fetchone()).strip('(').strip(',)')
		self.conn.commit()
		return rend, appoint

	def MakeBookRend(self, readerid, bookid):
		sql = 'update 图书 set 可约状态 = 0 where 图书.书号 = %s'
		sql1 = 'select 还书日期 from 借阅信息 where 借阅信息.书号 = %s'
		sql2 = "insert into 预约信息(学号, 书号, 取书日期) values(%s, %s, %s)"
		self.cursor.execute(sql, bookid)
		self.cursor.execute(sql1, bookid)
		time = str(self.cursor.fetchone())
		time = time.strip('(datetime.date(').strip('),)').replace(', ','-').replace('-1-','-01-').replace('-2-','-02-').replace('-3-','-03-').replace('-4-','-04-').replace('-5-','-05-').replace('-6-','-06-').replace('-7-','-07-').replace('-8-','-08-').replace('-9-','-09-')
		realtime = datetime.date(*map(int, time.split('-')))
		delytime = realtime+datetime.timedelta(days=3)
		print(realtime)
		print(delytime)
		self.cursor.execute(sql2, (readerid, bookid, delytime))
		self.conn.commit()

	def update_pass(self, readerid, password):
		sql = "update 读者 set 密码 = %s where 读者.学号 = %s"

		self.cursor.execute(sql, (password, readerid))
		self.conn.commit()

	def getPass(self, readerid):
		sql = "select 密码 from 读者 where 读者.学号 = %s"

		self.cursor.execute(sql, (readerid,))
		row = self.cursor.fetchone()

		self.conn.commit()

		return row

	def autocancel(self):
		sql1 = "select * from 预约信息 where 取书日期 < %s"
		sql2 = 'select 当前时间 from 时间表 where 时间表.时间 = "time"'

		self.cursor.execute(sql2)
		time = self.cursor.fetchone()

		self.cursor.execute(sql1, time)
		rows = self.cursor.fetchall()
		if rows == None:
			return
		for row in rows:
			self.quitreserve(row[0])

	def money(self, now_time):
		moneyall = {}
		sql = 'select 学号,还书日期 from 借阅信息'

		self.cursor.execute(sql)
		lists = self.cursor.fetchall()
		for i in lists:
			a = now_time - i[1]
			if i[1] < now_time:
				b = list(str(a))
				for j in range(len(b)):
					if b[j] == ' ':
						break
				c = str(b[:j]).strip('[').strip(']').replace("'", '').replace(",", '').replace(" ", '')
				d = int(c)
				moneyall[i[0]] = moneyall.get(i[0], 0) + d * 0.5
			for k,v in moneyall.items() :
				sql = 'update 读者 set 读者.罚款 = %s where 读者.学号 = %s'
				self.cursor.execute(sql, (v, k))
		self.conn.commit()


	def lasttime(self, readerid):
		sql = 'select 取书日期 from 预约信息 where 预约信息.学号 = %s'

		self.cursor.execute(sql, readerid)
		if self.cursor.rowcount == 0:
			return 0
		else:
			return str(self.cursor.fetchone()[0])

	def get_money(self, readerid):
		sql = 'select 罚款 from 读者 where 读者.学号 = %s'

		self.cursor.execute(sql, readerid)
		money = self.cursor.fetchone()[0]
		return money

	def get_app(self, bookid):
		sql = 'select 学号 from 预约信息 where 预约信息.书号 = %s'

		self.cursor.execute(sql, bookid)
		if self.cursor.rowcount == 0:
			return 1
		else:
			return 0

	def change_return_time(self, studentid):
		sql = 'update 借阅信息 set 还书日期 = %s where 借阅信息.学号 = %s'

		print(datetime.date.today())
		self.cursor.execute(sql, (datetime.date.today(), studentid))
		self.conn.commit()



