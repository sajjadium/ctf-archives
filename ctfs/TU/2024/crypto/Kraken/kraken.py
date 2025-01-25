import hashlib
import os
import time
import datetime
import struct
import time
import random
import users

class KrakenGuard:
    username = None
    TIMEOUT = 60 * 3
    # Isn't python beautiful
    users = users.users

    help = """
==================================HELP==================================
list                                - Lists users in the system
getmessage <username> <password>    - Gets the user's secret message
setmessage <message>                - Set your secret message
time                                - What time is it?
exit                                - Close the console
========================================================================
"""

    def __init__(self):
        self.prep_generator()
        self.load_users()
    
    def prep_generator(self):
        debug_time = time.time()
        print(debug_time)
        random.seed(int.from_bytes(struct.pack('<d', debug_time), byteorder='little'))

    def load_users(self):
        for user in self.users.keys():
            self.users[user]['session_token'] = self.gen_session_token(user, self.users[user]['password'])
    
    def create_user(self):
        username = ""
        password = ""
        while username == "" or username in self.users.keys() or len(username) > 10:
            username = input("What is your username: ")
        while password == "" or len(password) > 10:
            password = input("What is your password: ")
        self.users[username] = {'session_token': self.gen_session_token(username, password), 'password':password, 'message': ''}
        self.username = username
        time.sleep(1)

    def gen_session_token(self, username:str, password:str):
        return hashlib.md5(username.encode('utf8') + b':' + password.encode('utf8') + b':' + random.randbytes(5)).hexdigest()
    
    def check_identity(self, identity:str):
        byte_array = bytearray.fromhex(identity)
        if byte_array == hashlib.md5(self.admin_key).digest():
            return True
        return False

    def print_time(self):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def parse_command(self, input:str):
        command = input.split(' ')[0]
        args = input.split(' ')[1:]
        if len(input) > 100:
            print("Command is too large!")

        if command == 'help' and len(args) == 0:
            print(self.help)
            return
        if command == 'time' and len(args) == 0:
            self.print_time()
            return
        if command == 'exit' and len(args) == 0:
            print("Goodbye!")
            exit()
        if command == 'getmessage' and len(args) == 2:
            if args[0] not in self.users.keys():
                print('User does not exist!')
                return
            if self.users[args[0]]['password'] != args[1]:
                print("Incorrect password!")
                time.sleep(1)
                return
            print(self.users[args[0]]['message'])
            return
        if command == 'setmessage' and len(args) > 0:
            self.users[self.username]['message'] = input[len(command)+1:]
            print("Message set!")
            return

        if command == 'list' and len(args) == 0:
            print(f"{'USERNAME':<15} {'SESSION TOKEN'}")
            for user in self.users.keys():
                print(f"{user:<15} {self.users[user]['session_token']}")
            return
        print("Invalid command! Type 'help' for help.")

    def run(self):
        print("Kraken Server 1.0")
        self.create_user()

        start_time = time.time()
        while (time.time() < start_time + self.TIMEOUT):
            answer = input("Console $ ")
            self.parse_command(answer)

KrakenGuard().run()