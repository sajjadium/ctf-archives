SECRET = '[CENSORED]' # this is captcha
CHECK = '203c0617e3bde7ec99b5b657417a75131e3629b8ffdfdbbbbfd02332'

def check_captcha(cc):
	msg = b'hello '
	msg += cc.encode()
	if calculate(msg) == CHECK:
		return True
	return False

def calculate(msg):
	c = []
	a = ord(b'[CENSORED]')
	b = ord(b'[CENSORED]')

	for m in msg:
		c.append(a ^ m)
		a = (a + b) % 256
	return bytes(c).hex()