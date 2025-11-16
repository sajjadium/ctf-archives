import string, random, sys

alphabet = string.ascii_lowercase + "åäö "

def substitute(s: str, sub: str) -> str:
    assert set(sub) == set(alphabet) and len(sub) == len(alphabet)
    return "".join(alphabet[sub.index(c)] if c in alphabet else c for c in s.lower())

CHUNK_SIZE = 32
def substitute_better(s: str, init_sub: str) -> str:
    res = ""
    sub = init_sub
    for i in range(0, len(s), CHUNK_SIZE):
        pt = s[i:i+CHUNK_SIZE]
        nextsub = "".join(random.sample(alphabet, len(alphabet))) if len(s) > i + CHUNK_SIZE else ""
        res += substitute(pt + nextsub, sub)
        sub = nextsub
    return res

if __name__ == "__main__":
    with open(0, "r") as f:
        large_english_text = f.read()
    large_english_text = list(large_english_text)
    flag = sys.argv[1]
    large_english_text.insert(len(large_english_text) // 2, flag)
    plaintext = "".join(large_english_text)

    init_sub = random.sample(alphabet, len(alphabet))
    print(substitute_better(plaintext, init_sub))
