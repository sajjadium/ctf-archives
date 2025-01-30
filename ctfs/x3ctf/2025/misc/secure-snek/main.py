def encrypt(data: str, a: int, b: int, seed: int = None) -> str:
    ...

def get_data() -> tuple:
    msg = input('Enter a message you want to encrypt:\n')
    print('Enter two or three parameters: a, b, seed separataed by spaces (a >= 0, b >= 0, seed is optional):')
    y = input().split()
    a, b = map(int, y[:2])
    seed = int(y[2]) if len(y) == 3 else None
    return msg, a, b, seed


if __name__ == '__main__':
    from auth import *
    print('Here is the encrypted flag: {}\n'.format(encrypt('MVM{FLAG_GOES_HERE}', 3, 8)))
    print('You may encrypt messages. Your messages must consist of only printable ascii characters and no spaces!')

    while True:
        try:
            x = get_data()
        except:
            print('There was an error with your data, please try again')
            continue
        try:
            encrypted = encrypt(*x)
            print(f'Encrypted message: {encrypted}\n' + '-'*50)
        except:
            print('Error! Please try again.')