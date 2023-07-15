#!/usr/local/bin/python
from Crypto.Util.number import *
from os import urandom
from flag import flag

class lcg:
    def __init__(self, p):
        while (a:=bytes_to_long(urandom(16))) > p:
            pass
        while (b:=bytes_to_long(urandom(16))) > p:
            pass
        self.a, self.b, self.p = a, b, p
    
    seed = 1337

    def gen_next(self):
        self.seed = (self.a*self.seed + self.b) % self.p
        return self.seed

class order:
    def __init__(self, p):
        self.p = p

        self.inner_lcg = lcg(p)
    
        for i in range(1337):
            self.inner_lcg.gen_next()

        self.flavors = [self.inner_lcg.gen_next() for i in range(1338)]

        self.flavor_map = {i:self.flavors[i] for i in [1,2,3,4,5,6]}
        self.private = {i:self.flavors[i] for i in [1,2,3,4,5,6,1337]}
    
    bowls = [0, 0, 0]
    used = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    recipe = []

    def make_bowl(self):
        global flavor_indices
        self.bowls = [0, 0, 0]
        self.recipe = []
        new = {}
        available = []
        for i, n in self.used.items():
            if n == 0:
                new[i] = 0
                available += [i]
        self.used = new
        print("\nREMAINING FLAVORS: ")
        for i in available:
            print(f"Flavor {i} - {flavor_indices[i]}")
        while True:
            command = input("\nAdd, combine, or finish? ")
            if command.lower() == "add":
                try:
                    add = input("\nGive a flavor and a bowl: ").rsplit(" ", 1)
                    self.add(*add)
                except Exception as e:
                    print()
                    print(e)
            elif command.lower() == "combine":
                try:
                    combination = input("\nGive two bowls and an operation: ").split()
                    assert len(combination) == 3, "Invalid Input Length"
                    self.combine_bowl(*combination)
                except Exception as e:
                    print()
                    print(e)
            elif command.lower() == "finish bowl":
                self.finish_bowl()
            elif command.lower() == "finish":
                self.finish()
                break
            elif command.lower() == "exit":
                exit(1)
            else:
                print("\nPlease give a valid input.")
            

    def mod(self):
        self.bowls = [i % self.p for i in self.bowls]

    def add(self, flavor, bowl):
        assert "0" < bowl < "4", "Invalid Bowl"
        bowl = int(bowl) - 1
        global flavor_names
        if flavor not in ["1", "2", "3", "4", "5", "6"]:
            try:
                if self.used[flavor_names[flavor]] < 5:
                    self.bowls[bowl] += self.flavor_map[flavor_names[flavor]]
                    self.used[flavor_names[flavor]] += 1
                    self.recipe += [[flavor_names[flavor], bowl]]
                else:
                    print(f"\nCannot order {flavor} due to stock issues.")
            except:
                print("\nInvalid Flavor")
        else:
            try:
                flavor = int(flavor)
                if self.used[flavor] < 5:
                    self.bowls[bowl] += self.flavor_map[flavor]
                    self.used[flavor] += 1
                    self.recipe += [[flavor, bowl]]
                else:
                    print(f"\nCannot order {flavor} due to stock issues.")
            except:
                print("\nInvalid Flavor")
    
    def combine_bowl(self, a, b, op):
        assert op in ['add', 'sub', 'mult', 'div'], "Invalid Operation. Please choose either 'add', 'sub', 'mult', or 'div'."
        assert "0" < a < "4" and "0" < b < "4" and a != b, "Invalid Bowl"
        a = int(a) - 1
        b = int(b) - 1
        if op == 'add':
            self.bowls[a] += self.bowls[b]
        elif op == 'sub':
            self.bowls[a] -= self.bowls[b]
        elif op == 'mult':
            self.bowls[a] *= self.bowls[b]
        elif op == 'div':
            assert self.bowls[b] != 0, "Empty Bowl for Division"
            self.bowls[a] *= pow(self.bowls[b], -1, self.p)
        else:
            print("\nwtf")
            exit(1)
        self.recipe += [[op, a, b]]
        self.bowls[b] = 0
        self.mod()
    
    def finish_bowl(self):
        unique = 0
        for i, n in self.used.items():
            if n and n != 1337:
                unique += 1
        if unique < min(3, len(self.used)):
            print("\nAdd more flavor!")
            return False
        recipe = str(self.recipe).replace(' ', '')
        signature = sum(self.bowls) % self.p
        self.bowls = [0, 0, 0]
        self.recipe = []
        for i in self.used:
            if self.used[i]:
                self.used[i] = 1337
        print(f"\nUser #: {self.p}")
        print(f"\nRecipe: \n{recipe}")
        print(f"\n\nSignature: \n{signature}")
        return True
    
    def finish(self):
        if sum(self.bowls):
            if not self.finish_bowl():
                print("\nOk the bowls will be dumped.")
        print("\nOrder done!")
        return True

    def verify(self, recipe, signature):
        bowls = [0, 0, 0]
        for i in recipe:
            try:
                if len(i) == 2:
                    bowls[i[1]] += self.private[i[0]]
                elif len(i) == 3:
                    if i[0] == 'add':
                        bowls[i[1]] += bowls[i[2]]
                    elif i[0] == 'sub':
                        bowls[i[1]] -= bowls[i[2]]
                    elif i[0] == 'mult':
                        bowls[i[1]] *= bowls[i[2]]
                    elif i[0] == 'div':
                        bowls[i[1]] *= pow(bowls[i[2]], -1, self.p)
                    bowls[i[2]] = 0
                bowls = [i % self.p for i in bowls]
            except:
                exit("\nInvalid Recipe")
        try:
            assert sum(bowls) % self.p == signature, "\nInvalid Signature"
            print("\nYou have successfully redeemed your lce cream!")
            if signature == self.private[1337]:
                print(flag)
        except Exception as e:
            print(e)
        

