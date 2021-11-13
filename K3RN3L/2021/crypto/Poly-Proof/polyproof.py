#!/usr/bin/env python3
#
# Polymero
#

# Imports
import os

# Local imports
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

HDR = r"""|
|    ________  ________  ___           ___    ___      ________  ________  ________  ________  ________ 
|   |\   __  \|\   __  \|\  \         |\  \  /  /|    |\   __  \|\   __  \|\   __  \|\   __  \|\  _____\
|   \ \  \|\  \ \  \|\  \ \  \        \ \  \/  / /    \ \  \|\  \ \  \|\  \ \  \|\  \ \  \|\  \ \  \__/ 
|    \ \   ____\ \  \\\  \ \  \        \ \    / /      \ \   ____\ \   _  _\ \  \\\  \ \  \\\  \ \   __\
|     \ \  \___|\ \  \\\  \ \  \____    \/  /  /        \ \  \___|\ \  \\  \\ \  \\\  \ \  \\\  \ \  \_|
|      \ \__\    \ \_______\ \_______\__/  / /           \ \__\    \ \__\\ _\\ \_______\ \_______\ \__\ 
|       \|__|     \|_______|\|_______|\___/ /             \|__|     \|__|\|__|\|_______|\|_______|\|__| 
|                                    \|___|/                                
|"""

class Server:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.coefficients = None
        self.limit = 8
        self.i = 0
        self.set_up()
        
    def _eval_poly(self, x):
        return sum([ self.coefficients[i] * x**i for i in range(len(self.coefficients)) ])
    
    def _prod(self, intlst):
        ret = 1
        for i in intlst:
            ret *= i
        return ret
        
    def set_up(self, verbose=False):
        print(HDR)
        print("|  To prove to you that I own the flag, I used it to make a polynomial. Challenge me all you want!")
        noise = [ self._prod(list(os.urandom(self.difficulty))) for i in range(len(FLAG)) ]
        self.coefficients = [ noise[i] * FLAG[i] for i in range(len(FLAG)) ]
        
    def accept_challenge(self):
        print("|\n|  Name your challenge (as ASCII string):")
        try:
            user_input = int.from_bytes(str(input("|   >> ")).encode(),'big')
        except ValueError:
            print("|\n|  ERROR - That ain't working... s m h ")
            return
        if user_input == 0:
            print("|\n|  ERROR - You clearly don't know what ZERO-KNOWLEDGE means eh?")
            return
        if user_input <= 0:
            print("|\n|  ERROR - Your clever tricks will not work here, understood?")
            return
        print("|\n|  Here's my commitment: {}".format(self._eval_poly(user_input)))
        self.i += 1
        
    def run(self):
        while self.i < self.limit:
            try:
                self.accept_challenge()
            except:
                break
        if self.i >= self.limit:
            print("|\n|   Are you trying to steal my polynomial or something?")
            print("|   I think I have proven enough to you...")
        print("|\n|\n|  ~ See you back in polynomial time! o/ \n|")


S = Server(15)
S.run()
