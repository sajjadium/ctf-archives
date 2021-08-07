'''
Base-3 AES

Just use SAGE lmao
'''

T_SIZE  = 3             # Fixed trits in a tryte
W_SIZE  = 3             # Fixed trytes in a word (determines size of matrix)
POLY    = (2, 0, 1, 1)  # Len = T_SIZE + 1

POLY2   = ((2, 0, 1), (1, 2, 0), (0, 2, 1), (2, 0, 1))  # Len = W_SIZE + 1
CONS    = ((1, 2, 0), (2, 0, 1), (1, 1, 1))     # Len = W_SIZE 
I_CONS  = ((0, 0, 2), (2, 2, 1), (2, 2, 2))     # Inverse of CONS (mod POLY2)

# Secure enough ig
SBOX    = (6, 25, 17, 11, 0, 19, 22, 14, 3, 4, 23, 12, 15, 7, 26, 20, 9, 1, 2, 18, 10, 13, 5, 21, 24, 16, 8)

KEYLEN = 28

def up(array, size, filler):    # If only there was APL in python :pensiv:
    ''' Groups up things in a tuple based on size '''
    l = len(array)
    array += (filler,) * (-l % size)
    return tuple([array[i:i + size] for i in range(0, l, size)])

def down(array): 
    ''' Ungroups objects in tuple '''
    return sum(array, ())

def look(array):
    if type(array) is int:
        return array
    while type(array[0]) is not int:
        array = down(array)
    return sum(array)

def clean(array):
    while len(array) > 1:
        if look(array[-1]):
            break
        array = array[:-1]
    return tuple(array)

def int_to_tri(num):    # positive only
    out = []
    while num:
        num, trit = divmod(num, 3)
        out.append(trit)
    return tuple(out) if out else (0,)

def tri_to_int(tri):
    out = 0
    for i in tri[::-1]:
        out *= 3
        out += i
    return out

tri_to_tyt  = lambda tri: up(tri, T_SIZE, 0)
tyt_to_tri  = lambda tyt: down(tyt)

int_to_tyt  = lambda num: tri_to_tyt(int_to_tri(num))
tyt_to_int  = lambda tyt: tri_to_int(down(tyt))

tyt_to_wrd  = lambda tyt: up(tyt, W_SIZE, (0,) * T_SIZE)
wrd_to_tyt  = lambda wrd: down(wrd)

def apply(func, filler=None):    # scale up operations (same len only)
    def wrapper(a, b):
        return tuple(func(i, j) for i, j in zip(a, b))
    return wrapper

xor     = lambda a, b: (a + b) % 3
uxor    = lambda a, b: (a - b) % 3
t_xor   = apply(xor)
t_uxor  = apply(uxor)
T_xor   = apply(t_xor)
T_uxor  = apply(t_uxor)
W_xor   = apply(T_xor)
W_uxor  = apply(T_uxor)

def tri_mul(A, B):
    c = [0] * len(B)
    for a in A[::-1]:
        c = [0] + c
        x = tuple(b * a % 3 for b in B)
        c[:len(x)] = t_xor(c, x) # wtf slice assignment exists??? 
    return clean(c)

def tri_divmod(A, B):
    B = clean(B)
    A2  = list(A)
    c   = [0]
    while len(A2) >= len(B):
        c = [0] + c
        while A2[-1]:
            A2[-len(B):] = t_uxor(A2[-len(B):], B)
            c[0] = xor(c[0], 1)
        A2.pop()
    return clean(c), clean(A2) if sum(A2) else (0,)

def tri_mulmod(A, B, mod=POLY):
    c = [0] * (len(mod) - 1)
    for a in A[::-1]:
        c = [0] + c
        x = tuple(b * a % 3 for b in B)
        c[:len(x)] = t_xor(c, x) # wtf slice assignment exists??? 
        while c[-1]:
            c[:] = t_xor(c, mod)
        c.pop()
    return tuple(c)

def egcd(a, b):
    x0, x1, y0, y1 = (0,), (1,), b, a
    while sum(y1):
        q, _ = tri_divmod(y0, y1)
        u, v = tri_mul(q, y1), tri_mul(q, x1)
        x0, y0 = x0 + (0,) * len(u), y0 + (0,) * len(v)
        y0, y1 = y1, clean(t_uxor(y0, u) + y0[len(u):])
        x0, x1 = x1, clean(t_uxor(x0, v) + x0[len(v):])
    return x0, y0

def modinv(a, m=POLY):
    _, a = tri_divmod(a, m)
    x, y = egcd(a, m)
    if len(y) > 1:
        raise Exception('modular inverse does not exist')
    return tri_divmod(x, y)[0]

def tyt_mulmod(A, B, mod=POLY2, mod2=POLY):
    fil = [(0,) * T_SIZE]
    C = fil * (len(mod) - 1)
    for a in A[::-1]:
        C = fil + C
        x = tuple(tri_mulmod(b, a, mod2) for b in B)
        C[:len(x)] = T_xor(C, x)
        
        num = modinv(mod[-1], mod2)
        num2 = tri_mulmod(num, C[-1], mod2)
        x = tuple(tri_mulmod(m, num2, mod2) for m in mod)
        C[:len(x)] = T_uxor(C, x)

        C.pop()
    return C

