#!/usr/local/bin/python3 -u
import json
import builtins

def choose_cell():
    print("Choose your cell")
    while True:
        inp = input('> ')
        if hasattr(builtins,inp):
            return inp
        print("I don't think that cell would hold you")

def choose_inmate(ok):
    print("Choose your inmate")
    while True:
        inp = input('> ')
        if hasattr(type(ok),inp):
            return inp
        print("No that inmate is in solitary")

def name_registration():
    print("What is your name?")
    while True:
        inp = input('> ')
        try:
            return json.loads(inp)
        except: pass
        print("Is that an alias or...")

def checkin():
    print("How are you doing?")
    allowed = set('~(0)|<')
    while True:
        inp = input('> ')
        if set(inp) <= allowed:
            try:
                print(inp)
                return eval(inp)
            except:
                print('Wow must be rough')
        else:
            print('This may be the wrong jail for you.')

def main():
    print("Welcome to the OK Jail!")
    print("Let's hope you won't be staying long...\n")
    
    ok = checkin()
    name = name_registration()
    inmate = choose_inmate(ok)
    cell = choose_cell()

    jail = f'builtins.{cell}(ok.{inmate}(*{name}))'
    print(jail)
    try:
        eval(jail)
    except:
        print("JAILBREAK DETECTED")
    
    
if __name__ == "__main__":
    main()
