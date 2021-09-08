from Crypto.Util.number import bytes_to_long


def displace(a, base):
    res = []
    for i in range(base):
        if base + i >= len(a):
            for j in range(base - 1, i - 1, -1):
                res.append(a[j])
            return res
        res.append(a[base + i])
        res.append(a[i])
    for j in range(len(a) - 1, 2 * base - 1, -1):
        res.append(a[j])
    return res


def flag_encoder(flag):
    encoded_flag = []
    n = len(flag)
    for i in range(n):
        encoded_flag.append(ord(flag[i]) ^ ord(flag[i - 1]))
    for i in range(n):
        encoded_flag[i] ^= encoded_flag[n - i - 1]
    a = []
    for i in range(0, n, 3):
        a.append(encoded_flag[i] + encoded_flag[i + 1])
        a.append(encoded_flag[i + 1] + encoded_flag[i + 2])
        a.append(encoded_flag[i + 2] + encoded_flag[i])
    encoded_flag = a
    for i in range(1, n):
        if i % 6 == 0:
            encoded_flag = displace(encoded_flag, i)
    encoded_flag = ''.join(chr(encoded_flag[i]) for i in range(n))
    return encoded_flag


with open('flag', 'rb') as f:
    flag = f.read().decode('UTF-8')
    print(str(bytes_to_long(flag_encoder(flag).encode())))