'''
AES functions
'''

int_to_byt = lambda x: x.to_bytes((x.bit_length() + 7) // 8, "big")
byt_to_int = lambda x: int.from_bytes(x, byteorder="big")

def gen_row(size = W_SIZE):
    out = () 
    for i in range(size):
        row = tuple(list(range(i * size, (i + 1) * size)))
        out += row[i:] + row[:i]
    return out

SHIFT_ROWS = gen_row()
UN_SHIFT_ROWS = tuple([SHIFT_ROWS.index(i) for i in range(len(SHIFT_ROWS))])

def rot_wrd(tyt): # only 1 word so treat as tyt array
    return tyt[1:] + tyt[:1]
    
def sub_wrd(tyt):
    return tuple(int_to_tyt(SBOX[tri_to_int(tri)])[0] for tri in tyt)

def u_sub_wrd(tyt):
    return tuple(int_to_tyt(SBOX.index(tri_to_int(tri)))[0] for tri in tyt)

def rcon(num):  # num gives number of constants given
    out = int_to_tyt(1)
    for _ in range(num - 1):
        j = (0,) + out[-1]
        while j[-1]:   # xor until back in finite field
            j = t_xor(j, POLY)
        out += (j[:T_SIZE],)
    return out

def expand(tyt):
    words   = tyt_to_wrd(tyt) 
    size    = len(words)
    rnum    = size + 3
    rcons   = rcon(rnum * 3 // size)

    for i in range(size, rnum * 3):
        k   = words[i - size]
        l   = words[i - 1]
        if i % size == 0:
            s = sub_wrd(rot_wrd(l))
            k = T_xor(k, s)
            k = (t_xor(k[0], rcons[i // size - 1]),) + k[1:]
        else:
            k = T_xor(k, l)
        words = words + (k,)

    return up(down(words[:rnum * 3]), W_SIZE ** 2, int_to_tyt(0)[0])

def mix_columns(tyt, cons=CONS):
    tyt = list(tyt)
    for i in range(W_SIZE):
        tyt[i::W_SIZE] = tyt_mulmod(tyt[i::W_SIZE], cons)
    return tuple(tyt)

def a3s(msg, key): 
    m       = byt_to_int(msg)
    k       = byt_to_int(key)
    m       = up(int_to_tyt(m), W_SIZE ** 2, int_to_tyt(0)[0])[-1] # Fixed block size
    k       = int_to_tyt(k)
    keys    = expand(k) # tryte array
    assert len(keys) == KEYLEN

    ctt = T_xor(m, keys[0])

    for r in range(1, len(keys) - 1):
        ctt = sub_wrd(ctt)                          # SUB...
        ctt = tuple([ctt[i] for i in SHIFT_ROWS])   # SHIFT...
        ctt = mix_columns(ctt)                      # MIX...
        ctt = T_xor(ctt, keys[r])                   # ADD!

    ctt  = sub_wrd(ctt)
    ctt  = tuple([ctt[i] for i in SHIFT_ROWS])
    ctt  = T_xor(ctt, keys[-1])                     # last key

    ctt = tyt_to_int(ctt)
    return int_to_byt(ctt)

def d_a3s(ctt, key):
    c       = byt_to_int(ctt)
    k       = byt_to_int(key)
    c       = up(int_to_tyt(c), W_SIZE ** 2, int_to_tyt(0)[0])[-1] # Fixed block size
    k       = int_to_tyt(k)
    keys    = expand(k)[::-1] # tryte array
    assert len(keys) == KEYLEN

    msg = c
    msg = T_uxor(msg, keys[0])

    for r in range(1, len(keys) - 1):
        msg = tuple([msg[i] for i in UN_SHIFT_ROWS])    # UN SHIFT...
        msg = u_sub_wrd(msg)                            # UN SUB...
        msg = T_uxor(msg, keys[r])                      # UN ADD...
        msg = mix_columns(msg, I_CONS)                  # UN MIX!

    msg  = tuple([msg[i] for i in UN_SHIFT_ROWS])
    msg  = u_sub_wrd(msg)
    msg  = T_uxor(msg, keys[-1])                     # last key

    msg = tyt_to_int(msg)
    return int_to_byt(msg)

def chunk(c):
    c   = byt_to_int(c)
    c   = up(int_to_tyt(c), W_SIZE ** 2, int_to_tyt(0)[0])
    x   = tuple(tyt_to_int(i) for i in c)
    x   = tuple(int_to_byt(i) for i in x)
    return x

def unchunk(c):
    out = []
    for i in c:
        j   = byt_to_int(i)
        j   = up(int_to_tyt(j), W_SIZE ** 2, int_to_tyt(0)[0])
        assert len(j) == 1
        out.append(j[0])
    out = down(out)
    out = tyt_to_int(out)
    return int_to_byt(out)

def gen():
    flag, key = eval(open("secret.txt", "r").read())
    
    out = []
    for i in chunk(flag):
        out.append(a3s(i, key))

    with open("challenge.txt", "w+") as f:
        f.write(f'Encryption of "sus.": {a3s(b"sus.", key)}' + "\n")
        f.write(f"Encryption of the flag: {unchunk(out)}" + "\n")

if __name__ == "__main__":
    gen()
