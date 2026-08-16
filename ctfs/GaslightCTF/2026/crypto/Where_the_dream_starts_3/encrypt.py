from string import ascii_lowercase

def encrypt(pt: str, keyword: str) -> str:
    m = len(keyword)
    pt = list(map(lambda x: ascii_lowercase.index(x), pt))
    key = list(map(lambda x: ascii_lowercase.index(x), keyword))

    ct = ""
    for i in range(len(pt)):
        index = (pt[i] + key[i % m] + (i // m)) % 26
        char = ascii_lowercase[index]
        ct += char
    
    return ct

with open('gaslight-where-the-dream-starts-3/plaintext_and_keyword.txt', 'r') as file:
    ct = file.readline().strip()
    keyword = file.readline().strip()

print(encrypt(ct, keyword))