flavor_names = {"revanilla":1, "cryptolatte":2, "pwnstachio":3, "strawebrry":4, "miscnt":5, "cookie dalgo":6, "flaudge chocolate":1337}
flavor_indices = {i:n for n, i in flavor_names.items()}

intro = \
"""
----------------------------------------------------
            WELCOME TO THE LCE CREAM SHOP!          
----------------------------------------------------
  HERE AT THE LCE CREAM SHOP WE HAVE A FEW BELIEFS  

 1. Don't be boring! Choose at least 3 flavors of lce cream. All of it tastes the same anyways...
 2. Don't be repetitive! Well... that and the fact that we have some stock issues. After getting one lce cream with one flavor, you don't get to choose that flavor again.
 3. Since I rolled my own signature system that is extremely secure, if you can manage to forge an arbitrary flavor, I'll give it to you! As long as it exists...
 4. These aren't really beliefs anymore but we only have 6 flavors (available to the customer), and you're only allowed to order once (stock issues again smh). Choose wisely!
 5. To help with the boringness, I will allow you to mix flavors in any way you want. But you can only use up to 5 scoops of each flavor to concoct your lce cream (once again stock issues).
 6. I AM ONLY ACCEPTING ONE RECIEPT. If the first fails, too bad.
 7. I heard there's a special flavor called "flaudge chocolate", it's like the 1337th flavor or something.
 8. Orders can have multiple lce cream mixtures, as long as they follow the rules above.
 9. I am accepting reciepts for TAX PURPOSES only.
10. Each scoop costs $5 (stock issues AGAIN).
11. The reciept itself costs $1.
12. Everything is free. Have fun!
13. Zero indexing sucks. Here at LCE CREAM SHOP we use one indexing.

Oh yeah here are the options:"""

options = \
"""
OPTIONS:
(1) Generate order
(2) View flavors
(3) Redeem a reciept
(4) Exit
Choice: """

print(intro)

while True:
    choice = input(options)
    if choice == "1":
        if 'user' in vars():
            print("\nYou already ordered.")
            continue
        user = order(getPrime(128))
        user.make_bowl()
        print()
    elif choice == "2":
        print("\nThe only valid flavors are: ")
        [print(f"Flavor {i} - {n}") for i, n in flavor_indices.items() if i != 1337]
    elif choice == "3":
        if 'user' not in vars():
            print("\nNo user.")
        else:
            userid = int(input("\nENTER NUMBER: "))
            assert userid == user.p, "You seem to have lost your reciept."
            recipe = input("\nENTER RECIPE: ")
            assert all([i in "[,]01234567abdilmstuv'" for i in recipe]), "\n\nSir, please don't put junk in my lce cream machine!"
            recipe = eval(recipe, {"__builtins__": {}}, {"__builtins__": {}}) # screw json or ast.literal_eval
            signature = input("\nENTER SIGNATURE: ")
            user.verify(recipe, int(signature))
            exit("\nGoodbye.")
    elif choice == "4":
        exit("\nGoodbye.")
    else:
        print("\nINVALID CHOICE. Please input '1', '2', '3', or '4'")
