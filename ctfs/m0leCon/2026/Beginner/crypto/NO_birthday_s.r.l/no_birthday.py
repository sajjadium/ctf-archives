#! /usr/bin/env python3

import os
import hashlib
from functools import reduce
from secret import *

assert FLAG is not None
assert FLAG.startswith("ptm{")
assert FLAG.endswith("}")

db = {(1, 'admin', 1002319200)}

banner = """
===========================================================
=                                                         =
=                  NO birthday s.r.l                      =
=                                                         =
===========================================================
"""


menu = """
1) Iscriviti
2) Controlla compleanno
0) Esci
"""

def get_birthday(bd: int) -> bytes:
    h = hashlib.sha3_256(bd.to_bytes(8, 'little')).digest()
    l = [int.from_bytes(h[i: i+8], 'big') for i in range(0, len(h), 8)]
    return reduce(lambda x, y: x ^ y, l).to_bytes(8, 'big')[:7]

def enroll():
    print("Iscriviti")
    name = input("Nome: ")
    birthday = input("Inserisci il tuo compleanno (timestamp unix): ")
    for (_, n, b) in db:
        if n == name or b == int(birthday): raise Exception("Non possono esistere due persone con lo stesso nome o compleanno!")
    db.add((len(db) + 1, name, int(birthday)))
    print(f"Utente {name} iscritto con successo!")

def check():
    print("Stai sfidando il nostro amministratore!?")
    print("Ti concede solo una possibilità per dimostrargli che ha torto...")

    name1 = input("Nome del primo dipendente: ")
    name2 = input("Nome del secondo dipendente: ")

    user1 = next(((i, n, b) for (i, n, b) in db if n == name1), None)
    user2 = next(((i, n, b) for (i, n, b) in db if n == name2), None)

    if not user1 or not user2:
        raise Exception("Uno dei due utenti non esiste!")
    if user1[0] == user2[0]:
        print("Hai provato a barare, il nostro amministratore non è stupido!")
        exit(0)
    if get_birthday(user1[2]) == get_birthday(user2[2]): # Guarda, io il codice lo metto, anche se non raggiungibile ~ admin
        print("Non è possibile! Il nostro amministratore ha sbagliato!")
        print(f"Ecco la flag: {FLAG}")

        if user1[1][0] == 0:
            super_secret_function() 
        exit(0)
    print("Mi dispiace, ma il nostro amministratore aveva ragione.")
    exit(0)

if __name__ == '__main__':
    print(banner)
    print("Il nostro amministratore è convinto che ogni persona abbia diritto a un compleanno sicuro.")
    print("È talmente certo, che è disposto a rivelare il suo segreto alla coppia di dipendenti che sia nata nello stesso esatto momento!")
    print("")

    while True:
        try:
            print(menu)
            choice = input("> ")
            if choice == "1":
                enroll()
            elif choice == "2":
                check()
            elif choice == "0":
                print("Arrivederci!")
                exit(0)
        except Exception as e:
            print("Bzz! Bzz! Bzz!")
            exit(0)