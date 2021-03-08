__metaclass__ = type
class Book:
	'''一个书本信息类，包括书号、书名、出版社、作者、可借状态、可约状态'''
	def __init__(self, bookid = "", bookName = "", author = "", publish = "", borrow = "", order = ""):
		self.bookid = bookid              # 书号
		self.bookName = bookName          # 书名
		self.author = author              # 作者
		self.publish = publish            # 出版社
		self.borrow = borrow              # 可借状态
		self.order = order                # 可约状态

	def setBookid(self, bookid):
		self.bookid = bookid

	def getBookid(self):
		return self.bookid

	def setBookName(self, name):
		self.bookName = name

	def getBookName(self):
		return self.bookName

	def setAuthor(self, author):
		self.author = author

	def getAuthor(self):
		return self.author

	def setPublish(self, publish):
		self.publish = publish

	def getPublish(self):
		return self.publish

	def setBorrow(self, borrow):
		self.borrow = borrow

	def getBorrow(self):
		return self.borrow

	def setOrder(self, order):
		self.order = order

	def getOrder(self):
		return self.order

if __name__ == "__main__":
	mybook = Book()
