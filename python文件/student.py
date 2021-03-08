import wx
from book import *
from dbhelper_s import *
from borrowhelper import *
from reader import *
class ShowFrame(wx.Frame):
	'''用来显示书籍的信息'''

	def __init__(self, parent, title, select_id):
		'''初始化该小窗口的布局'''

		#便于调用父窗口
		self.mainframe = parent

		#生成一个300*300的框
		wx.Frame.__init__(self, parent, title = title, size = (400, 250))

		self.panel = wx.Panel(self, pos = (0, 0), size = (400, 250))
		self.panel.SetBackgroundColour("#FFFFFF")                              #背景为白色

		#三个编辑框，分别用来编辑书名，作者，书籍相关信息
		bookName_tip = wx.StaticText(self.panel, label = "书名:", pos = (5, 8), size = (60, 25))
		bookName_tip.SetBackgroundColour("#FFFFFF")
		bookName_text = wx.TextCtrl(self.panel, pos = (70, 5), size = (300, 25))
		bookName_text.SetEditable(False)
		self.name = bookName_text

		author_tip = wx.StaticText(self.panel, label = "作者:", pos = (5, 38), size = (60, 25))
		author_tip.SetBackgroundColour("#FFFFFF")
		author_text = wx.TextCtrl(self.panel, pos = (70, 35), size = (300, 25))
		author_text.SetEditable(False)
		self.author = author_text

		publisher_tip = wx.StaticText(self.panel, label = "出版社:", pos = (5, 68), size = (60, 25))
		publisher_tip.SetBackgroundColour("#FFFFFF")
		publisher_text = wx.TextCtrl(self.panel, pos = (70, 65), size = (300, 30))
		publisher_text.SetEditable(False)
		self.publisher = publisher_text

		count_tip = wx.StaticText(self.panel, label = "借阅状态:", pos = (5, 103), size = (60, 25))
		count_tip.SetBackgroundColour("#FFFFFF")
		count_text = wx.TextCtrl(self.panel, pos = (70, 100), size = (300, 25))
		count_text.SetEditable(False)
		self.count = count_text

		status_b_tip = wx.StaticText(self.panel, label = "预约状态:", pos = (5, 133), size = (60, 25))
		status_b_tip.SetBackgroundColour("#FFFFFF")
		status_b_text = wx.TextCtrl(self.panel, pos = (70, 130), size = (300, 25))
		status_b_text.SetEditable(False)
		self.status_b = status_b_text

		#选中的id和bookid
		self.select_id = select_id
		self.bookid = self.mainframe.list.GetItem(select_id, 0).Text             #获取第select_id行的第0列的值

		#需要用到的数据库接口
		self.dbhelper = DBHelper()
		self.showAllText()                     #展现所有的text原来取值

	def showAllText(self):
		'''显示概述本原始信息'''
		data = self.dbhelper.getBookById(self.bookid)                      #通过id获取书本信息

		self.name.SetValue(data[1])                                        #设置值
		self.publisher.SetValue(data[3])
		self.author.SetValue(data[2])
		self.count.SetValue(str(data[4]))
		self.status_b.SetValue(str(data[5]))

