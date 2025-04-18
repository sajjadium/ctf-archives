#!/usr/local/bin/python3
from Crypto.Util.number import *
from secret import flag, init, N, a, b

seed = init
state = seed

current_user = (None, None)

accounts = []
notes = dict()

menu1 = '''[1] - Register
[2] - Login
[3] - Manage Notes
[4] - List Users
[5] - Exit 
'''

menu2 = '''[1] - Register
[2] - Logout
[3] - Manage Notes
[4] - List Users
[5] - Exit 
'''
menu3 = '''[1] - Add Note
[2] - Remove Note
[3] - Return to Menu
'''

def getNext(state):
    state = (a * state + b) % N
    return state
    
def make_account(name, password):
    global accounts
    global notes
    accounts.append((name, password))
    notes[name] = []

def register(name):
    for account in accounts:
        if name == account[0]:
            print("An account with this name already exists")
            raise ValueError(f"User '{name}' already exists. Please choose a different username")
    global state
    state = getNext(state)
    make_account(name, state)
    
    return state

def list_users():
    print("Here are all list of all users currently registered.")
    for i in range(len(accounts)):
        print("Account [" + str(i) + "] - ", accounts[i][0])
    
def login(name, password):
    for account in accounts:
        if account[0] == name and str(account[1]) == str(password):
            global current_user
            current_user = account
            print()
            print(f"Succesfully Logged in as {current_user[0]}")
            return
    print("Invalid username or password")    

def logout():
    global current_user
    current_user = (None, None)
    
def get_menu_choice(minimum, maximum, prompt, input_func=input):
    choice = ""
    while(True):
        choice = input_func(prompt)
        try:
            choice = int(choice)
            if (choice < minimum or choice > maximum):
                print("Invalid Choice. Try again")
            break
        except:
            print("Error parsing your input. Try again")
    return choice

def view_notes(user):
    print(f"Here are the notes for user '{user}'")
    current_notes = notes[user]
    if (len(current_notes) == 0):
        print("This user currently has no notes!")
        return
    i = 1
    for value in current_notes:
        print(f"Note {i}: {value}")
        i += 1
    return

def add_note(user, message):
    if (len(message) == 0):
        print("Can't add note with an empty message")
        return
    current_notes = notes[user]
    current_notes.append(message)
    notes[user] = current_notes
    return

def remove_note(user, index):
    current_notes = notes[user]
    del current_notes[index]
    return

def is_logged_in():
    global current_user
    if (current_user[0] == None and current_user[1] == None):
        return False
    return True

def handle_note(user, input_func=input):
    global notes
    view_notes(user)
    print()
    while(True):
        print(menu3)
        choice = get_menu_choice(1, 3, "> ")
        if choice == 1:
            msg = input_func("What message do you want to save? ")
            add_note(user, msg)
            break
        elif choice == 2:
            num_notes = len(notes[user])
            if num_notes == 0:
                print("This user currently has no notes to remove.")
            else:
                note_choice = get_menu_choice(1, num_notes, f"Which note do you want to remove? (1 - {num_notes}) ")
                remove_note(user, note_choice - 1)
                break
        elif choice == 3:
            break
def initAdmin():
    register("admin")
    add_note("admin", flag)
    
        
def run(input_func=input):
    global notes
    global accounts
    initAdmin()
    print("Welcome to the state of the art secure note taking app, Global Content Library . You can make accounts, see active users, store and view private information. Everything you can ask for. You can rest well knowing your password is securely generated, just make sure you don't lose it. That's the only way to access your account!")
    while(True):
        print()
        if is_logged_in():
            print(menu2)
        else:
            print(menu1)
        choice = get_menu_choice(1, 5, "> ")
        if choice == 1: # Register
            name = input_func("Enter your name: ")
            try:
                password = register(name)
            except:
                continue
            print("Your secret password is: ", password, "\nPlease don't lose it!!")
        if choice == 2:
            if (current_user[0] == None and current_user[1] == None):
                name = input_func("Enter your name: ")
                password = input_func("Enter your password: ")
                login(name, password)
            else:
                logout()               
        if choice == 3:
            if (current_user[0] == None):
                print("You must be logged in to use this feature")
            else:
                handle_note(current_user[0])
        if choice == 4:
            list_users()
        if choice == 5:#Exit
            print("See you later!")
            exit()
                
if __name__ == '__main__':
    run()
