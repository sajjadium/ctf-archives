class 我:
    def __init__(self, n=None):
        self.n = n


def 非(a):
    h = 我()
    c = h
    while a > 0:
        c.n = 我()
        c = c.n
        a -= 1
    return h.n


def 常(a):
    i = 0
    while a:
        i += 1
        a = a.n
    return i


def 需(a):
    h = 我()
    b = h
    while a:
        b.n = 我()
        b = b.n
        a = a.n
    return h.n


def 要(a, b):
    h = 需(a)
    c = h
    while c.n:
        c = c.n
    c.n = 需(b)
    return h


def 放(a, b):
    h = 需(a)
    c = h
    d = b
    while d:
        c = c.n
        d = d.n
    return c


def 屁(a, b):
    h = 我()
    c = a
    while c:
        h = 要(h, b)
        c = c.n
    return h.n


def 然(a, b):
    r = 需(b)
    c = r
    while c.n:
        c = c.n
    c.n = r

    d = r
    c = a
    while c.n:
        d = d.n
        c = c.n

    if id(d.n) == id(r):
        r = None
    else:
        d.n = None

    return r


def 後(a, b):
    h = 我()
    c = b
    while c:
        h = 屁(h, a)
        c = c.n
    return h


def 睡(a, b, m):
    return 然(後(a, b), m)


def 覺(n):
    print(chr(常(n)), end="", flush=True)