class searchFrame(wx.Frame):
	'''查找书籍弹出的小窗口'''

	def __init__(self, parent, title):
		'''初始化该小窗口的布局'''

		self.mainframe = parent.mainframe
		self.studentid = parent.studentid
		self.main_layout = wx.BoxSizer(wx.VERTICAL)

		wx.Frame.__init__(self, parent, title=title, size = (400, 300))

		self.panel_1 = wx.Panel(self, pos = (0, 0), size = (400, 40))
		self.panel_1.SetBackgroundColour("#FFFFFF")
		self.panel_2 = wx.Panel(self, pos = (0, 180), size = (400, 100))
		self.panel_2.SetBackgroundColour("#FFFFFF")

		bookName = wx.StaticText(self.panel_1, label='书名：', pos=(5,8),size=(40, 25))
		bookName.SetBackgroundColour("#FFFFFF")
		bookName_text = wx.TextCtrl(self.panel_1, pos = (45,5), size = (250, 25))
		self.name = bookName_text

		self.list = wx.ListCtrl(self, -1,pos = (5,45), size = (375,160), style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)
		self.list.InsertColumn(0, "ID")
		self.list.InsertColumn(1, "书名")
		self.list.InsertColumn(2, "借阅状态")
		self.list.InsertColumn(3, "预约状态")

		self.list.SetColumnWidth(0, 50)                                         
		self.list.SetColumnWidth(1, 165)
		self.list.SetColumnWidth(2, 80)
		self.list.SetColumnWidth(3, 80)

	
		search_button = wx.Button(self.panel_1, label = '搜索书籍', pos = (300, 5))
		detail_button = wx.Button(self.panel_2, label = '详细', pos = (10,10))
		borrow_button = wx.Button(self.panel_2, label = '借阅', pos = (100,10))
		self.Bind(wx.EVT_BUTTON, self.searchBook, search_button)
		self.Bind(wx.EVT_BUTTON, self.showDetail, detail_button)
		self.Bind(wx.EVT_BUTTON, self.bbook, borrow_button)

		self.main_layout.Add(self.panel_1)
		self.main_layout.Add(self.list)
		self.main_layout.Add(self.panel_2,1)
		self.SetSizer(self.main_layout)

		self.dbhelper = DBHelper()

	def searchBook(self, evk):
		'''
		1.获取text文本
		'''
		bookName = self.name.GetValue()
		if bookName == '':
			warn = wx.MessageDialog(self, message = '书名不能为空！', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()
			warn.Destroy()
			return
		else:
			self.list.DeleteAllItems()
			self.dbhelper = DBHelper()
			datas = self.dbhelper.getBookByName(bookName)

			for data in datas:
				index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
				self.list.SetItem(index, 1, data[1])
				self.list.SetItem(index, 2, str(data[2]))
				self.list.SetItem(index, 3, str(data[3]))

	def showDetail(self, evk):
		'''详细按钮响应事件'''
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = '未选中任何条目！', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()
			warn.Destroy()
			return
		else:
			detail_f = ShowFrame(self, "详细窗口", selectId)
			detail_f.Show(True)

	def bbook(self, evk):
		'''借阅按钮响应事件'''
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = '未选中任何条目！', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()
			warn.Destroy()
			return
		else:
			bookname = self.list.GetItem(selectId, 1).Text
			bookid = self.list.GetItem(selectId, 0).Text
			dlg = wx.MessageDialog(self, message = "确定借阅" + bookname + '吗？', caption="标题信息", style = wx.YES_NO | wx.ICON_QUESTION)
			if dlg.ShowModal() == wx.ID_YES:
				self.dbhelper = DBHelper()
				returnValue = self.dbhelper.borrowbook(bookid,self.studentid)
				if(returnValue == 0):
					self.mainframe.list.DeleteAllItems()
					items = self.dbhelper.bookOwned(reader_id)
					for item in items:
						index = self.mainframe.list.InsertItem(self.mainframe.list.GetItemCount(), str(item[0]))
						self.mainframe.list.SetItem(index, 1, str(item[1]))
						self.mainframe.list.SetItem(index, 2, str(item[2]))
						self.mainframe.list.SetItem(index, 3, str(item[3]))
						self.mainframe.list.SetItem(index, 4, str(item[4]))
					info = wx.MessageDialog(self, message='成功借阅', caption='借阅', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
					info.ShowModal()
					info.Destroy()
				elif(returnValue == 1):
					warn = wx.MessageDialog(self, message = '选中书籍已借出', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
					warn.ShowModal()
					warn.Destroy()
				elif(returnValue == 2):
					warn = wx.MessageDialog(self, message = '超出最大借书限制', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
					warn.ShowModal()
					warn.Destroy()
				elif(returnValue == 3):
					warn = wx.MessageDialog(self, message = '有罚款未付清', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
					warn.ShowModal()
					warn.Destroy()
				else:
					self.mainframe.list.DeleteAllItems()
					items = self.dbhelper.bookOwned(reader_id)
					for item in items:
						index = self.mainframe.list.InsertItem(self.mainframe.list.GetItemCount(), str(item[0]))
						self.mainframe.list.SetItem(index, 1, str(item[1]))
						self.mainframe.list.SetItem(index, 2, str(item[2]))
						self.mainframe.list.SetItem(index, 3, str(item[3]))
						self.mainframe.list.SetItem(index, 4, str(item[4]))
					self.mainframe.resbook.SetValue('空')
					info = wx.MessageDialog(self, message='成功借阅', caption='借阅', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
					info.ShowModal()
					info.Destroy()
			else:
				dlg.Destroy()


	
class borrowFrame(wx.Frame):
	def __init__(self, parent, title):
		'''初始化借书表总体布局，包括各种控件'''

		self.mainframe = parent
		#生成一个宽为400，高为400的frame框
		wx.Frame.__init__(self, parent, title=title, size=(400, 400))
		
		#定一个网格布局,两行一列
		self.main_layout = wx.BoxSizer(wx.VERTICAL)

		self.studentid = parent.studentid
		#生成一个列表
		self.list = wx.ListCtrl(self, -1, size = (400,300), style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)

		#列表有散列，分别是书本ID,书名，添加日期
		self.list.InsertColumn(0, "ID")
		self.list.InsertColumn(1, "书名")
		
		#设置各列的宽度
		self.list.SetColumnWidth(0, 60)                                         
		self.list.SetColumnWidth(1, 240)
		

		#添加一组按钮，实现增删改查,用一个panel来管理该组按钮的布局
		self.panel = wx.Panel(self, pos = (0, 300), size = (400, 100))
		
		#定义一组按钮
		search_button = wx.Button(self.panel, label = "搜索", pos = (10, 15), size = (60, 30)) 
		borrow_button = wx.Button(self.panel, label = "借阅", pos = (110, 15), size = (60, 30))
		detail_button = wx.Button(self.panel, label = "详细", pos = (210, 15), size = (60, 30))
		app_button = wx.Button(self.panel, label = "预约", pos = (310, 15), size = (60, 30))
		#w为按钮绑定相应事件函数，第一个参数为默认参数，指明为按钮类事件，第二个为事件函数名，第三个为按钮名
		self.Bind(wx.EVT_BUTTON, self.searchBook, search_button)
		self.Bind(wx.EVT_BUTTON, self.borrowBook, borrow_button)
		self.Bind(wx.EVT_BUTTON, self.showDetail, detail_button)
		self.Bind(wx.EVT_BUTTON, self.appBook, app_button)
		#将列表和panel添加到主面板
		self.main_layout.Add(self.list, 2)
		self.main_layout.Add(self.panel, 1)

		self.SetSizer(self.main_layout)

		#添加数据库操作对象
		self.dbhelper = DBHelper()
		datas = self.dbhelper.getAllBook()

		for data in datas:
			index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
			self.list.SetItem(index, 1, data[1])

	def searchBook(self, evt):
		search_f = searchFrame(self, '查找书籍窗口')
		search_f.Show(True)

	def showDetail(self, evk):
		'''详细按钮响应事件'''
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = '未选中任何条目！', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()
			warn.Destroy()
			return
		else:
			detail_f = ShowFrame(self, "详细窗口", selectId)
			detail_f.Show(True)
	
	def borrowBook(self, evk):
		'''借阅按钮响应事件'''
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = '未选中任何条目！', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()
			warn.Destroy()
			return
		else:
			bookname = self.list.GetItem(selectId, 1).Text
			bookid = self.list.GetItem(selectId, 0).Text
			dlg = wx.MessageDialog(self, message = "确定借阅" + bookname + '吗？', caption="标题信息", style = wx.YES_NO | wx.ICON_QUESTION)
			if dlg.ShowModal() == wx.ID_YES:
				self.dbhelper = DBHelper()
				returnValue = self.dbhelper.borrowbook(bookid,self.studentid)
				if(returnValue == 0):
					self.mainframe.list.DeleteAllItems()
					items = self.dbhelper.bookOwned(reader_id)
					for item in items:
						index = self.mainframe.list.InsertItem(self.mainframe.list.GetItemCount(), str(item[0]))
						self.mainframe.list.SetItem(index, 1, str(item[1]))
						self.mainframe.list.SetItem(index, 2, str(item[2]))
						self.mainframe.list.SetItem(index, 3, str(item[3]))
						self.mainframe.list.SetItem(index, 4, str(item[4]))
					info = wx.MessageDialog(self, message='成功借阅', caption='借阅', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
					info.ShowModal()
					info.Destroy()
				elif(returnValue == 1):
					warn = wx.MessageDialog(self, message = '选中书籍已借出', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
					warn.ShowModal()
					warn.Destroy()
				elif(returnValue == 2):
					warn = wx.MessageDialog(self, message = '超出最大借书限制', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
					warn.ShowModal()
					warn.Destroy()
				elif (returnValue == 3):
					warn = wx.MessageDialog(self, message='有罚款未付清', caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
					warn.ShowModal()
					warn.Destroy()
				else:
					self.mainframe.list.DeleteAllItems()
					items = self.dbhelper.bookOwned(reader_id)
					for item in items:
						index = self.mainframe.list.InsertItem(self.mainframe.list.GetItemCount(), str(item[0]))
						self.mainframe.list.SetItem(index, 1, str(item[1]))
						self.mainframe.list.SetItem(index, 2, str(item[2]))
						self.mainframe.list.SetItem(index, 3, str(item[3]))
						self.mainframe.list.SetItem(index, 4, str(item[4]))
					self.mainframe.resbook.SetValue('空')
					self.mainframe.last_time.SetLabel('空')
					info = wx.MessageDialog(self, message='成功借阅', caption='借阅', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
					info.ShowModal()
					info.Destroy()
			else:
				dlg.Destroy()


	def appBook(self, evt):#预约按钮事件
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = "未选中任何书籍！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
			return
		self.bookid = self.list.GetItem(selectId, 0).Text #书号
		self.dbhelper = DBHelper()
		rend, appoint = self.dbhelper.getBookRend(self.bookid)
		status = self.dbhelper.getReservedBook(self.studentid)
		if status != "无":
			warn = wx.MessageDialog(self, message = "超过最大预约数量限制", caption = "无法预约", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()                                                             #提示错误
			warn.Destroy()
		elif (self.dbhelper.get_money(self.studentid) != 0):
			warn = wx.MessageDialog(self, message='您已欠费，请先缴费，再尝试续借。', caption="错误警告",
									style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()
			warn.Destroy()
		else:
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
				bookname = self.dbhelper.getReservedBook(self.studentid)
				self.mainframe.resbook.SetValue(bookname)
				self.mainframe.last_time.SetLabel(self.dbhelper.lasttime(reader_id))
				warn = wx.MessageDialog(self, message = "预约成功", caption = "预约成功", style = wx.OK)
				warn.ShowModal()
				warn.Destroy()
class changeFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(400, 200))

		self.panel = wx.Panel(self, pos=(0, 0), size=(400, 200))
		self.panel.SetBackgroundColour("#FFFFFF")

		password_tip = wx.StaticText(self.panel, label="密码:", pos=(5, 38), size=(40, 25))
		password_tip.SetBackgroundColour("#FFFFFF")
		password_text = wx.TextCtrl(self.panel, pos=(45, 35), size=(250, 25))
		self.password = password_text

		save_button = wx.Button(self.panel, label="保存修改", pos=(305, 35))
		self.Bind(wx.EVT_BUTTON, self.saveUpdate, save_button)

		self.dbhelper = DBHelper()
		data = self.dbhelper.getPass(reader_id)
		self.password.SetValue(data[0])

	def saveUpdate(self, evt):
		password = self.password.GetValue()
		if len(password) > 12:
			warn = wx.MessageDialog(self, message="密码不能超过12位！！！", caption="错误警告",
									style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		else:
			info = wx.MessageDialog(self, message='成功修改密码', caption='修改密码', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
			info.ShowModal()
			info.Destroy()
			self.dbhelper.update_pass(reader_id, password)

class studentFrame(wx.Frame):
	
	def __init__(self, parent, title, studentId):
		'''初始化学生表总体布局，包括各种控件'''
		global reader_id
		reader_id = studentId
		wx.Frame.__init__(self, parent, title=title, size=(480, 480))
		
		#定一个网格布局,两行一列
		self.main_layout = wx.BoxSizer(wx.VERTICAL)
		self.panel_1 = wx.Panel(self, pos = (0, 0), size = (480, 180))
		self.panel_1.SetBackgroundColour("#FFFFFF")
		self.panel_2 = wx.Panel(self, pos = (0, 400), size = (480, 100))
		self.panel_2.SetBackgroundColour("#FFFFFF")
		
		self.dbhelper = DBHelper()
		data = self.dbhelper.getStudentById(studentId)
		self.studentid = studentId
		self.stuname = data[2]
		self.insname = data[4]
		self.tele = str(data[5])
		self.money = data[8]#        欠款
		Font1 = wx.Font(14,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
		Font2 = wx.Font(14,wx.DECORATIVE,wx.NORMAL,wx.NORMAL,True)
		stu_id = wx.StaticText(self.panel_1, label = "学号: ", pos = (8, 10), size = (60, 25))
		stu_id.SetBackgroundColour("#FFFFFF")
		stu_id_text = wx.StaticText(self.panel_1, label = str(self.studentid), pos = (75, 10), size = (250, 25))
		stu_id_text.SetFont(Font2)
		stu_id.SetFont(Font1)
		
		
		stu_name = wx.StaticText(self.panel_1, label = "姓名: ", pos = (8, 40), size = (60, 20))
		stu_name.SetBackgroundColour("#FFFFFF")
		stu_name_text = wx.StaticText(self.panel_1, label = self.stuname, pos = (75, 40), size = (250, 20))
		stu_name_text.SetFont(Font2)
		stu_name.SetFont(Font1)
		
		ins_name = wx.StaticText(self.panel_1, label = "学院: ", pos = (8, 65), size = (60, 20))
		ins_name.SetBackgroundColour("#FFFFFF")
		ins_name_text = wx.StaticText(self.panel_1, label = self.insname, pos = (75, 65), size = (250, 20))
		ins_name_text.SetFont(Font2)
		ins_name.SetFont(Font1)

		tele = wx.StaticText(self.panel_1, label = "电话: ", pos = (8, 90), size = (60, 20))
		tele.SetBackgroundColour("#FFFFFF")
		tele_text = wx.StaticText(self.panel_1, label = self.tele, pos = (75, 90), size = (250, 20))
		tele_text.SetFont(Font2)
		tele.SetFont(Font1)

		money = wx.StaticText(self.panel_1, label = "欠款：", pos = (8, 115), size = (60, 20))
		money.SetBackgroundColour("#FFFFFF")
		money_text = wx.StaticText(self.panel_1, label = str(self.money), pos = (75, 115), size = (250, 20))
		money_text.SetFont(Font2)
		money.SetFont(Font1)
		self.money_show = money_text
		
		reserve_tip = wx.StaticText(self.panel_1, label = "预约图书:", pos = (8, 148), size = (60, 25))
		reserve_tip.SetBackgroundColour("#FFFFFF")
		reserve_text = wx.TextCtrl(self.panel_1, pos = (70,145), size = (180, 25))
		reserve_tip.SetBackgroundColour("#FFFFFF")
		reserve_text.SetEditable(False)

		last_time = self.dbhelper.lasttime(reader_id)
		time_tip = wx.StaticText(self.panel_1, label="最晚取书日期:", pos=(258, 148), size=(80, 25))
		time_tip.SetBackgroundColour("#FFFFFF")
		if last_time == 0:
			time_text = wx.StaticText(self.panel_1, label = "空", pos=(350, 148), size=(70, 25))
			time_tip.SetBackgroundColour("#FFFFFF")
		else:
			time_text = wx.StaticText(self.panel_1, label=self.dbhelper.lasttime(reader_id), pos=(350, 148), size=(70, 25))
			time_tip.SetBackgroundColour("#FFFFFF")

		self.last_time = time_text

		#reserve_tip.SetFont(Font1)
		#reserve_text.SetFont(Font1)
		self.resbook = reserve_text

		image = wx.Image('student.jpg', wx.BITMAP_TYPE_JPEG)
		w = image.GetWidth()
		h = image.GetHeight()
		bmp = image.Scale(w/6, h/6).ConvertToBitmap()
		wx.StaticBitmap(self, -1, bmp, pos=(300,8))


		#借书列表
		self.list = wx.ListCtrl(self, -1, pos=(0,0) ,size = (480,200), style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)

		#列表有散列
		self.list.InsertColumn(0, "ID")
		self.list.InsertColumn(1, "书名")
		self.list.InsertColumn(2, "借书日期")
		self.list.InsertColumn(3, "应还日期")
		self.list.InsertColumn(4, "续借状态")
		#设置各列的宽度
		self.list.SetColumnWidth(0, 65)
		self.list.SetColumnWidth(1, 120)
		self.list.SetColumnWidth(2, 100)
		self.list.SetColumnWidth(3, 100)
		self.list.SetColumnWidth(4, 70)
		
		#定义一组按钮
		return_button = wx.Button(self.panel_2, label = "还书", pos = (10, 15), size = (60, 30)) 
		renew_button = wx.Button(self.panel_2, label = "续借", pos = (85, 15), size = (60, 30))
		borrow_button = wx.Button(self.panel_2, label = "借阅", pos = (160, 15), size = (60, 30))
		fine_button = wx.Button(self.panel_2, label = "交罚款", pos = (235, 15), size = (60, 30))
		reserveq_button = wx.Button(self.panel_2, label = "取消预约", pos = (310, 15), size = (60, 30))
		flash_button = wx.Button(self.panel_2, label = "修改密码", pos = (385, 15), size = (60, 30))
		#w为按钮绑定相应事件函数，第一个参数为默认参数，指明为按钮类事件，第二个为事件函数名，第三个为按钮名
		self.Bind(wx.EVT_BUTTON, self.return_book, return_button)
		self.Bind(wx.EVT_BUTTON, self.borrow, borrow_button)
		self.Bind(wx.EVT_BUTTON, self.renew, renew_button)
		self.Bind(wx.EVT_BUTTON, self.fine, fine_button)
		self.Bind(wx.EVT_BUTTON, self.quit, reserveq_button)
		self.Bind(wx.EVT_BUTTON, self.flash, flash_button)
		#将列表和panel添加到主面板
		self.main_layout.Add(self.panel_1, 1)
		self.main_layout.Add(self.list, 2)
		self.main_layout.Add(self.panel_2, 1)

		self.SetSizer(self.main_layout)

		items = self.dbhelper.bookOwned(studentId)
		for item in items:
			index = self.list.InsertItem(self.list.GetItemCount(), str(item[0]))
			self.list.SetItem(index, 1, str(item[1]))
			self.list.SetItem(index, 2, str(item[2]))
			self.list.SetItem(index, 3, str(item[3]))
			self.list.SetItem(index, 4, str(item[4]))

		bookname = self.dbhelper.getReservedBook(self.studentid) 
		self.resbook.SetValue(bookname)

	def return_book(self,evt):
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message="未选中任何条目！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()  # 提示错误
			warn.Destroy()
			return
		else:
			bookid = self.list.GetItem(selectId, 0).Text  # 得到书本id
			self.list.DeleteItem(selectId)  # 先在listctrl中删除选中行
			readerid = reader_id  # 传入readerid
			# 删去借阅表中的记录
			self.dbhelper = BorrowHelper()
			self.dbhelper.delete_record(readerid, bookid)

			self.dbhelper.change_time(bookid)
			# 获得该书籍的预约状态
			data_1 = self.dbhelper.pre_bookborrow(bookid)

			# 准备好修改后的读者信息
			data_2 = self.dbhelper.pre_reader(readerid)
			borrow_num = str(data_2[0] - 1)
			able_num = str(data_2[1] + 1)

			# 如果已经被预约，不修改可借状态和预约状态，只修改读者状态   #三天后可借可预约，等待实现
			if data_1 == 0:
				self.dbhelper.update_reader(readerid, borrow_num, able_num)
			else:
				self.dbhelper.update_reader(readerid, borrow_num, able_num)
				self.dbhelper.update_book(bookid)

	def borrow(self,evt):
		b_f = borrowFrame(self, '借阅书籍窗口')
		b_f.Show(True)

	def renew(self,evt):
		selectId = self.list.GetFirstSelected()
		if selectId == -1:
			warn = wx.MessageDialog(self, message = '未选中任何条目！', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()
			warn.Destroy()
			return
		else:
			bookid = self.list.GetItem(selectId, 0).Text
			self.dbhelper = DBHelper()
			returnValue = self.dbhelper.renewBook(bookid)
			if(self.dbhelper.get_money(self.studentid) != 0):
				warn = wx.MessageDialog(self, message = '您已欠费，请先缴费，再尝试续借。', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()
				warn.Destroy()
			elif(returnValue == 1):
				warn = wx.MessageDialog(self, message = '已续借过，无法再次续借。', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()
				warn.Destroy()
			elif(returnValue == 2):
				warn = wx.MessageDialog(self, message = '书籍已被人预约，无法续借。', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
				warn.ShowModal()
				warn.Destroy()
			else:
				info = wx.MessageDialog(self, message='成功续借', caption='info', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
				info.ShowModal()
				info.Destroy()
				self.list.SetItem(selectId, 4, '1')
				self.list.SetItem(selectId, 3, returnValue)

				

	def fine(self,evt):
		# selectId = self.list.GetFirstSelected()
		self.dbhelper = DBHelper()
		self.dbhelper.payFine(self.studentid)
		self.money_show.SetLabel("0")
		self.dbhelper.change_return_time(self.studentid)
		self.list.DeleteAllItems()
		items = self.dbhelper.bookOwned(reader_id)
		for item in items:
			index = self.list.InsertItem(self.list.GetItemCount(), str(item[0]))
			self.list.SetItem(index, 1, str(item[1]))
			self.list.SetItem(index, 2, str(item[2]))
			self.list.SetItem(index, 3, str(item[3]))
			self.list.SetItem(index, 4, str(item[4]))
		info = wx.MessageDialog(self, message='罚款付清', caption='info', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
		info.ShowModal()
		info.Destroy()

	def quit(self, evt):
		self.dbhelper = DBHelper()
		returnValue = self.dbhelper.quitreserve(self.studentid)
		if returnValue == 1:
			info = wx.MessageDialog(self, message='取消预约成功', caption='info', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
			self.last_time.SetLabel('空')
			info.ShowModal()
			info.Destroy()
			self.resbook.SetValue('空')
		else:
			warn = wx.MessageDialog(self, message = '当前没有预约书籍', caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
			warn.ShowModal()
			warn.Destroy()
	def flash(self, evt):
		change_f = changeFrame(self, "修改密码")
		change_f.Show(True)

if __name__ == "__main__":	
	app = wx.App()
	studentId = '0006'

	frame = studentFrame(None, "library-system",studentId)
	frame.Show()
	app.MainLoop()