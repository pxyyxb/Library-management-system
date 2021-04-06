#author = liuwei  date = 2017-06-02
                                              #导入日期模块
__metaclass__ = type



class Log:
	def __init__(self, personalid = "", password = ""):
		self.personalid = personalid                                    
		self.password = password                                      

	def setpersonalid(self, personalid):
		self.personalid = personalid

	def getpersonalid(self):
		return self.personalid

	def setpassword(self, password):
		self.password = password

	def getpassword(self):
		return self.password

if __name__ == "__main__":
	mybook = Log()