'''读者所能进行的操作'''

import wx
from borrowhelper import *

__metaclass__ = type

def return_book(self, evt):
    selectId = self.list.GetFirstSelected()
    if selectId == -1:
        warn = wx.MessageDialog(self, message="未选中任何条目！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
        warn.ShowModal()  # 提示错误
        warn.Destroy()
        return
    else:
        bookid = self.list.GetItem(selectId, 0).Text  # 得到书本id
        self.list.DeleteItem(selectId)  # 先在listctrl中删除选中行
        readerid = self.readerid  # 传入readerid

        # 删去借阅表中的记录
        self.dbhelper = BorrowHelper()
        self.dbhelper.delete_record(readerid, bookid)

        # 获得该书籍的预约状态
        data_1 = self.dbhelper.pre_bookborrow(bookid)

        # 准备好修改后的读者信息
        data_2 = self.dbhelper.pre_reader(readerid)
        borrow_num = str(data_2[0] - 1)
        able_num = str(data_2[1] + 1)
        money = str(0)

        reader = Reader(readerid, "", "", "", "", "", borrow_num, able_num, money)

        # 如果已经被预约，不修改可借状态和预约状态，只修改读者状态
        if data_1 == 0:
            self.dbhelper.update_reader(readerid, reader)
        else:
            self.dbhelper.update_reader(readerid, reader)
            borrow = str(1)
            order = str(0)
            book = Book(bookid, "", "", "", borrow, order)
            self.dbhelper.update_book(bookid, book)




