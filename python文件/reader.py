__metaclass__ = type
class Reader:
    def __init__(self, readerid = "", password = "", readerName = "", sex = "", dept = "", tele = "", borrow_num = "", able_num = "", money = ""):
        self.readerid = readerid
        self.password = password
        self.readerName = readerName
        self.sex = sex
        self.dept = dept
        self.tele = tele
        self.borrow_num = borrow_num
        self.able_num = able_num
        self.money = money

    def setReaderid(self, readerid):
        self.readerid = readerid

    def getReaderid(self):
        return self.readerid

    def setPassword(self, password):
        self.password = password

    def getPassword(self):
        return self.password

    def setReaderName(self, readerName):
        self.readerName = readerName

    def getReaderName(self):
        return self.readerName

    def setSex(self, sex):
        self.sex = sex

    def getSex(self):
        return self.sex

    def setDept(self, dept):
        self.dept = dept

    def getDept(self):
        return self.dept

    def SetTelephone(self, tele):
        self.tele = tele

    def getTelephone(self):
        return self.tele

    def setBorrow_num(self, borrow_num):
        self.borrow_num = borrow_num

    def getBorrow_num(self):
        return self.borrow_num

    def SetAble_num(self, able_num):
        self.able_num = able_num

    def getAble_num(self):
        return self.able_num

    def setMoney(self, money):
        self.money = money

    def getMoney(self):
        return self.money


if __name__ == "__main__":
    myreader = Reader()

