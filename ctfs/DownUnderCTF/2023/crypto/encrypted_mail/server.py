#!/usr/bin/env python3

from collections import defaultdict
import os, time, re

from db import Database
from bot_users import Bots
from crypto import Authenticator, Encryptor, p


def menu():
    print('[R]egister')
    print('[L]ogin')
    print('[S]end message')
    print('[V]iew inbox')
    return input('> ')[0].lower()


def register(db):
    username = input('Username: ')
    if db.user_exists(username):
        print('User already exists with that username!')
        return
    if not re.fullmatch(r'[a-zA-Z0-9]{8,16}', username):
        print('Invalid username!')
        return
    pubkey = int(input('Public key: '))
    if not (1 < pubkey < p - 1):
        print('Invalid public key!')
        return
    db.add_user(username, pubkey)
    print('Registration successful!')


def login(db):
    username = input('Username: ')
    if not db.user_exists(username):
        print('Unknown user!')
        return
    auth = Authenticator(db.get_user_pubkey(username))
    challenges = auth.generate_challenges()
    print(challenges)
    answers = list(map(int, input('Answers: ').split()))
    if not auth.verify_answers(answers):
        print('Authentication failed!')
        return
    print('Login successful!')
    db.set_current_user(username)


def send_message(db):
    user = db.get_current_user()
    if user is None:
        print('Log in first!')
        return
    recipient = input('Recipient user: ')
    if not db.user_exists(recipient):
        print('Unknown recipient!')
        return
    print('Recipient public key:', db.get_user_pubkey(recipient))
    msg_enc = bytes.fromhex(input('Encrypted message: '))
    sig = list(map(int, input('Signature: ').split()))
    if len(sig) != 2:
        print('Invalid signature!')
        return
    db.add_message(user, recipient, msg_enc, sig)
    print('Message sent!')


def view_inbox(db):
    user = db.get_current_user()
    if user is None:
        print('Log in first!')
        return
    inbox = db.get_inbox(user)
    if len(inbox) == 0:
        print('Inbox is empty!')
    else:
        print(f'You have {len(inbox)} messages!')
        for i, (sender, timestamp, msg_enc, sig) in enumerate(inbox):
            print(f'Message #{i+1} from {sender} at {timestamp}')
            print(msg_enc.hex())
            print(sig)
            print()


def main():
    db = Database()
    bots = Bots(db)
    bots.setup()
    while True:
        choice = menu()
        { 'r': register, 'l': login, 's': send_message, 'v': view_inbox }[choice](db)
        bots.perform_bot_user_actions()


if __name__ == '__main__':
    main()
