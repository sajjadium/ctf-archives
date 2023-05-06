import ast, sys, re, struct, tempfile, os
from uuid import uuid4

if len(sys.argv) < 2:
	sys.argv.append('test.asm')
if len(sys.argv) < 3:
	sys.argv.append(tempfile.mktemp(prefix='%s_' % uuid4(), dir='/tmp/relativity'))

f = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'wb')

# Opcode definition
handler = {}
def sd(src=0, dst=0, src2=None):
	r = chr((src & 0xf) | ((dst & 0xf) << 4))
	if src2 is not None:
		r = r + chr((src2 & 0xf))
	return r
def reg(x):
	if REGS.match(x):
		return int(REGS.match(x).group(2))
def push(x):
	src = reg(x)
	return '\x03' + sd(src=src)
def arith(code):
	def f(x, y, z):
		dst, src, src2 = reg(x), reg(y), reg(z)
		return chr(code) + sd(src=src, src2=src2, dst=dst)
	return f
def li(x, y):
	dst = reg(x)
	return chr(9) + sd(dst=dst) + struct.pack("<L", y)
def print_op(x):
	src = reg(x)
	return chr(12) + sd(src=src)
def ls(x, y):
	dst = reg(x)
	return chr(10) + sd(dst=dst) + struct.pack("<L", len(y)) + y

def jmp(x):
	return chr(5) + struct.pack("<L", x)
def jz(x, y):
	src = reg(x)
	return chr(15) + sd(src=src) + struct.pack("<L", y)
def jnz(x, y):
	src = reg(x)
	return chr(8) + sd(src=src) + struct.pack("<L", y)
def call(x, y):
	return chr(6) + struct.pack("<LH", y, x)
def ret():
	return chr(7)
def loadarg(x, y):
	dst = reg(x)
	return chr(11) + sd(dst=dst) + struct.pack("<H", y)
def pop(x):
	dst = reg(x)
	return chr(4) + sd(dst=dst)
def mov(x, y):
	dst, src = reg(x), reg(y)
	return chr(0) + sd(dst=dst, src=src)
refneeded = {
	'jmp': (1, 5, [0]),
	'jnz': (2, 6, [1]),
	'jz': (2, 6, [1]),
	'call': (3, 7, [1])
}
handler['mov'] = mov
handler['push'] = push
handler['add'] = arith(1)
handler['sub'] = arith(2)
handler['mul'] = arith(13)
handler['exit'] = lambda: '\x0e'
handler['li'] = li
handler['print'] = print_op
handler['ls'] = ls
handler['jmp'] = jmp
handler['jz'] = jz
handler['jnz'] = jnz
handler['call'] = call
handler['ret'] = ret
handler['loadarg'] = loadarg
handler['pop'] = pop

# Assembly parser
REGS = re.compile(r'(r(1[0-5]|[0-9]))')
COMMENT = re.compile(r'#(.*)$')
result = ''
reloc = []
labels = {}

def parse_args(args):
	if args is not None:
		args = REGS.sub(r"'\1'", args)
		args = args.strip()
		try:
			if args:
				args = ast.literal_eval(args)
		except:
			raise Exception('Invalid arguments: %s' % orig)
		if op not in handler:
			raise Exception('Unknown opcode: %s' % op)
		if type(args)is not tuple:
			args = args,
	else:
		args = ()
	return args

for line in f:
	line = COMMENT.sub('', line)
	line = line.strip()
	if not line: continue
	if line[-1] == ':':
		labels[line[:-1]] = len(result)
		continue
	if ' ' not in line:
		op = line
		args = None
	else:
		op, args = line.split(' ', 1)
	op = op.lower()
	orig = args
	prev = len(result)
	if op in refneeded:
		reloc.append((len(result), op, args))
		result += '?' * refneeded[op][1]
	else:
		args = parse_args(args)
		result += handler[op](*args)

# Relocator
for offset, op, args in reloc:
	binding, length, rel = refneeded[op]
	node = ast.parse(args)
	val = node.body[0].value
	if not isinstance(val,ast.Tuple):
		args += ','
	args = args.split(',')
	for i in rel:
		args[i] = str(labels[args[i].strip()])
	args = ','.join(args)
	args = parse_args(args)
	result = result[:offset] + handler[op](*args) + result[offset+length:]

f2.write('GRRR' + struct.pack(">L", len(result)).encode('hex') + result.encode('hex'))
f2.close()

# Interpreter
os.system('node ./interpreter.js working/%s' % sys.argv[2])
os.system('rm -f %s' % sys.argv[2])