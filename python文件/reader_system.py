'''实现增加读者，删除读者，修改读者和搜索读者，基于mysql数据库和wxPython'''

import wx
from reader import *
from readerhelper import *
from bookhelper import *
__metaclass__ = type


class AddFrame(wx.Frame):
    # 添加读者弹出的小窗口

    def __init__(self, parent, title):

        # 初始化该小窗口的布局

        self.mainframe = parent

        wx.Frame.__init__(self, parent, title=title, size=(400, 325))

        self.panel = wx.Panel(self, pos=(0, 0), size=(400, 325))
        self.panel.SetBackgroundColour("#FFFFFF")  # 背景为白色

        # 六个编辑框，分别用来编辑书名，作者，书籍相关信息
        readerid_tip = wx.StaticText(self.panel, label="学     号:", pos=(5, 8), size=(75, 25))
        readerid_tip.SetBackgroundColour("#FFFFFF")
        readerid_text = wx.TextCtrl(self.panel, pos=(80, 5), size=(275, 25))
        self.readerid = readerid_text

        password_tip = wx.StaticText(self.panel, label="密     码:", pos=(5, 38), size=(75, 25))
        password_tip.SetBackgroundColour("#FFFFFF")
        password_text = wx.TextCtrl(self.panel, pos=(80, 35), size=(275, 25))
        self.password = password_text

        readerName_tip = wx.StaticText(self.panel, label="姓     名:", pos=(5, 68), size=(75, 25))
        readerName_tip.SetBackgroundColour("#FFFFFF")
        readerName_text = wx.TextCtrl(self.panel, pos=(80, 65), size=(275, 25))
        self.readerName = readerName_text

        sex_tip = wx.StaticText(self.panel, label="性     别:", pos=(5, 98), size=(75, 25))
        sex_tip.SetBackgroundColour("#FFFFFF")
        sex_text = wx.TextCtrl(self.panel, pos=(80, 95), size=(275, 25))
        self.sex = sex_text

        dept_tip = wx.StaticText(self.panel, label="学     院:", pos=(5, 128), size=(75, 25))
        dept_tip.SetBackgroundColour("#FFFFFF")
        dept_text = wx.TextCtrl(self.panel, pos=(80, 125), size=(275, 25))
        self.dept = dept_text

        tele_tip = wx.StaticText(self.panel, label="电     话:", pos=(5, 158), size=(75, 25))
        tele_tip.SetBackgroundColour("#FFFFFF")
        tele_text = wx.TextCtrl(self.panel, pos=(80, 155), size=(275, 25))
        self.tele = tele_text

        borrow_num_tip = wx.StaticText(self.panel, label="已借图书数:", pos=(5, 188), size=(75, 25))
        borrow_num_tip.SetBackgroundColour("#FFFFFF")
        borrow_num_text = wx.TextCtrl(self.panel, pos=(80, 185), size=(275, 25))
        self.borrow_num = borrow_num_text

        money_tip = wx.StaticText(self.panel, label="罚    款:", pos=(5, 218), size=(75, 25))
        money_tip.SetBackgroundColour("#FFFFFF")
        money_text = wx.TextCtrl(self.panel, pos=(80, 215), size=(275, 25))
        self.money = money_text

        save_button = wx.Button(self.panel, label="保存读者", pos=(155, 250))
        self.Bind(wx.EVT_BUTTON, self.saveReader, save_button)

        # 需要用到的数据库接口
        self.dbhelper = ReaderHelper()

    def saveReader(self, evt):
        # 第一步：获取text中文本；第二步，连接数据库；第三步插入并获得主键；第四步添加到ListCtrl中
        readerid = self.readerid.GetValue()
        password = self.password.GetValue()
        readerName = self.readerName.GetValue()
        sex = self.sex.GetValue()
        dept = self.dept.GetValue()
        tele = self.tele.GetValue()
        borrow_num = self.borrow_num.GetValue()
        able_num = str(3 - int(borrow_num))
        money = self.money.GetValue()

        # 得到所有书籍的书号，查看是否有重复的
        list = []
        datas = self.dbhelper.getAllReader()
        for data in datas:
            list.append(data[0])

        if readerid == "" or password == "" or readerName == "" or borrow_num == "":
            warn = wx.MessageDialog(self, message="学号、密码、读者姓名、已借图书数不能为空！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if len(readerid) != 4:
            warn = wx.MessageDialog(self, message="学号必须是四位！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if len(password) > 12:
            warn = wx.MessageDialog(self, message="密码不能超过12位！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if len(readerName) > 8:
            warn = wx.MessageDialog(self, message="输入姓名不能超过8位！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if sex != '男' and sex != '女' and sex != "":
            warn = wx.MessageDialog(self, message="性别输入有问题！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if len(dept) > 20:
            warn = wx.MessageDialog(self, message="输入学院不能超过20位！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if len(tele) != 11 and tele != "":
            warn = wx.MessageDialog(self, message="电话输入有问题！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if 0 > int(borrow_num) > 3:
            warn = wx.MessageDialog(self, message="已借图书数范围在0~3", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return

        if money == "":
            money = str(0)
        if float(money) < 0:
            warn = wx.MessageDialog(self, message="罚款数值必须大于等于0！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return

        for item in list:
            if readerid == item:
                warn = wx.MessageDialog(self, message="该学号已存在！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
                return

        reader = Reader(readerid, password, readerName, sex, dept, tele, borrow_num, able_num, money)
        self.dbhelper.insertReader(reader)
        self.mainframe.addToList(readerid, reader)

        self.Destroy()


class UpdateFrame(wx.Frame):
    def __init__(self, parent, title, select_id):
        # 更新图书信息界面总布局

        wx.Frame(parent, title=title, size=(400, 325))

        # 用来调用父frame,便于更新
        self.mainframe = parent
        # 生成一个300*300的框
        wx.Frame.__init__(self, parent, title=title, size=(400, 325))

        self.panel = wx.Panel(self, pos=(0, 0), size=(400, 325))
        self.panel.SetBackgroundColour("#FFFFFF")  # 背景为白色

        readerid_tip = wx.StaticText(self.panel, label="学     号:", pos=(5, 8), size=(75, 25))
        readerid_tip.SetBackgroundColour("#FFFFFF")
        readerid_text = wx.TextCtrl(self.panel, pos=(80, 5), size=(275, 25))
        readerid_text.SetEditable(False)
        self.readerid = readerid_text
        '''
        password_tip = wx.StaticText(self.panel, label="密     码:", pos=(5, 38), size=(75, 25))
        password_tip.SetBackgroundColour("#FFFFFF")
        password_text = wx.TextCtrl(self.panel, pos=(80, 35), size=(275, 25))
        password_text.SetEditable(False)
        self.password = password_text
        '''
        readerName_tip = wx.StaticText(self.panel, label="姓     名:", pos=(5, 38), size=(75, 25))
        readerName_tip.SetBackgroundColour("#FFFFFF")
        readerName_text = wx.TextCtrl(self.panel, pos=(80, 35), size=(275, 25))
        self.readerName = readerName_text

        sex_tip = wx.StaticText(self.panel, label="性     别:", pos=(5, 68), size=(75, 25))
        sex_tip.SetBackgroundColour("#FFFFFF")
        sex_text = wx.TextCtrl(self.panel, pos=(80, 65), size=(275, 25))
        self.sex = sex_text

        dept_tip = wx.StaticText(self.panel, label="学     院:", pos=(5, 98), size=(75, 25))
        dept_tip.SetBackgroundColour("#FFFFFF")
        dept_text = wx.TextCtrl(self.panel, pos=(80, 95), size=(275, 25))
        self.dept = dept_text

        tele_tip = wx.StaticText(self.panel, label="电     话:", pos=(5, 128), size=(75, 25))
        tele_tip.SetBackgroundColour("#FFFFFF")
        tele_text = wx.TextCtrl(self.panel, pos=(80, 125), size=(275, 25))
        self.tele = tele_text

        borrow_num_tip = wx.StaticText(self.panel, label="已借图书数:", pos=(5, 158), size=(75, 25))
        borrow_num_tip.SetBackgroundColour("#FFFFFF")
        borrow_num_text = wx.TextCtrl(self.panel, pos=(80, 155), size=(275, 25))
        borrow_num_text.SetEditable(False)
        self.borrow_num = borrow_num_text

        money_tip = wx.StaticText(self.panel, label="罚    款:", pos=(5, 188), size=(75, 25))
        money_tip.SetBackgroundColour("#FFFFFF")
        money_text = wx.TextCtrl(self.panel, pos=(80, 185), size=(275, 25))
        self.money = money_text

        save_button = wx.Button(self.panel, label="保存读者", pos=(155, 230))
        self.Bind(wx.EVT_BUTTON, self.saveUpdate, save_button)

        # 选中的id和bookid
        self.select_id = select_id
        self.reader_id = self.mainframe.list.GetItem(select_id, 0).Text  # 获取第select_id行的第0列的值

        # 需要用到的数据库接口
        self.dbhelper = ReaderHelper()
        self.showAllText()  # 展现所有的text原来取值

    def showAllText(self):
        # 显示概述本原始信息
        data = self.dbhelper.getReaderById(self.reader_id)  # 通过id获取书本信息
        self.readerid.SetValue(str(data[0]))  # 设置值
        self.readerName.SetValue(data[2])
        self.sex.SetValue(data[3])
        self.dept.SetValue(data[4])
        self.tele.SetValue(data[5])
        self.borrow_num.SetValue(str(data[6]))
        self.money.SetValue(str(data[8]))

    def saveUpdate(self, evt):
        # 保存修改后的值
        readerid = self.readerid.GetValue()  # 获得修改后的值
        readerName = self.readerName.GetValue()
        sex = self.sex.GetValue()
        dept = self.dept.GetValue()
        tele = self.tele.GetValue()
        borrow_num = self.borrow_num.GetValue()
        able_num = str(3 - int(borrow_num))
        money = self.money.GetValue()

        # 得到所有书籍的书号，查看是否有重复的
        list = []
        datas = self.dbhelper.getAllReader()
        for data in datas:
            list.append(data[0])

        if readerid == "" or readerName == "" or borrow_num == "":
            warn = wx.MessageDialog(self, message="学号、密码、读者姓名、已借图书数不能为空！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if len(readerid) != 4:
            warn = wx.MessageDialog(self, message="学号必须是四位！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if len(readerName) > 8:
            warn = wx.MessageDialog(self, message="输入姓名不能超过8位！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if sex != '男' and sex != '女' and sex != "":
            warn = wx.MessageDialog(self, message="性别输入有问题！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if len(dept) > 20:
            warn = wx.MessageDialog(self, message="输入学院不能超过20位！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if len(tele) != 11 and tele != "":
            warn = wx.MessageDialog(self, message="电话输入有问题！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        if 0 > int(borrow_num) > 3:
            warn = wx.MessageDialog(self, message="已借图书数范围在0~3", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return

        if money == "":
            money = str(0)
        elif float(money) < 0:
            warn = wx.MessageDialog(self, message="罚款数值必须大于等于0！！！", caption="错误警告",
                                    style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return


        reader = Reader(readerid, "", readerName, sex, dept, tele, borrow_num, able_num, money)
        self.dbhelper.saveUpdate_read(self.reader_id, reader)
        self.mainframe.list.SetItem(self.select_id, 0, readerid)
        self.mainframe.list.SetItem(self.select_id, 1, readerName)
        self.mainframe.list.SetItem(self.select_id, 2, borrow_num)
        self.mainframe.list.SetItem(self.select_id, 3, able_num)
        self.mainframe.list.SetItem(self.select_id, 4, money)

        self.Destroy()
        # 修改完后自动销毁


class ShowFrame(wx.Frame):
    # 添加读者弹出的小窗口

    def __init__(self, parent, title, select_id):
        # 初始化该小窗口的布局

        self.mainframe = parent

        wx.Frame.__init__(self, parent, title=title, size=(400, 325))

        self.panel = wx.Panel(self, pos=(0, 0), size=(400, 325))
        self.panel.SetBackgroundColour("#FFFFFF")  # 背景为白色

        # 六个编辑框，分别用来编辑书名，作者，书籍相关信息
        readerid_tip = wx.StaticText(self.panel, label="学     号:", pos=(5, 8), size=(75, 25))
        readerid_tip.SetBackgroundColour("#FFFFFF")
        readerid_text = wx.TextCtrl(self.panel, pos=(80, 5), size=(275, 25))
        readerid_text.SetEditable(False)
        self.readerid = readerid_text

        readerName_tip = wx.StaticText(self.panel, label="姓     名:", pos=(5, 38), size=(75, 25))
        readerName_tip.SetBackgroundColour("#FFFFFF")
        readerName_text = wx.TextCtrl(self.panel, pos=(80, 35), size=(275, 25))
        readerName_text.SetEditable(False)
        self.readerName = readerName_text

        sex_tip = wx.StaticText(self.panel, label="性     别:", pos=(5, 68), size=(75, 25))
        sex_tip.SetBackgroundColour("#FFFFFF")
        sex_text = wx.TextCtrl(self.panel, pos=(80, 65), size=(275, 25))
        sex_text.SetEditable(False)
        self.sex = sex_text

        dept_tip = wx.StaticText(self.panel, label="学     院:", pos=(5, 98), size=(75, 25))
        dept_tip.SetBackgroundColour("#FFFFFF")
        dept_text = wx.TextCtrl(self.panel, pos=(80, 95), size=(275, 25))
        dept_text.SetEditable(False)
        self.dept = dept_text

        tele_tip = wx.StaticText(self.panel, label="电     话:", pos=(5, 128), size=(75, 25))
        tele_tip.SetBackgroundColour("#FFFFFF")
        tele_text = wx.TextCtrl(self.panel, pos=(80, 125), size=(275, 25))
        tele_text.SetEditable(False)
        self.tele = tele_text

        borrow_num_tip = wx.StaticText(self.panel, label="已借图书数:", pos=(5, 158), size=(75, 25))
        borrow_num_tip.SetBackgroundColour("#FFFFFF")
        borrow_num_text = wx.TextCtrl(self.panel, pos=(80, 155), size=(275, 25))
        borrow_num_text.SetEditable(False)
        self.borrow_num = borrow_num_text

        able_num_tip = wx.StaticText(self.panel, label="可借图书数:", pos=(5, 188), size=(75, 25))
        able_num_tip.SetBackgroundColour("#FFFFFF")
        able_num_text = wx.TextCtrl(self.panel, pos=(80, 185), size=(275, 25))
        able_num_text.SetEditable(False)
        self.able_num = able_num_text

        money_tip = wx.StaticText(self.panel, label="罚    款:", pos=(5, 218), size=(75, 25))
        money_tip.SetBackgroundColour("#FFFFFF")
        money_text = wx.TextCtrl(self.panel, pos=(80, 215), size=(275, 25))
        money_text.SetEditable(False)
        self.money = money_text

        # 选中的id和bookid
        self.select_id = select_id
        self.reader_id = self.mainframe.list.GetItem(select_id, 0).Text  # 获取第select_id行的第0列的值

        # 需要用到的数据库接口
        self.dbhelper = ReaderHelper()
        self.showAllText()  # 展现所有的text原来取值

    def showAllText(self):
        # 显示概述本原始信息
        data = self.dbhelper.getReaderById(self.reader_id)  # 通过id获取书本信息

        self.readerid.SetValue(str(data[0]))  # 设置值
        self.readerName.SetValue(data[2])
        self.sex.SetValue(data[3])
        self.dept.SetValue(data[4])
        self.tele.SetValue(data[5])
        self.borrow_num.SetValue(str(data[6]))
        self.able_num.SetValue(str(data[7]))
        self.money.SetValue(str(data[8]))


class ReaderFrame(wx.Frame):
    def __init__(self, parent, title):
        # 初始化系统总体布局，包括各种控件
        self.mainframe = parent

        # 生成一个宽为1000，高为600的frame框
        wx.Frame.__init__(self, parent, title=title, size=(470, 600))

        self.panel_1 = wx.Panel(self, pos=(0, 0), size=(470, 25))
        self.panel_1.SetBackgroundColour("#FFFFFF")

        # 书号文本框
        readerid_tip = wx.StaticText(self.panel_1, label="学   号:", pos=(5, 10), size=(40, 20))
        readerid_tip.SetBackgroundColour("#FFFFFF")
        readerid_text = wx.TextCtrl(self.panel_1, pos=(55, 8), size=(100, 25))
        self.readerid_search = readerid_text

        # 书名文本框
        readerName_tip = wx.StaticText(self.panel_1, label="姓   名:", pos=(165, 10), size=(50, 25))
        readerName_tip.SetBackgroundColour("#FFFFFF")
        readerName_text = wx.TextCtrl(self.panel_1, pos=(220, 8), size=(125, 25))
        self.readerName_search = readerName_text

        search_button = wx.Button(self.panel_1, label="搜 索 读 者", pos=(355, 8))
        self.Bind(wx.EVT_BUTTON, self.searchReader, search_button)

        # 定一个网格
        self.main_layout = wx.BoxSizer(wx.VERTICAL)

        # 生成一个列表
        self.list = wx.ListCtrl(self, -1, pos=(0, 0), size=(470, 470), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        # 列表有散列，分别是书本ID,书名，添加日期
        self.list.InsertColumn(0, "   学        号", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(1, "姓       名", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(2, "已借图书数", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(3, "可借图书数", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(4, "罚      款", wx.LIST_FORMAT_CENTER)
        # 设置各列的宽度
        self.list.SetColumnWidth(0, 100)  # 设置每一列的宽度
        self.list.SetColumnWidth(1, 100)
        self.list.SetColumnWidth(2, 75)
        self.list.SetColumnWidth(3, 75)
        self.list.SetColumnWidth(4, 100)

        self.panel_2 = wx.Panel(self, pos=(0, 0), size=(470, 50))

        # 定义一组按钮
        add_button = wx.Button(self.panel_2, label="添加", pos=(10, 10), size=(100, 35))
        del_button = wx.Button(self.panel_2, label="删除", pos=(120, 10), size=(100, 35))
        update_button = wx.Button(self.panel_2, label="修改", pos=(230, 10), size=(100, 35))
        show_button = wx.Button(self.panel_2, label="查看", pos=(340, 10), size=(100, 35))

        # w为按钮绑定相应事件函数，第一个参数为默认参数，指明为按钮类事件，第二个为事件函数名，第三个为按钮名
        self.Bind(wx.EVT_BUTTON, self.addReader, add_button)
        self.Bind(wx.EVT_BUTTON, self.delReader, del_button)
        self.Bind(wx.EVT_BUTTON, self.updateReader, update_button)
        self.Bind(wx.EVT_BUTTON, self.showReader, show_button)

        # 将列表和panel添加到主面板
        self.main_layout.Add(self.panel_1, 1)
        self.main_layout.Add(self.list, 6)
        self.main_layout.Add(self.panel_2, 1)

        self.SetSizer(self.main_layout)

        # 添加数据库操作对象
        self.dbhelper = ReaderHelper()
        datas = self.dbhelper.getAllReader()

        for data in datas:
            index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
            self.list.SetItem(index, 1, str(data[1]))
            self.list.SetItem(index, 2, str(data[2]))
            self.list.SetItem(index, 3, str(data[3]))
            self.list.SetItem(index, 4, str(data[4]))

    def addReader(self, evt):
        # 添加读者按钮，弹出添加读者框
        add_f = AddFrame(self, "添加读者窗口")
        add_f.Show(True)

    def delReader(self, evt):
        # 删除读者按钮，先选中,然后删除

        # 得到所有读者的学号，查看该读者是否有书籍未还
        list = []
        datas = self.dbhelper.getAllReader()
        for data in datas:
            list.append(data[0])

        selectId = self.list.GetFirstSelected()
        if selectId == -1:
            warn = wx.MessageDialog(self, message="未选中任何条目！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            readerid = self.list.GetItem(selectId, 0).Text  # 得到书本id
            readerName = self.list.GetItem(selectId, 1).Text
            dlg = wx.MessageDialog(self, message="确定删除学号  " + readerid + ':  ' + readerName + '吗？', caption="For Sure ",
                                   style=wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                for item in list:
                    if item == readerid:
                        dlg_again = wx.MessageDialog(self, message="该读者有书籍未还，是否确定删除？", caption="For Sure ", style=wx.YES_NO | wx.ICON_QUESTION)
                        if dlg_again.ShowModal() == wx.ID_YES:
                            rows = self.dbhelper.selectBook(readerid)
                            for row in rows:
                                self.dbhelper.deleteBook(row[0])
                            self.list.DeleteItem(selectId)  # 先在listctrl中删除选中行
                            self.dbhelper.deleteReader(readerid)
                            info = wx.MessageDialog(self, message='成功删除该读者', caption='删除读者', style=wx.YES_DEFAULT | wx.ICON_INFORMATION)
                            info.ShowModal()
                            info.Destroy()
                        else:
                            dlg.Destroy()
            else:
                dlg.Destroy()

    def updateReader(self, evt):
        # 修改按钮响应事件，点击修改按钮，弹出修改框
        selectId = self.list.GetFirstSelected()
        print(selectId)
        if selectId == -1:
            warn = wx.MessageDialog(self, message="未选中任何条目！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            update_f = UpdateFrame(self, "修改读者信息窗口", selectId)
            update_f.Show(True)

    def searchReader(self, evt):
        # 获取text中文本
        readerid = self.readerid_search.GetValue()
        readerName = self.readerName_search.GetValue()
        self.dbhelper = ReaderHelper()

        if readerid == "" and readerName == "":
            self.showAllReader()
        if readerid != "" and readerName == "":
            self.search_id(readerid)
        if readerid == "" and readerName != "":
            self.search_name(readerName)
        if readerid != "" and readerName != "":
            self.search_both(readerid, readerName)

    def addToList(self, id, reader):
        index = self.list.InsertItem(self.list.GetItemCount(), id)
        self.list.SetItem(index, 1, reader.getReaderName())
        self.list.SetItem(index, 2, reader.getBorrow_num())
        self.list.SetItem(index, 3, reader.getAble_num())
        self.list.SetItem(index, 4, reader.getMoney())

    def showAllReader(self):
        self.list.DeleteAllItems()
        # 添加数据库操作对象
        self.dbhelper = ReaderHelper()
        datas = self.dbhelper.getAllReader()

        for data in datas:
            index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
            self.list.SetItem(index, 1, str(data[1]))
            self.list.SetItem(index, 2, str(data[2]))
            self.list.SetItem(index, 3, str(data[3]))
            self.list.SetItem(index, 4, str(data[4]))

    def search_id(self, readerid):
        # 显示概述本原始信息
        self.list.DeleteAllItems()
        data = self.dbhelper.getReaderById(readerid)  # 通过id获取书本信息
        if data is None:
            warn = wx.MessageDialog(self, message="该读者不存在！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
            self.list.SetItem(index, 1, str(data[2]))
            self.list.SetItem(index, 2, str(data[6]))
            self.list.SetItem(index, 3, str(data[7]))
            self.list.SetItem(index, 4, str(data[8]))

    def search_name(self, readerName):
        # 显示概述本原始信息
        self.list.DeleteAllItems()
        datas = self.dbhelper.getReaderByName(readerName)  # 通过id获取书本信息
        if datas is None:
            warn = wx.MessageDialog(self, message="该读者不存在！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            for data in datas:
                index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
                self.list.SetItem(index, 1, str(data[2]))
                self.list.SetItem(index, 2, str(data[6]))
                self.list.SetItem(index, 3, str(data[7]))
                self.list.SetItem(index, 4, str(data[8]))

    def search_both(self, readerid, readerName):
        # 显示概述本原始信息
        self.list.DeleteAllItems()
        data = self.dbhelper.getReaderByBoth(readerid, readerName)  # 通过id获取书本信息
        if data is None:
            warn = wx.MessageDialog(self, message="该读者不存在！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
            self.list.SetItem(index, 1, str(data[2]))
            self.list.SetItem(index, 2, str(data[6]))
            self.list.SetItem(index, 3, str(data[7]))
            self.list.SetItem(index, 4, str(data[8]))

    def showReader(self, evt):
        # 修改按钮响应事件，点击修改按钮，弹出修改框
        selectId = self.list.GetFirstSelected()
        show_f = ShowFrame(self, "读者详细信息", selectId)
        show_f.Show(True)
