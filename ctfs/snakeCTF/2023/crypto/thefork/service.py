import forkaes
import os
import signal

TIMEOUT = 600

assert("KEY" in os.environ)
KEY = os.environ["KEY"]
KEY = [ x for x in bytes.fromhex(KEY)]
assert len(KEY) == forkaes.BLOCK_SIZE


def main():
    print("TheFORK oracle is here!")

    tweak = [ int.from_bytes(os.urandom(1), byteorder='big') for _ in range(forkaes.BLOCK_SIZE)]
    plaintext = [ int.from_bytes(os.urandom(1), byteorder='big') for _ in range(forkaes.BLOCK_SIZE)]

    left_ct, right_ct = forkaes.encrypt(plaintext, KEY, tweak)

    print("Try to find the key we used to encrypt the following plaintext:")
    print(plaintext)
    print()
    print(f'The tweak we used is:')
    print(tweak)
    print()
    print("The corresponding left and right ciphertexts are:")
    print(f'Left: {left_ct}')
    print(f'Rigth: {right_ct}')
    print()
    while True:
        print(""" 
        MENU:
            1) Compute sibling
            2) Exit
            """)

        choice = input("> ")

        if choice == "1":
            # Below line read inputs from user using map() function
            print(f"The ciphertext and the tweak should be represented as a list of values space separated such as 2 3 4 5 6\nYou can input only {forkaes.BLOCK_SIZE} numbers")
            ciphertext = list(map(int,input("\nEnter the ciphertext : ").strip().split(',')))[:forkaes.BLOCK_SIZE]
            tweak = list(map(int,input("\nEnter the tweak : ").strip().split(',')))[:forkaes.BLOCK_SIZE]
            side_of_the_ciphertext = input("Side of your ciphertext (possible values are: right | left): ")

            if side_of_the_ciphertext != "left" and side_of_the_ciphertext != "right":
                print("Wrong side value!")
                continue
            
            print("The other ciphertexts is: ")
            print(forkaes.compute_sibling(ciphertext, KEY, tweak, side=side_of_the_ciphertext))
            
        elif choice == "2": 
            break




if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    main()