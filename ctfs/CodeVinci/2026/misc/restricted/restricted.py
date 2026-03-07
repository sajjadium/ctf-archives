#!/usr/bin/env python3
import sys
import code

sys.excepthook = sys.__excepthook__

class RestrictedConsole(code.InteractiveConsole):

	def __init__(self, locals, blacklist, *a, **kw):
		super().__init__(locals, *a, **kw)
		self.blacklist = blacklist.copy()
		
	def runsource(self, source, *a, **kw):
		if not source.isascii() or any(word in source for word in self.blacklist):
			print("Blacklisted word detected, exiting ...")
			sys.exit(1)
		return super().runsource(source, *a, **kw)
	
	def write(self, data):
		sys.stdout.write(data)

safe_builtins = {
	'exec': exec
}

locals = {'__builtins__': safe_builtins}

blacklist = [
	'import', 'os', 'system', 'subproces',
	'subclasses', 'globals', 'x'
    'sh', 'flag', '\'', '"', '0', '1',
    '2', '3', '4', '5', '6', '7', '8', '9',
	'locals', '{', '}', 'open', 'built', 'chr'
]

RestrictedConsole(locals, blacklist).interact()
