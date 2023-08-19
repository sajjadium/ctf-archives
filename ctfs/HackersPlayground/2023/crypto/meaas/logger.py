from sys import stdout, stderr

class Logger:
	verbose, info, warning, error, none = 0, 1, 2, 3, 4

	def __init__(self, loglevel=0, output=None):
		if type(output) is str:
			self.fp = open(output, "w")
			self.isStrPath = True
		else:
			self.fp = output
			self.isStrPath = False

		self.loglevel = loglevel

	def Log(self, level, msg, prefix=None):
		if self.loglevel <= level:
			if prefix: self.fp.write(prefix)
			if type(msg) is str:
				self.fp.write(msg + '\n')
			else:
				self.fp.write(msg.decode() + '\n')

	def Error(self, msg):
		self.Log(self.error, msg, prefix = "[Err] ")

	def Warning(self, msg):
		self.Log(self.warning, msg, prefix = "[Warn] ")

	def Info(self, msg):
		self.Log(self.info, msg, prefix = "[Info] ")

	def Verbose(self, msg):
		self.Log(self.verbose, msg, prefix = "[Verbose] ")

	def Close(self):
		if self.isStrPath:
			self.fp.close()

noLog = Logger(Logger.none, "/dev/null")
