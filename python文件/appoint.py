import wx
from dbhelper import *
class libraryframe(wx.Frame):
	def __init__(self, parent, title, reader_ID):
		'''初始化系统总体布局，包括各种控件'''
		global reader_id
		reader_id = reader_ID
		#生成一个宽为400，高为400的frame框
		wx.Frame.__init__(self, parent, title=title, size=(400, 400))  

		#定一个网格布局,两行一列
		self.main_layout = wx.BoxSizer(wx.VERTICAL)


		#生成一个列表
		self.list = wx.ListCtrl(self, -1, size = (400,300), style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES) #| wx.LC_SINGLE_SEL
		#列表有散列，分别是书本ID,书名，添加日期
		self.list.InsertColumn(0, "ID")
		self.list.InsertColumn(1, "书名")

		self.list.SetColumnWidth(0, 60)                                         #设置每一列的宽度
		self.list.SetColumnWidth(1, 230)

		self.panel = wx.Panel(self, pos = (0, 300), size = (400, 100))

		#定义一组按钮
		app_button = wx.Button(self.panel, label = "预约", pos = (10, 15), size = (60, 30))    #, size = (75, 30)
		self.Bind(wx.EVT_BUTTON, self.addBook, app_button)

		self.main_layout.Add(self.list, 2)
		self.main_layout.Add(self.panel, 1)

		self.SetSizer(self.main_layout)

		#添加数据库操作对象
		self.dbhelper = DBHelper()
		datas = self.dbhelper.getAllBook()

		for data in datas:
			index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
			self.list.SetItem(index, 1, data[1])

	def appBook(self, evt):
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = "未选中任何书籍！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		self.bookid = str(selectId + 1)#书号
		self.dbhelper = DBHelper()
		rend, appoint = self.dbhelper.getBookRend(self.bookid)
		print(rend, appoint)
		if rend == '1' :
			warn = wx.MessageDialog(self, message = "书籍可直接借出，无需预约。", caption = "无需预约", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		elif appoint == '0':
			warn = wx.MessageDialog(self, message = "书籍已被预约。", caption = "已被预约", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
		else:
			self.dbhelper.MakeBookRend(reader_id, self.bookid)
			warn = wx.MessageDialog(self, message = "预约成功。", caption = "预约成功", style = wx.OK)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
