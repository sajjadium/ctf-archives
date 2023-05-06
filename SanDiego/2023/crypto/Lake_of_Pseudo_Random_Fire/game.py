#!/bin/python3

from Crypto.Cipher import AES
from os import urandom
import random
import binascii

flag = open("flag.txt", "rb").read()

class PRFGame:
    def __init__(self, mode):
        self.plaintext_ciphertext = {}
        self.key = urandom(16)
        # mode = 1 is pseudorandom, move = 0 is random
        # one of the doors will be in the pseudorandom mode, and the other door will be in random mode
        self.mode = mode
    
    def pseudorandom(self, msg): # pseudorandom function
        msg_comp = bytes(x ^ 0xff for x in msg) # bitwise complement of msg
        cipher = AES.new(self.key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(msg) + cipher.decrypt(msg_comp) # concatenation of cipher.encrypt(msg) and cipher.decrypt(msg_comp)
        return ciphertext
    
    def random(self, msg):
        # random oracle has consistency: if the same plaintext was given to the oracle twice,
        # the random oracle will return the same ciphertext on both queries
        if (msg in self.plaintext_ciphertext):
            return self.plaintext_ciphertext[msg] 
        random_string = urandom(32)
        self.plaintext_ciphertext[msg] = random_string
        return random_string
    
    def oracle(self, msg): # msg is a bytestring that is 16 bytes long
        if (len(msg) != 16):
            return None
        if (self.mode == 0):
            return self.random(msg)
        else: # mode = 1 (pseudorandom oracle)
            return self.pseudorandom(msg)
    
    def guess(self, mode_guess):
        return (self.mode == mode_guess)

doors = """
          ┌---------┐                         ┌---------┐          
          |         |                         |         |          
          |         |                         |         |          
          |         |                         |         |          
          |       O |                         |       O |          
          |         |                         |         |          
          |         |                         |         |          
          └---------┘                         └---------┘          
"""

enter_dialog = "You enter a room. Inside the room are two doors. How do you proceed?" 
options = """1 - Choose left door
2 - Choose right door
3 - Call on Orycull the High Priest
Enter a number: """
options_fail = "Invalid option."
left_dialog = "You walk through the left door..."
right_dialog = "You walk through the right door..."
fail_dialog = "Oh no! You fell straight into the Lake of Pseudo-Random Fire. Better luck next time!"
succeed_dialog = "Phew! You didn't walk into the Lake of Pseudo-Random Fire."
orycull_dialog = "Enter your incantation for Orycull to utter: "
orycull_error_dialog = "Sorry, Orycull only utters 16-byte incantations, in hexspeak."
orycull_response_dialog = """The left door sings: {left_response}
The right door sings: {right_response}"""
orycull_run_out_dialog = "Oh no! Orycull's voice broke! They can't talk anymore for the rest of the quest..."
orycull_remaining_dialog = "Orycull can still speak {n:d} more times."
rooms_remaining_dialog = "There are {n:d} rooms remaining. Onwards..."
win_dialog = """Magnificent! You have braved the 50 rooms. Unfortunately, to your chagrin, the Beacon of True Randomness is in another castle...
Oh well. Here's a consolation prize:"""

def orycull(messages_left, left_game, right_game):
    while True:
        if (messages_left == 0):
            print(orycull_run_out_dialog)
            continue
        hex_message = input(orycull_dialog)
        try:
            message = binascii.unhexlify(hex_message)
        except binascii.Error:
            print(orycull_error_dialog)
            continue
        if (len(message) != 16):
            print(orycull_error_dialog)
            continue
        left_response = binascii.hexlify(left_game.oracle(message)).decode("utf-8")
        right_response = binascii.hexlify(right_game.oracle(message)).decode("utf-8")
        print(orycull_response_dialog.format(left_response=left_response, right_response=right_response))
        print(orycull_remaining_dialog.format(n=(messages_left - 1)))
        return (messages_left - 1)

def main():
    rooms = 50
    messages_left = 100
    while (rooms > 0):
        correct_door = random.getrandbits(1) # 0 is left, 1 is right
        if (correct_door == 0):
            left_game = PRFGame(0) # make the left door emit truly random signals
            right_game = PRFGame(1) # make the right door emit pseudorandom signals
        else:
            left_game = PRFGame(1) # make the left door emit pseudorandom signals
            right_game = PRFGame(0) # make the right door emit truly random signals
        print(doors)
        print(enter_dialog)
        while True:
            decision = input(options)
            match decision:
                case "1": # left door
                    if (left_game.guess(0)):
                        print(succeed_dialog)
                        rooms -= 1
                        print(rooms_remaining_dialog.format(n=rooms))
                        break
                    else:
                        print(fail_dialog)
                        return
                case "2": # right door
                    if (right_game.guess(0)):
                        print(succeed_dialog)
                        rooms -= 1
                        print(rooms_remaining_dialog.format(n=rooms))
                        break
                    else:
                        print(fail_dialog)
                        return
                case "3": # Orycull
                    messages_left = orycull(messages_left, left_game, right_game)
                case other:
                    print(options_fail)
    print(win_dialog)
    print(flag)

if (__name__ == "__main__"):
    main()
