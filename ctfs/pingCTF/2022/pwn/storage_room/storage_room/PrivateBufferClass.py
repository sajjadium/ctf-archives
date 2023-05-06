class PrivateBufferClass:
	def __init__(self, size):
		self.__buffer = [None] * size
		self.__bufferSize = size
		self.__bufferIndex = 0

	def add(self, data):
		if type(data) == str or type(data) == bytes:
			for i in range(len(data)):
				self.__buffer[self.__bufferIndex] = data[i]
				self.__bufferIndex += 1
				if self.__bufferIndex >= self.__bufferSize:
					self.__bufferIndex = 0
		if self.__bufferIndex >= self.__bufferSize:
			self.__bufferIndex = 0

	def get(self):
		return self.__buffer
	
	def clear(self):
		self.__buffer = [None] * self.__bufferSize
		self.__bufferIndex = 0

	def __len__(self):
		return self.__bufferSize

	def position(self):
		return self.__bufferIndex
