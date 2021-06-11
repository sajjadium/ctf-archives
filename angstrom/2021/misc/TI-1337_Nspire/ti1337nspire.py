#!/run/cpython/python
from multiprocessing import Process, Queue

def sandbox(calculation, result):
	from sys import addaudithook
	from os import _exit
	import constants
	code = compile(calculation, '<math>', 'exec')
	def audit(name, args):
		if not audit.calculated and name == 'exec':
			audit.calculuated = True
		else: _exit(1)
	audit.calculated = False
	addaudithook(audit)

	# College Board SAT compliance (prevent cheating)
	if (any(s in calculation for s in ('__', '==', 'del', 'not',
		'in', 'if', 'while', 'for', 'await', 'with', 'import'))
		or set(calculation) & set('()[]{}+-*@/%&|^<>!~')): return
	state = {}
	exec(code, {'__builtins__': {}, 'constants': constants}, state)
	result.put(state)

calculation = ''
print('> ', end='')
while (i := input()):
	print('> ', end='')
	calculation += i + '\n'
result = Queue()
p = Process(target=sandbox, args=(calculation, result))
p.start()
p.join()
if result.empty():
	print("Hey, that's not math!")
else:
	for var in (state := result.get()):
		print(f"{var} = {state[var]}")
