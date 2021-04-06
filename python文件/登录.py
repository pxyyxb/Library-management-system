import wx
from log import *
from dbhelper_s import *
from datetime import * 
from book_system import *
from reader_system import *
from student import *
now_time = str(date.today())#.__format__('%Y-%m-%d')#用字符串表示的当前日期,如"2019-08-16"
__metaclass__ = type
class logFrame_A(wx.Frame):
	'''管理员登录窗口'''
	def __init__(self, parent, title):
		'''初始化该小窗口的布局'''

		self.parent = parent#保存其父界面，下面会用到
		#生成一个400*200的框
		wx.Frame.__init__(self, parent, title = title, size = (400, 200))

		self.panel = wx.Panel(self, pos = (0, 0), size = (400, 200))
		self.panel.SetBackgroundColour("#FFFFFF")                              #背景为白色

		#2个编辑框，分别用来编辑账号和密码
		ID_tip = wx.StaticText(self.panel, label = "账号:", pos = (5 , 8), size = (35, 25))
		ID_tip.SetBackgroundColour("#FFFFFF")
		ID_text = wx.TextCtrl(self.panel, pos = (40, 5), size = (340, 25))
		self.ID = ID_text

		password_tip = wx.StaticText(self.panel, label = "密码:", pos = (5, 38), size = (35, 25))
		password_tip.SetBackgroundColour("#FFFFFF")
		password_text = wx.TextCtrl(self.panel, pos = (40, 35), size = (340, 25))
		self.password = password_text
		
		log_button = wx.Button(self.panel, label = "登录", pos = (160, 90))
		self.Bind(wx.EVT_BUTTON, self.admin_log, log_button)

		#需要用到的数据库接口
		self.dbhelper = DBHelper()

	def admin_log(self, evt):
		'''第一步：获取text中文本；第二步，连接数据库；第三步插入并获得主键；第四步添加到ListCtrl中'''
		personalid = self.ID.GetValue()
		password = self.password.GetValue()

		if personalid == "" or password == "":
			warn = wx.MessageDialog(self, message = "账户或密码不能为空！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		else:
			print("开始查询数据库")
			book = Log(personalid, password)
			realpassword = self.dbhelper.login_A(book)
			if realpassword == password:
				print("登录成功")
				admin_f = R_or_B(self.parent, "选择图书管理或读者管理")#将其父界面设为其爷界面
				admin_f.Show(True)
				self.Destroy()
			else:
				print("登录失败")
				warn = wx.MessageDialog(self, message = "账户或密码错误！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()                                                             #提示错误
				warn.Destroy()

class logFrame_R(wx.Frame):
	'''登录窗口'''
	def __init__(self, parent, title):
		'''初始化该小窗口的布局'''

		self.parent = parent
		#生成一个400*200的框
		wx.Frame.__init__(self, parent, title = title, size = (400, 200))

		self.panel = wx.Panel(self, pos = (0, 0), size = (400, 200))
		self.panel.SetBackgroundColour("#FFFFFF")                              #背景为白色

		#2个编辑框，分别用来编辑账号和密码
		ID_tip = wx.StaticText(self.panel, label = "账号:", pos = (5 , 8), size = (35, 25))
		ID_tip.SetBackgroundColour("#FFFFFF")
		ID_text = wx.TextCtrl(self.panel, pos = (40, 5), size = (340, 25))
		self.ID = ID_text

		password_tip = wx.StaticText(self.panel, label = "密码:", pos = (5, 38), size = (35, 25))
		password_tip.SetBackgroundColour("#FFFFFF")
		password_text = wx.TextCtrl(self.panel, pos = (40, 35), size = (340, 25))
		self.password = password_text
		
		log_button = wx.Button(self.panel, label = "登录", pos = (160, 90))
		self.Bind(wx.EVT_BUTTON, self.reader_log, log_button)

		#需要用到的数据库接口
		self.dbhelper = DBHelper()

	def reader_log(self, evt):
		'''第一步：获取text中文本；第二步，连接数据库；第三步插入并获得主键；第四步添加到ListCtrl中'''
		personalid = self.ID.GetValue()
		password = self.password.GetValue()

		if personalid == "" or password == "":
			warn = wx.MessageDialog(self, message = "账户或密码不能为空！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		else:
			print("开始查询数据库")
			book = Log(personalid, password)
			realpassword = self.dbhelper.login_R(book)
			if realpassword == password:
				print("登录成功")
				frame = studentFrame(None, "library-system",personalid)
				frame.Show()
				self.Destroy()
			else:
				print("登录失败")
				warn = wx.MessageDialog(self, message = "账户或密码错误！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()                                                             #提示错误
				warn.Destroy()

class R_or_B(wx.Frame):
	def __init__(self, parent, title):
		'''初始化系统总体布局，包括各种控件'''

		self.parent = parent#保存其父界面
		#生成一个宽为400，高为400的frame框
		wx.Frame.__init__(self, parent, title=title, size=(400, 400))  

		#定一个网格布局,两行一列
		self.main_layout = wx.BoxSizer(wx.VERTICAL)
		
		#添加一组按钮，实现身份的选择,用一个panel来管理该组按钮的布局
		self.panel = wx.Panel(self, pos = (0, 0), size = (400, 400))

		#定义book和reader的按钮
		book_button = wx.Button(self.panel, label = "图书管理", pos = (100, 50), size = (200, 100))
		reader_button = wx.Button(self.panel, label = "读者管理", pos = (100, 200), size = (200, 100))
		self.Bind(wx.EVT_BUTTON, self.do_book, book_button)
		self.Bind(wx.EVT_BUTTON, self.do_reader, reader_button)

		#将列表和panel添加到主面板
		self.main_layout.Add(self.panel, 1)

		self.SetSizer(self.main_layout)

	def do_reader(self, evt):
		reader_f = ReaderFrame(self, "读者管理")
		reader_f.Show(True)

	def do_book(self, evt):
		book_f = LibraryFrame(self, "图书管理")
		book_f.Show(True)


class LibraryFrame1(wx.Frame):
	def __init__(self, parent, title):
		'''初始化系统总体布局，包括各种控件'''

		#生成一个宽为400，高为400的frame框
		wx.Frame.__init__(self, parent, title=title, size=(400, 400))  

		#定一个网格布局,两行一列
		self.main_layout = wx.BoxSizer(wx.VERTICAL)

		#添加一组按钮，实现身份的选择,用一个panel来管理该组按钮的布局
		self.panel = wx.Panel(self, pos = (0, 0), size = (400, 400))

		#定义admin和reader的按钮
		admin_button = wx.Button(self.panel, label = "管理员", pos = (100, 50), size = (200, 100))
		reader_button = wx.Button(self.panel, label = "读者", pos = (100, 200), size = (200, 100))
		self.Bind(wx.EVT_BUTTON, self.admin, admin_button)
		self.Bind(wx.EVT_BUTTON, self.reader, reader_button)

		#将列表和panel添加到主面板
		self.main_layout.Add(self.panel, 1)

		self.SetSizer(self.main_layout)

	def admin(self, evt):
		'''管理员登录界面'''
		admin_f = logFrame_A(self, "管理员登录")
		admin_f.Show(True)

	def reader(self, evt):
		'''读者登录'''
		reader_f = logFrame_R(self, "读者登录")
		reader_f.Show(True)

AppBaseClass = wx.App


class LibraryApp(AppBaseClass):
	def OnInit(self):
		frame = LibraryFrame1(None, "library-system")
		if DBHelper().time_update(now_time) == 1:#时间更新了，每个读者的欠款都要更新
			DBHelper().money(date.today())
			DBHelper().autocancel()
		frame.Show()
		return True

#类似于c中的main函数，但被其他模块导入时，__name__值不是"__main__"
if __name__ == "__main__":	
	app = LibraryApp()
	app.MainLoop()

 