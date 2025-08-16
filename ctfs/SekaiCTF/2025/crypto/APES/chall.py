import os
FLAG = os.getenv("FLAG", "SEKAI{TESTFLAG}")

def play():
    plainperm = bytes.fromhex(input('Plainperm: '))
    assert sorted(plainperm) == list(range(256)), "Invalid permutation"

    key = os.urandom(64)
    def f(i):
        for k in key[:-1]:
            i = plainperm[i ^ k]
        return i ^ key[-1]

    cipherperm = bytes(map(f, range(256)))
    print(f'Cipherperm: {cipherperm.hex()}')
    print('Do you know my key?')
    return bytes.fromhex(input()) == key

if __name__ == '__main__':
    # if you're planning to brute force anyway, let's prevent excessive connections
    while not play():
        print('Bad luck, try again.')
    print(f'APES TOGETHER STRONG! {FLAG}')