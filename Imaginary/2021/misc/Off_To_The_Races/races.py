#!/usr/bin/env python3

import re
import time
from random import choice
from multiprocessing import Process, Value

balance = 0
bets = {}

rx = re.compile(r'ju(5)tn((([E3e])(v\4))+\4\5)+rl0\1\4')

def menu():
    print("1) Place Bet")
    print("2) Login as Admin")
    print()
    inp = input(">>> ")
    if '1' in inp:
        bet()
    elif '2' in inp:
        login()
    else:
        print("Invalid input!")

def flag():
    if admin.value:
        print("Admins aren't allowed to view the flag!")
        return
    if balance >= 100:
        print(open("flag.txt").read())
        exit(0)
    else:
        print("Insufficient balance!")

def bet():
    global bets
    name = input("What horse would you like to bet on? ")
    val = input("How much would you like to bet? ")
    if val.isdigit():
        bets[name] = int(val)
    else:
        print("Invalid bet!")

def admin_menu():
    print("1) Declare winner")
    print("2) View balance")
    print("3) Buy flag for $100")
    print("4) Logout")
    print()
    inp = input(">>> ")
    if '1' in inp: 
        declareWinner()
    elif '2' in inp:
        print("Balance:", balance)
    elif '3' in inp:
        flag()
    elif '4' in inp:
        login()
    else:
        print("Invalid input!")

def declareWinner():
    global balance, bets
    if len(bets) == 0:
        print("No bets placed!")
        return
    winner = choice(list(bets))
    print("%s is the big winner!"%winner)
    for i in bets:
        balance -= bets[i]*(-1+2*(winner==i))
    bets = {}

def login():
    pwd = input("Enter admin password (empty to logout): ")
    if len(pwd) == 0:
        print("Logging out...")
        admin = 0
        return
    print("Validating...")
    Process(None, checkPass, None, args=(pwd,)).start()
    time.sleep(2)

def checkPass(pwd):
    valid = rx.match(pwd)
    if valid:
        print("Login success!")
        print("Redirecting...")
        admin.value = 1
    else:
        print("Login failure!")
        print("Redirecting...")
        admin.value = 0

def main():
    while True:
        print()
        print('='*80)
        if admin.value:
            admin_menu()
        else:
            menu()

if __name__ == '__main__':
    admin = Value('i', 0)
    main()