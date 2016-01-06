import hashlib

class hashtable():
	def __init__(self, size):
		self.load = 0
		self.size = size
		self.array = [[]for x in xrange(0 , size)]
		
	def add(self, str):
		self.load 
		m = hashlib.sha1()
		m.update(str)
		key = int(m.hexdigest(), 16) % self.size
		self.array[key].append(str)
		if float(self.load) / self.size > 0.75:
			self.grow()

		
	def visited(self, str):
		m = hashlib.sha1()
		m.update(str)
		key = int(m.hexdigest(), 16) % self.size
		return str in self.array[key]

		
	def grow(self):
		oarray = self.array
		self.size *= 2
		self.array = [[]for x in xrange(0 , self.size)]
		
		#copy
		for list in oarray:
			for ele in list:
				self.add(ele)
				
	def printtable(self):
		for list in self.array:
			print list