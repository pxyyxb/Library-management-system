# 数据库帮助类
import pymysql
from reader import *

__metaclass__ = type
class ReaderHelper:
    def getCon(self):
        # 获取操作数据库的curcor即游标，首先的建立连接，需要服务器地址，端口号，用户名，密码和数据库名
		# 为了能用中文，加上编码方式
        conn = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "123456", db = "图书馆管理系统" , charset = "utf8", autocommit = 1)
        return conn

    def insertReader(self, reader):

        sql = "insert into 读者(学号, 密码, 姓名, 性别, 学院, 电话, 已借图书数, 可借图书数, 罚款) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        conn = self.getCon()
        if conn ==None:
            return

        cursor = conn.cursor()
        cursor.execute(sql, (reader.getReaderid(), reader.getPassword(), reader.getReaderName(), reader.getSex(), reader.getDept(), reader.getTelephone(), reader.getBorrow_num(), reader.getAble_num(), reader.getMoney()))

        conn.commit()
        cursor.close()
        conn.close()
        return

    def getAllReader(self):
        sql = "select 学号, 姓名, 已借图书数, 可借图书数, 罚款 from 读者"

        conn = self.getCon()
        if conn == None:
            return

        cursor = conn.cursor()
        # 执行并返回找到的行数
        rownum = cursor.execute(sql)

        # 获取查询结果
        rows = cursor.fetchall()
        '''
        list = []

        for item in rows:
            bitem = (item[0], item[1], item[2], item[3], item[4])
            list.append(bitem)
        '''
        conn.commit()
        cursor.close()
        conn.close()

        return rows

    def getReaderById(self,readerid):

        sql = "select 学号, 密码, 姓名, 性别, 学院, 电话, 已借图书数, 可借图书数, 罚款 from 读者  where 学号 = %s"

        conn = self.getCon()
        if conn == None:
            return

        cursor = conn.cursor()
        cursor.execute(sql, (readerid, ))                     # 参数以元组形式给出
        row = cursor.fetchone()                               # 取到一条匹配结果

        conn.commit()
        cursor.close()
        conn.close()
        return row                                          # 返回该书本信息

    def getReaderByName(self, readerName):
        sql = "select 学号, 密码, 姓名, 性别, 学院, 电话, 已借图书数, 可借图书数, 罚款 from 读者 where 姓名 = %s"

        conn = self.getCon()
        if conn == None:
            return

        cursor = conn.cursor()
        cursor.execute(sql, (readerName, ))
        # row是一个二维元组
        row = cursor.fetchall()                             # 取到全部匹配结果

        conn.commit()
        cursor.close()
        conn.close()

        return row

    def getReaderByBoth(self, readerid, readerName):
        # 根据书名来寻找书本信息
        sql = "select 学号, 密码, 姓名, 性别, 学院, 电话, 已借图书数, 可借图书数, 罚款 from 读者 where 学号 = %s and 姓名 = %s"

        conn = self.getCon()
        if conn == None:
            return

        cursor = conn.cursor()
        cursor.execute(sql, (readerid, readerName, ))
        row = cursor.fetchone()                             # 取到全部匹配结果

        conn.commit()
        cursor.close()
        conn.close()

        return row

    def saveUpdate_reader(self, readerid, reader):

        sql = "update 读者 set 读者.学号=%s, 读者.密码 = %s, 读者.姓名=%s, 读者.性别=%s, 读者.学院=%s, 读者.电话=%s, 读者.已借图书数=%s, 读者.可借图书数=%s, 读者.罚款 = %s  where 读者.学号=%s"

        conn = self.getCon()
        if conn == None:
            return

        cursor = conn.cursor()
        cursor.execute(sql, (reader.getReaderid(), reader.getPassword(), reader.getReaderName(), reader.getSex(), reader.getDept(), reader.getTelephone(), reader.getBorrow_num(), reader.getAble_num(), reader.getMoney(), readerid))

        conn.commit()
        cursor.close()
        conn.close()
    def saveUpdate_read(self, readerid, reader):

        sql = "update 读者 set 读者.学号=%s, 读者.姓名=%s, 读者.性别=%s, 读者.学院=%s, 读者.电话=%s, 读者.已借图书数=%s, 读者.可借图书数=%s, 读者.罚款 = %s  where 读者.学号=%s"

        conn = self.getCon()
        if conn == None:
            return

        cursor = conn.cursor()
        cursor.execute(sql, (reader.getReaderid(), reader.getReaderName(), reader.getSex(), reader.getDept(), reader.getTelephone(), reader.getBorrow_num(), reader.getAble_num(), reader.getMoney(), readerid))

        conn.commit()
        cursor.close()
        conn.close()

    def selectBook(self, readerid):
        sql_1 = "update 图书 set 可约状态 = 1 where 书号 in (select 书号 from 预约信息 where 学号 = %s)"
        sql_2 = "delete from 预约信息 where 学号= %s"
        sql_3 = "select 书号 from 借阅信息 where 学号 = %s"
        sql_4 = "delete from 借阅信息 where 学号 = %s"

        conn = self.getCon()
        if conn == None:
            return

        cursor = conn.cursor()
        cursor.execute(sql_1, (readerid,))
        cursor.execute(sql_2, (readerid,))
        cursor.execute(sql_3, (readerid,))
        row = cursor.fetchall()
        cursor.execute(sql_4, (readerid,))
          # 取到全部匹配结果

        conn.commit()
        cursor.close()
        conn.close()

        return row

    def deleteBook(self, bookid):
        # 根据读者id来删除书籍
        sql = "delete from 图书 where 图书.书号 = %s"
        conn = self.getCon()
        if conn == None:
            return

        cursor = conn.cursor()
        cursor.execute(sql, (bookid,))

        conn.commit()
        cursor.close()
        conn.close()

    def deleteReader(self, readerid):
        sql = "delete from 读者 where 读者.学号 = %s"
        conn = self.getCon()
        if conn == None:
            return

        cursor = conn.cursor()
        cursor.execute(sql, (readerid,))

        conn.commit()
        cursor.close()
        conn.close()

if __name__ == '__main__':
    db = ReaderHelper()
    list = db.getAllReader()
    for item in list:
        print(item)

