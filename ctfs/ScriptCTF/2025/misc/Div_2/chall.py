import secrets
import decimal
decimal.getcontext().prec = 50
secret =  secrets.randbelow(1 << 127) + (1 << 127) # Choose a 128 bit number
for _ in range(1000):
    print("[1] Provide a number\n[2] Guess the secret number")
    choice = int(input("Choice: "))
    if choice == 1:
        num = input('Enter a number: ')
        fl_num = decimal.Decimal(num)
        assert int(fl_num).bit_length() == secret.bit_length()
        div = secret / fl_num
        print(int(div))
    if choice == 2:
        guess = int(input("Enter secret number: "))
        if guess == secret:
            print(open('flag.txt').read().strip())
        else:
            print("Incorrect!")
        exit(0)
