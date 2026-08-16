from string import ascii_lowercase

def encrypt(pt: str, K: int) -> str:
    pt = list(map(lambda x: ascii_lowercase.index(x), list(pt)))
    ct = []
    for x in pt:
        ct.append((x + K) % 26)
    
    ct = list(map(lambda x: ascii_lowercase[x], ct))
    ct = ''.join(ct)
    return ct

with open('gaslight-where-the-dream-starts-1/flag_and_key.txt', 'r') as file:
    flag, K = file.readline().split()
    K = int(K)

print(encrypt(flag, K))
