#!/usr/local/bin/python
import random
import base64
import sys
import select

class User:
    def __init__(self, username):
        self.username = username
        self.key = self.get_key()
        self.message = None

    def get_key(self):
        username = self.username
        num_bits = 8 * len(username)
        rand = random.getrandbits(num_bits)
        rand_bits = bin(rand)[2:].zfill(num_bits)
        username_bits = ''.join([bin(ord(char))[2:].zfill(8) for char in username])
        xor_bits = ''.join([str(int(rand_bits[i]) ^ int(username_bits[i])) for i in range(num_bits)])
        xor_result = int(xor_bits, 2)
        shifted = ((xor_result << 3) & (1 << (num_bits + 3)) - 1) ^ 0x5A
        byte_data = shifted.to_bytes((shifted.bit_length() + 7) // 8, 'big')
        key = base64.b64encode(byte_data).decode('utf-8')
        return key
    
    def set_message(self, message):
        self.message = message

def input_with_timeout(prompt="", timeout=10):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.buffer.readline().rstrip(b'\n')
    raise Exception
input = input_with_timeout

flag = open("flag.txt").read()

assert len(flag)%3 == 0
flag_part1 = flag[:len(flag)//3]
flag_part2 = flag[len(flag)//3:2*len(flag)//3]
flag_part3= flag[2*len(flag)//3:]

admin1 = User("Admin001")
admin2 = User("Admin002")
admin3 = User("Admin003")
admin1.set_message(flag_part1)
admin2.set_message(flag_part2)
admin3.set_message(flag_part3)
user_dict = {
    "Admin001": admin1,
    "Admin002": admin2,
    "Admin003": admin3
}

print("Welcome!")
logged_in = None
user_count = 3 
MAX_USERS = 200

while True:
    if logged_in is None:
        print("\n\n[1] Sign-In\n[2] Create Account\n[Q] Quit")
        inp = input().decode('utf-8').strip().lower()
        match inp:
            case "1":
                username = input("Enter your username:  ").decode('utf-8')
                if username in user_dict:
                    user = user_dict[username]
                    key = input("Enter your sign-in key: ").decode('utf-8')
                    if key == user.key:
                        logged_in = user
                        print(f"Logged in as {username}")
                    else:
                        print("Incorrect key. Please try again!")
                else:
                    print("Username not found. Please try again or create an account.")
            case "2":
                if user_count >= MAX_USERS:
                    print("Max number of users reached. Cannot create new account.")
                else:
                    username = input("Select username:  ").decode('utf-8')
                    if username in user_dict:
                        print(f"Username '{username}' is already taken!")
                    else:
                        user_dict[username] = User(username)
                        user_count += 1 
                        print(f"Account successfully created!\nYour sign-in key is: {user_dict[username].key}")
            case "q":
                sys.exit()
            case _:
                print("Invalid option. Please try again.")
    else:
        print(f"Welcome, {logged_in.username}!")
        print("\n\n[1] View Message\n[2] Set Message\n[L] Logout")
        inp = input().decode('utf-8').strip().lower()
        match inp:
            case "1":
                print(f"Your message: {logged_in.message}")
            case "2":
                new_message = input("Enter your new message: ").decode('utf-8')
                logged_in.set_message(new_message)
                print("Message updated successfully.")
            case "l":
                print(f"Logged out from {logged_in.username}.")
                logged_in = None
            case _:
                print("Invalid option. Please try again.")
