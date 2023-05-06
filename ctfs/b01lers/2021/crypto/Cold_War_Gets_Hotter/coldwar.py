#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad 
import os
import re
import sys

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

IU_MANIFESTO = '''
"Indiana, Our Indiana"

Indiana, our Indiana
Indiana, we're all for you!
We will fight for the cream and crimson
For the glory of old IU
Never daunted, we cannot falter
In the battle, we're tried and true
Indiana, our Indiana,
Indiana we're all for you! I-U!

"Indiana Fight"

Fight for the Cream and Crimson,
Loyal sons of our old I. U.
Fight for your Alma Mater,
and the school you love so true.
Fight for old Indiana,
See her victories safely through,
GO! I.U! FIGHT! FIGHT! FIGHT!
For the glory of old I. U.!
'''

MESSAGE_HEADER = '''
WARNING WARNING WARNING WARNING
MISSILE IN FLIGHT
TARGET: Purdue Memorial Union
WARNING WARNING WARNING WARNING
'''

MENU_OPTIONS = '''
Missile Options:
1 - give coordinates to launch missile
2 - alter target coordinates for missile in flight
3 - explode missile in mid flight
4 - exit
> '''

TARGET_LATITUDE = b'???'
TARGET_LONGITUDE = b'???'
KEY = open(os.path.join(BASE_DIRECTORY, 'key'), 'rb').read()
FLAG = open(os.path.join(BASE_DIRECTORY, 'flag.txt'), 'r').read()


def decrypt_message(ciphertext):
    if len(ciphertext) < 64 or len(ciphertext) % 16 != 0:
        return b''
    
    iv = bytes.fromhex(ciphertext[:32])
    cipher = AES.new(KEY, AES.MODE_CBC, iv=iv)
    return cipher.decrypt(bytes.fromhex(ciphertext[32:]))


def validate_new_coordinates(new_coordinates):
    r = re.compile(b'([-]?[\d]*\.[\d],[-]?[\d]*\.[\d])')
    result = r.search(new_coordinates)

    if result is None:
        return False

    match = result.group()
    latitude, longitude = match.split(b',')

    if latitude == TARGET_LATITUDE and longitude == TARGET_LONGITUDE:
        return True

    return False    


def launch_missle():
    sys.stdout.write('\nMissile has already been launched!!\n')


def change_target():
    encrypted = input('\nInput encrypted coordinate message:').strip()
    decrypted = decrypt_message(encrypted)
    if validate_new_coordinates(decrypted):
        sys.stdout.write('\nCoordinates altered to IU Memorial Union')
        sys.stdout.write('\n' + FLAG + '\n')
    else:
        sys.stdout.write('\nCoordinates have not been altered\n')


def decommission_missile():
    encrypted = input('\nInput encrypted decommission message:').strip()
    decrypted = decrypt_message(encrypted)
    if decrypted == IU_MANIFESTO:
        sys.stdout.write('\nWho would dare betray us!!')

    sys.stdout.write('\nYou are not of the cream and crimson!!')


def receive_message():
    sys.stdout.write(MESSAGE_HEADER)
    while 1:
        message_choice = input(MENU_OPTIONS)
        if message_choice == '1':
            launch_missle()
        elif message_choice == '2':    
            change_target()
        elif message_choice == '3':
            decommission_missile()
        else:
            break


receive_message()

