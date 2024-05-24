from Crypto.Util.number import getPrime, bytes_to_long as btl

menu = '''(1) Encrypt Message
(2) Receive Flag
(3) Exit'''

e = 1337
size = 1024
flag = open('flag.txt', 'r').read().rstrip()

print('Welcome to the L3ak Really Simple Algorithm (RSA) Encryption Service™!')
print('Here you can encrypt your own message, or choose to receive the encrypted flag.')
print('Good luck!\n')

while True:

    p, q = getPrime(size), getPrime(size)
    n = p*q
    print(menu)

    option = int(input('Select Option: '))
    if option == 1:
        message = btl(input('Your Message: ').encode())
        enc_msg = pow(message, e, n)
        print(f'n = {n}')
        print(f'c = {enc_msg}')
    elif option == 2:
        enc_flag = pow(btl(flag.encode()), e, n)
        print(f'n = {n}')
        print(f'flag = {enc_flag}')
    elif option == 3:
        print('Goodbye!')
        exit()
    else:
        print('Invalid choice! Please try again.')

