from Crypto.Cipher import AES
import math


def xor(bytes_a: bytes, bytes_b: bytes, block_len: int = 128) -> bytes:
    return bytes([a ^ b for (a, b) in zip(bytes_a, bytes_b)])

def b_and(bytes_a: bytes, bytes_b: bytes, block_len: int = 128) -> bytes:
    return bytes([a & b for (a, b) in zip(bytes_a, bytes_b)])

def degree(poly) -> list:
    while poly and poly[-1] == 0:
        poly.pop()   # normalize
    return len(poly)-1

def lead(poly) -> list:
    while poly and poly[-1] == 0:
        poly.pop()   # normalize
    return poly[-1]

def mul_poly(poly1, poly2) -> list:
    out = [0 for _ in range(len(poly1) + len(poly2) - 1)]
    for x,i in enumerate(poly1):
        for y,j in enumerate(poly2):
            out[x+y] = (out[x+y]+(i*j)) % 3
    return out

def add(X: int, Y: int):
    # add two numbers in GF(3^81)
    # x represented in GF(3^81)
    x = [(X // (3 ** i)) % 3 for i in range(81)]

    # y represented in GF(3^81)
    y = [(Y // (3 ** i)) % 3 for i in range(81)]

    r = [(a + b) % 3 for a,b in zip(x, y)]

    Z = sum([r[i] * (3 ** i) for i in range(len(r))])
    return Z

def sub(X: int, Y: int):
    # subtract two numbers in GF(3^81)
    # x represented in GF(3^81)
    x = [(X // (3 ** i)) % 3 for i in range(81)]

    # y represented in GF(3^81)
    y = [(Y // (3 ** i)) % 3 for i in range(81)]

    r = [(a - b) % 3 for a,b in zip(x, y)]

    Z = sum([r[i] * (3 ** i) for i in range(len(r))])
    return Z

def mul(X: int, Y: int):
    # I'm using a custom field, its all homebrew
    # We're working in GF(3^81) coz were cool B)
    # its slightly bigger than 2^128

    # modulus of the field
    modulus = [1,2,1,2,2,2,1,1,1,1,1,2,2,2,1,0,2,2,0,2,2,0,1,2,1,1,1,2,2,1,1,0,0,2,2,0,2,0,1,0,0,1,2,2,0,2,1,2,2,0,0,2,0,0,1,0,2,1,0,1,2,1,0,0,1,2,0,1,2,0,0,1,0,0,1,1,0,0,0,2,0,1]
    # x represented in GF(3^81)
    x = [(X // (3 ** i)) % 3 for i in range(81)]

    # y represented in GF(3^81)
    y = [(Y // (3 ** i)) % 3 for i in range(81)]

    # calculate product
    mul_res = mul_poly(x, y)

    # long division by modulus  
    r = mul_res
    
    while r.count(0) != len(r) and degree(r) >= degree(modulus):
        d = [0] * (degree(r) - degree(modulus)) + modulus
        mult = (lead(r) * pow(lead(d), -1 , 3)) % 3
        d2 = ([(mult * coeff) % 3 for coeff in d])
        r = [(a - b) % 3 for a,b in zip(r, d2)]

    Z = sum([r[i] * (3 ** i) for i in range(len(r))])
    return Z


def ghash(H: bytes, X: bytes, block_len: int=128) -> bytes:
    block_len_b = (block_len//8) 
    m = len(X) // block_len_b

    X_blocks = [int.from_bytes(X[i*block_len_b:(i+1)*block_len_b], 'big') for i in range(m)]
    H_int = int.from_bytes(H, 'big')
    # 0th block
    Y_i = 0
    # iterate through the blocks
    Y_prev = Y_i
    for i in range(m):
        X_i = X_blocks[i]

        # each round is then Y_i = (X_i + Y_i-1) * H in GF(3^81)
        Y_i = mul(add(X_i, Y_prev), H_int)
        Y_prev = Y_i
    return (Y_i).to_bytes(block_len_b + 1, 'big')

def inc(Y, ctr_len):
    Y = int.from_bytes(Y, 'big')
    # 0xffffff....
    mask = 2 ** (ctr_len) - 1
    
    # Y = iv || ctr
    # ignore iv, increment ctr
    Y_inc = ((Y >> ctr_len) << ctr_len) ^ (((Y & mask) + 1) & mask)
    return Y_inc.to_bytes(16, 'big')


def gctr(cipher, icb: bytes, X: bytes, operation: str, block_len = 128, ctr_len = 32):
    if not X:
        return b''

    # our ciphertext blocks are 16 + 1 byte long
    # bcs our |GF| is bigger than 16 bytes
    # but the plaintext blocks have to be 16 bytes
    # as the |GF| is still smaller than 17 bytes
    # and we don't want to overflow
    if operation == 'enc':
        block_len_input = block_len // 8 
        block_len_output = block_len // 8 + 1
    elif operation == 'dec':
        block_len_input = block_len // 8 + 1
        block_len_output = block_len // 8
    elif operation == 'tag':
        block_len_input = block_len // 8 + 1
        block_len_output = block_len // 8 + 1

    n = math.ceil(len(X) / block_len_input)

    X_blocks = [int.from_bytes(X[i*block_len_input:(i+1)*block_len_input], 'big') for i in range(n)]

    # counter block
    cb = [icb]

    # generate counter blocks
    for i in range(1, n):
        cb_next = inc(cb[i-1], ctr_len)
        cb.append(cb_next)

    # calculate ciphertexts
    Y_blocks = []
    for i in range(n):
        X_next = X_blocks[i]
        assert X_next < 3 ** 81
        cb_next = cb[i]
        if operation == 'dec':
            Y_next = sub(X_next, int.from_bytes(cipher.encrypt(cb_next), 'big'))
        else:
            Y_next = add(X_next, int.from_bytes(cipher.encrypt(cb_next), 'big'))
        Y_blocks.append(Y_next)
    if operation == 'dec':
        Y = b''.join([(x).to_bytes(block_len_output, 'big').strip(b"\x00") for x in Y_blocks])
    else:
        Y = b''.join([(x).to_bytes(block_len_output, 'big') for x in Y_blocks])

    return Y

def aes_gua_decrypt(ct: bytes, key: bytes, iv: bytes, additional_data: bytes, tag: bytes, t: int, block_len = 128):
    assert block_len == len(key) * 8
    assert 0 < len(iv) * 8 < block_len
    assert t == len(tag) * 8 

    ctr_len = block_len - len(iv) * 8

    cipher = AES.new(key, AES.MODE_ECB)
    # mac subkey
    H = cipher.encrypt(b'\x00' * (block_len // 8))

    # first keystream block
    J_0 = iv + b'\x01'.rjust((ctr_len) // 8, b'\x00')
    # first decrypted block
    pt = gctr(cipher, inc(J_0, ctr_len), ct, 'dec')

    ct_len, A_len = len(ct) * 8, len(additional_data) * 8
    u = 128 * math.ceil(ct_len / 128) - ct_len
    v = 128 * math.ceil(A_len / 128) - A_len

    # calculate hash
    zero_vector_v = b'\x00' * (v // 8)
    zero_vector_u = b'\x00' * (u // 8)
    A_64_len = int.to_bytes(A_len, 8, 'big')
    ct_64_len = int.to_bytes(ct_len, 8, 'big')
    S = ghash(H, additional_data + zero_vector_v + ct + zero_vector_u + A_64_len + ct_64_len)

    mask = b'\xff' * (t // 8)
    tag_prim = b_and(gctr(cipher, J_0, S, 'tag'), mask)
    if tag == tag_prim:
        return pt
    else:
        raise Exception("Invalid tag")

def aes_gua_encrypt(pt: bytes, key: bytes, iv: bytes, additional_data: bytes, t: int, block_len = 128) -> (bytes, bytes):
    assert block_len == len(key) * 8
    assert 0 < len(iv) * 8 <= block_len

    ctr_len = block_len - len(iv) * 8

    cipher = AES.new(key, AES.MODE_ECB)
    # mac subkey
    H = cipher.encrypt(b'\x00' * (block_len // 8))

    # first keystream block
    J_0 = iv + b'\x01'.rjust((ctr_len) // 8, b'\x00')

    # first encrypted block
    ct = gctr(cipher, inc(J_0, ctr_len), pt, 'enc')

    ct_len, A_len = len(ct) * 8, len(additional_data) * 8
    u = 128 * math.ceil(ct_len / 128) - ct_len
    v = 128 * math.ceil(A_len / 128) - A_len

    # calculate hash
    zero_vector_v = b'\x00' * (v // 8)
    zero_vector_u = b'\x00' * (u // 8)
    A_64_len = int.to_bytes(A_len, 8, 'big')
    ct_64_len = int.to_bytes(ct_len, 8, 'big')

    S = ghash(H, additional_data + zero_vector_v + ct + zero_vector_u + A_64_len + ct_64_len)

    # Calculate mac tag
    T = gctr(cipher, J_0, S, 'tag')[:t // 8]  

    return ct, T

if __name__ == "__main__":
    # NIST test vector 2
    key = bytearray.fromhex('fe47fcce5fc32665d2ae399e4eec72ba')
    iv = bytearray.fromhex('5adb9609dbaeb58cbd6e7275')
    #plaintext = bytearray.fromhex('7c0e88c88899a779228465074797cd4c2e1498d259b54390b85e3eef1c02df60e743f1b840382c4bccaf'
    #                              '3bafb4ca8429bea063')
    plaintext = b'test12345678mnbvcxzdsadasdadas3123r123312312adskadkadk222'
    associated_data = bytearray.fromhex('88319d6e1d3ffa5f987199166c8a9b56c2aeba5a')
    t = 128

    ciphertext, auth_tag = aes_gua_encrypt(plaintext, key, iv, associated_data, t)

    pt = aes_gua_decrypt(ciphertext, key, iv, associated_data, auth_tag, t)
    print(pt)
    assert (aes_gua_decrypt(ciphertext, key, iv, associated_data, auth_tag, t).hex() == plaintext.hex())
    try: 
        (aes_gua_decrypt(b'\x01' + ciphertext[:1], key, iv, associated_data, auth_tag, t).hex() == plaintext.hex())
        print('tag failed')
        exit(1)
    except Exception as E:
        pass

    print("tests ok")