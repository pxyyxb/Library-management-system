'''实现增加书籍，删除书籍，修改书籍和查看图书详情，基于mysql数据库和wxPython'''

import wx
from book import *
from bookhelper import *

__metaclass__ = type


class AddFrame(wx.Frame):
	# 添加书籍弹出的小窗口

	def __init__(self, parent, title):

		# 初始化该小窗口的布局

		self.mainframe = parent

		wx.Frame.__init__(self, parent, title = title, size = (400, 275))

		self.panel = wx.Panel(self, pos = (0, 0), size = (400, 275))
		self.panel.SetBackgroundColour("#FFFFFF")                              # 背景为白色

		# 六个编辑框，分别用来编辑书名，作者，书籍相关信息
		bookid_tip = wx.StaticText(self.panel, label="书   号:", pos=(5, 8), size=(50, 25))
		bookid_tip.SetBackgroundColour("#FFFFFF")
		bookid_text = wx.TextCtrl(self.panel, pos=(55, 5), size=(300, 25))
		self.bookid = bookid_text

		bookName_tip = wx.StaticText(self.panel, label="书   名:", pos=(5, 38), size=(50, 25))
		bookName_tip.SetBackgroundColour("#FFFFFF")
		bookName_text = wx.TextCtrl(self.panel, pos=(55, 35), size=(300, 25))
		self.name = bookName_text

		author_tip = wx.StaticText(self.panel, label="作   者:", pos=(5, 68), size=(50, 25))
		author_tip.SetBackgroundColour("#FFFFFF")
		author_text = wx.TextCtrl(self.panel, pos=(55, 65), size=(300, 25))
		self.author = author_text

		publish_tip = wx.StaticText(self.panel, label="出版社:", pos=(5, 98), size=(50, 25))
		publish_tip.SetBackgroundColour("#FFFFFF")
		publish_text = wx.TextCtrl(self.panel, pos=(55, 95), size=(300, 25))
		self.publish = publish_text

		borrow_tip = wx.StaticText(self.panel, label="可 借\n状 态", pos=(10, 128), size=(40, 40))
		borrow_tip.SetBackgroundColour("#FFFFFF")
		borrow_text = wx.TextCtrl(self.panel, pos=(55, 130), size=(125, 25))
		self.borrow = borrow_text

		order_tip = wx.StaticText(self.panel, label="可 约\n状 态", pos=(190, 128), size=(40, 40))
		order_tip.SetBackgroundColour("#FFFFFF")
		order_text = wx.TextCtrl(self.panel, pos=(230, 130), size=(125, 25))
		self.order = order_text

		save_button = wx.Button(self.panel, label="保存书籍", pos = (155, 180))
		self.Bind(wx.EVT_BUTTON, self.saveBook, save_button)

		# 需要用到的数据库接口
		self.dbhelper = BookHelper()


	def saveBook(self, evt):
		# 第一步：获取text中文本；第二步，连接数据库；第三步插入并获得主键；第四步添加到ListCtrl中
		bookid = self.bookid.GetValue()
		bookName = self.name.GetValue()
		author = self.author.GetValue()
		publish = self.publish.GetValue()
		borrow = self.borrow.GetValue()
		order = self.order.GetValue()

		# 得到所有书籍的书号，查看是否有重复的
		list = []
		datas = self.dbhelper.getAllBook()
		for data in datas:
			list.append(data[0])

		if bookid == "" or borrow == "" or order == "":
			warn = wx.MessageDialog(self, message="书号、可借状态、可约状态不能为空！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                        # 提示错误
			warn.Destroy()
			return
		if len(bookid) != 6:
			warn = wx.MessageDialog(self, message="书号长度必须为6位！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if len(bookName) > 20:
			warn = wx.MessageDialog(self, message="输入的书名长度不能超过20位！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if len(author) > 20:
			warn = wx.MessageDialog(self, message="输入的作者长度不能超过20位！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if len(publish) > 20:
			warn = wx.MessageDialog(self, message="输入的出版社长度不能超过20位之间！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if int(borrow) != 0 and int(borrow) != 1:
			warn = wx.MessageDialog(self, message="可借状态必须为0或1！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if int(order) != 0 and int(order) != 1:
			warn = wx.MessageDialog(self, message="可约状态必须为0或1！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		for item in list:
			if bookid == item:
				warn = wx.MessageDialog(self, message="该书号已存在！！！", caption="错误警告",style=wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()  # 提示错误
				warn.Destroy()
				return
		book = Book(bookid, bookName, author, publish, borrow, order)
		self.dbhelper.insertBook(book)
		self.mainframe.addToList(bookid, book)
		info = wx.MessageDialog(self, message='成功添加书籍', caption='添加书籍', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
		info.ShowModal()
		info.Destroy()

		self.Destroy()

class UpdateFrame(wx.Frame):
	def __init__(self, parent, title, select_id):
		# 更新图书信息界面总布局

		wx.Frame(parent, title=title, size=(400, 275))

		# 用来调用父frame,便于更新
		self.mainframe = parent
		# 生成一个300*300的框
		wx.Frame.__init__(self, parent, title = title, size = (400, 275))

		self.panel = wx.Panel(self, pos = (0, 0), size = (400, 275))
		self.panel.SetBackgroundColour("#FFFFFF")                              # 背景为白色

		# 六个编辑框，分别用来编辑书名，作者，书籍相关信息
		bookid_tip = wx.StaticText(self.panel, label="书号:", pos=(5, 8), size=(50, 25))
		bookid_tip.SetBackgroundColour("#FFFFFF")
		bookid_text = wx.TextCtrl(self.panel, pos=(55, 5), size=(300, 25))
		bookid_text.SetEditable(False)
		self.bookid = bookid_text

		bookName_tip = wx.StaticText(self.panel, label="书   名:", pos=(5, 38), size=(50, 25))
		bookName_tip.SetBackgroundColour("#FFFFFF")
		bookName_text = wx.TextCtrl(self.panel, pos=(55, 35), size=(300, 25))
		self.name = bookName_text

		author_tip = wx.StaticText(self.panel, label="作   者:", pos=(5, 68), size=(50, 25))
		author_tip.SetBackgroundColour("#FFFFFF")
		author_text = wx.TextCtrl(self.panel, pos=(55, 65), size=(300, 25))
		self.author = author_text

		publish_tip = wx.StaticText(self.panel, label="出版社:", pos=(5, 98), size=(50, 25))
		publish_tip.SetBackgroundColour("#FFFFFF")
		publish_text = wx.TextCtrl(self.panel, pos=(55, 95), size=(300, 25))
		self.publish = publish_text

		borrow_tip = wx.StaticText(self.panel, label="可 借\n状 态", pos=(10, 128), size=(40, 40))
		borrow_tip.SetBackgroundColour("#FFFFFF")
		borrow_text = wx.TextCtrl(self.panel, pos=(55, 130), size=(125, 25))
		self.borrow = borrow_text

		order_tip = wx.StaticText(self.panel, label="可 约\n状 态", pos=(190, 128), size=(40, 40))
		order_tip.SetBackgroundColour("#FFFFFF")
		order_text = wx.TextCtrl(self.panel, pos=(230, 130), size=(125, 25))
		self.order = order_text

		save_button = wx.Button(self.panel, label="保存修改", pos=(155, 180))
		self.Bind(wx.EVT_BUTTON, self.saveUpdate, save_button)

		# 选中的id和bookid
		self.select_id = select_id
		self.book_id = self.mainframe.list.GetItem(select_id, 0).Text             # 获取第select_id行的第0列的值

		# 需要用到的数据库接口
		self.dbhelper = BookHelper()
		self.showAllText()                     # 展现所有的text原来取值

	def showAllText(self):
		# 显示概述本原始信息
		data = self.dbhelper.getBookById(self.book_id)  # 通过id获取书本信息

		self.bookid.SetValue(str(data[0]))  # 设置值
		self.name.SetValue(data[1])
		self.author.SetValue(data[2])
		self.publish.SetValue(data[3])
		self.borrow.SetValue(str(data[4]))
		self.order.SetValue(str(data[5]))

	def saveUpdate(self, evt):
		# 保存修改后的值
		bookid = self.bookid.GetValue()													# 获得修改后的值
		bookName = self.name.GetValue()
		author = self.author.GetValue()
		publish = self.publish.GetValue()
		borrow = self.borrow.GetValue()
		order = self.order.GetValue()

		if bookid == "" or borrow == "" or order == "":
			warn = wx.MessageDialog(self, message="书号、可借状态、可约状态不能为空！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             # 提示错误
			warn.Destroy()
			return
		if len(bookid) != 6:
			warn = wx.MessageDialog(self, message="书号长度必须为6位！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if len(bookName) > 20:
			warn = wx.MessageDialog(self, message="输入的书名长度不能超过20位！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if len(author) > 20:
			warn = wx.MessageDialog(self, message="输入的作者长度不能超过20位！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if len(publish) > 20:
			warn = wx.MessageDialog(self, message="输入的出版社长度不能超过20位！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if int(borrow) != 0 and int(borrow) != 1:
			warn = wx.MessageDialog(self, message="可借状态必须为0或1！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		if int(order) != 0 and int(order) != 1:
			warn = wx.MessageDialog(self, message="可约状态必须为0或1！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		book = Book(bookid, bookName, author, publish, borrow, order)                         # 将数据封装到book对象中
		self.dbhelper.saveUpdate(self.book_id, book)
		self.mainframe.list.SetItem(self.select_id, 0, bookid)
		self.mainframe.list.SetItem(self.select_id, 1, bookName)
		self.mainframe.list.SetItem(self.select_id, 2, author)
		self.mainframe.list.SetItem(self.select_id, 3, publish)
		self.mainframe.list.SetItem(self.select_id, 4, borrow)
		self.mainframe.list.SetItem(self.select_id, 5, order)
		info = wx.MessageDialog(self, message='成功修改书籍', caption='修改书籍', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
		info.ShowModal()
		info.Destroy()

		self.Destroy()
			# 修改完后自动销毁

class LibraryFrame(wx.Frame):
	def __init__(self, parent, title):
		# 初始化系统总体布局，包括各种控件

		# 生成一个宽为1000，高为600的frame框
		wx.Frame.__init__(self, parent, title=title, size=(870, 600))

		self.panel_1 = wx.Panel(self, pos=(0, 0), size=(870, 25))
		self.panel_1.SetBackgroundColour("#FFFFFF")

		# 书号文本框
		bookid_tip = wx.StaticText(self.panel_1, label="书   号:", pos=(20, 15), size=(50, 25))
		bookid_tip.SetBackgroundColour("#FFFFFF")
		bookid_text = wx.TextCtrl(self.panel_1, pos=(75, 12), size=(200, 25))
		self.bookid_search = bookid_text

		# 书名文本框
		bookName_tip = wx.StaticText(self.panel_1, label="书   名:", pos=(295, 15), size=(50, 25))
		bookName_tip.SetBackgroundColour("#FFFFFF")
		bookName_text = wx.TextCtrl(self.panel_1, pos=(355, 12), size=(350, 25))
		self.bookName_search = bookName_text

		search_button = wx.Button(self.panel_1, label="搜   索   书   籍", pos=(725, 12))
		self.Bind(wx.EVT_BUTTON, self.searchBook, search_button)

		# 定一个网格
		self.main_layout = wx.BoxSizer(wx.VERTICAL)

		# 生成一个列表
		self.list = wx.ListCtrl(self, -1, pos=(0, 0), size=(870, 450), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
		# 列表有散列，分别是书本ID,书名，添加日期
		self.list.InsertColumn(0, "  书          号", wx.LIST_FORMAT_CENTER)
		self.list.InsertColumn(1, "书          名", wx.LIST_FORMAT_CENTER)
		self.list.InsertColumn(2, "作            者", wx.LIST_FORMAT_CENTER)
		self.list.InsertColumn(3, "出     版     社", wx.LIST_FORMAT_CENTER)
		self.list.InsertColumn(4, "可 借 状 态", wx.LIST_FORMAT_CENTER)
		self.list.InsertColumn(5, "可 约 状 态", wx.LIST_FORMAT_CENTER)
		# 设置各列的宽度
		self.list.SetColumnWidth(0, 100)                                         # 设置每一列的宽度
		self.list.SetColumnWidth(1, 200)
		self.list.SetColumnWidth(2, 200)
		self.list.SetColumnWidth(3, 200)
		self.list.SetColumnWidth(4, 75)
		self.list.SetColumnWidth(5, 75)

		self.panel_2 = wx.Panel(self, pos=(0, 0), size=(870, 50))

		# 定义一组按钮
		add_button = wx.Button(self.panel_2, label="添加", pos=(100, 10), size=(150, 35))
		del_button = wx.Button(self.panel_2, label="删除", pos=(350, 10), size=(150, 35))
		update_button = wx.Button(self.panel_2, label="修改", pos=(600, 10), size=(150, 35))

		# w为按钮绑定相应事件函数，第一个参数为默认参数，指明为按钮类事件，第二个为事件函数名，第三个为按钮名
		self.Bind(wx.EVT_BUTTON, self.addBook, add_button)
		self.Bind(wx.EVT_BUTTON, self.delBook, del_button)
		self.Bind(wx.EVT_BUTTON, self.updateBook, update_button)

		# 将列表和panel添加到主面板
		self.main_layout.Add(self.panel_1, 1)
		self.main_layout.Add(self.list, 6)
		self.main_layout.Add(self.panel_2, 1)

		self.SetSizer(self.main_layout)

		# 添加数据库操作对象
		self.dbhelper = BookHelper()
		datas = self.dbhelper.getAllBook()
		
		for data in datas:
			index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
			self.list.SetItem(index, 1, str(data[1]))
			self.list.SetItem(index, 2, str(data[2]))
			self.list.SetItem(index, 3, str(data[3]))
			self.list.SetItem(index, 4, str(data[4]))
			self.list.SetItem(index, 5, str(data[5]))


	def addBook(self, evt):
		# 添加书籍按钮，弹出添加书籍框
		add_f = AddFrame(self, "添加书籍窗口")
		add_f.Show(True)


	def delBook(self, evt):
		# 删除书籍按钮，先选中,然后删除
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = "未选中任何条目！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		else:
			bookid = self.list.GetItem(selectId, 0).Text  # 得到书本id
			bookName = self.list.GetItem(selectId, 1).Text
			dlg = wx.MessageDialog(self, message="确定删除书号  " + bookid + ':  ' + bookName + '吗？', caption="For Sure ",style=wx.YES_NO | wx.ICON_QUESTION)
			if dlg.ShowModal() == wx.ID_YES:
				self.list.DeleteItem(selectId)                                               # 先在listctrl中删除选中行
				self.dbhelper.deleteBook(bookid)
				info = wx.MessageDialog(self, message='成功删除该书籍', caption='删除书籍', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
				info.ShowModal()
				info.Destroy()
			else:
				dlg.Destroy()

	def updateBook(self, evt):
		# 修改按钮响应事件，点击修改按钮，弹出修改框
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = "未选中任何条目！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		else:
			update_f = UpdateFrame(self, "修改书籍窗口", selectId)
			update_f.Show(True)

	def searchBook(self, evt):
		# 获取text中文本
		bookid = self.bookid_search.GetValue()
		bookName = self.bookName_search.GetValue()
		self.dbhelper = BookHelper()

		if bookid == "" and bookName == "":
			self.showAllBook()
		if bookid != "" and bookName == "":
			self.search_id(bookid)
		if bookid == "" and bookName != "":
			self.search_name(bookName)
		if bookid != "" and bookName != "":
			self.search_both(bookid, bookName)

	def search_id(self, bookid):
		# 显示概述本原始信息
		self.list.DeleteAllItems()
		data = self.dbhelper.getBookById(bookid)  # 通过id获取书本信息
		if data is None:
			warn = wx.MessageDialog(self, message="该书不存在！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		else:
			index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
			self.list.SetItem(index, 1, str(data[1]))
			self.list.SetItem(index, 2, str(data[2]))
			self.list.SetItem(index, 3, str(data[3]))
			self.list.SetItem(index, 4, str(data[4]))
			self.list.SetItem(index, 5, str(data[5]))

	def search_name(self, bookName):
		# 显示概述本原始信息
		self.list.DeleteAllItems()
		datas = self.dbhelper.getBookByName(bookName)  # 通过id获取书本信息
		if datas is None:
			warn = wx.MessageDialog(self, message="该书不存在！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		else:
			for data in datas:
				index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
				self.list.SetItem(index, 1, str(data[1]))
				self.list.SetItem(index, 2, str(data[2]))
				self.list.SetItem(index, 3, str(data[3]))
				self.list.SetItem(index, 4, str(data[4]))
				self.list.SetItem(index, 5, str(data[5]))

	def search_both(self, bookid, bookName):
		# 显示概述本原始信息
		self.list.DeleteAllItems()
		data = self.dbhelper.getBookByBoth(bookid, bookName)  # 通过id获取书本信息
		if data is None:
			warn = wx.MessageDialog(self, message="该书不存在！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		else:
			index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
			self.list.SetItem(index, 1, str(data[1]))
			self.list.SetItem(index, 2, str(data[2]))
			self.list.SetItem(index, 3, str(data[3]))
			self.list.SetItem(index, 4, str(data[4]))
			self.list.SetItem(index, 5, str(data[5]))

	def addToList(self, id, book):
		index = self.list.InsertItem(self.list.GetItemCount(), id)
		self.list.SetItem(index, 1, book.getBookName())
		self.list.SetItem(index, 2, book.getAuthor())
		self.list.SetItem(index, 3, book.getPublish())
		self.list.SetItem(index, 4, book.getBorrow())
		self.list.SetItem(index, 5, book.getOrder())

	def showAllBook(self):
		self.list.DeleteAllItems()
		# 添加数据库操作对象
		self.dbhelper = BookHelper()
		datas = self.dbhelper.getAllBook()

		for data in datas:
			index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
			self.list.SetItem(index, 1, str(data[1]))
			self.list.SetItem(index, 2, str(data[2]))
			self.list.SetItem(index, 3, str(data[3]))
			self.list.SetItem(index, 4, str(data[4]))
			self.list.SetItem(index, 5, str(data[5]))



 
