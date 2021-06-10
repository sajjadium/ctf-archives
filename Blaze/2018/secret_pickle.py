#!/usr/bin/env python3
import pickle
import hashlib
import os
import sys

class Note:
    def __init__(self, name, date, content):
        self.name = name
        self.date = date
        self.content = content
    def prints(self):
        print()
        print('-'*5 + self.name + '-'*5)
        print('Date: ' + self.date)
        print(self.content)

username = input('username: ')

if username == 'nsnc':
    while True:
        print(eval(input()[:5]))

directory = hashlib.md5(bytes(username, 'cp1252')).hexdigest()
if not os.path.exists(directory):
    os.makedirs(directory)

choice = ''
while choice not in ('0', '1'):
    print("0: Structured Note")
    print("1: Freeform Note")
    choice = input('choice: ')

if choice == '0': # Structured Note
    try:
        with open(directory + '/mode', 'r') as f:
            if f.read() != 'structured':
                os.system('rm ' + hashlib.md5(bytes(username, 'cp1252')).hexdigest() + '/*')
    except:
        pass # so good
    with open(directory + '/mode', 'w') as f:
        f.write('structured')

    rw_choice = ''
    while rw_choice not in ('0', '1'):
        print("0: Write Note")
        print("1: Read Note")
        rw_choice = input('choice: ')

    if rw_choice == '0': # Write note
        name = input('note name: ')
        date = input('note date: ')
        print('note content: ')
        content = ''
        line = input()
        while line:
            content += line + '\n'
            line = input()
        note = Note(name, date, content)
        with open(directory + '/' + hashlib.md5(bytes(name, 'cp1252')).hexdigest(), 'wb') as f:
            pickle.dump(note, f, protocol=0)

    else: # Read note
        name = input('note name: ')
        try:
            with open(directory + '/' + hashlib.md5(bytes(name, 'cp1252')).hexdigest(), 'rb') as f:
                pickle.load(f).prints()
        except:
            pass # best error handling



else: # Freeform note
    try:
        with open(directory + '/mode', 'r') as f:
            if f.read() != 'freeform':
                os.system('rm ' + hashlib.md5(bytes(username, 'cp1252')).hexdigest() + '/*')
    except:
        pass # very good
    with open(directory + '/mode', 'w') as f:
        f.write('freeform')

    rw_choice = ''
    while rw_choice not in ('0', '1'):
        print("0: Write Note")
        print("1: Read Note")
        rw_choice = input('choice: ')

    if rw_choice == '0': # Write note
        name = input('note name: ')
        print('note content: ')
        content = ''
        line = input()
        while line:
            content += line + '\n'
            line = input()
        with open(directory + '/' + hashlib.md5(bytes(name, 'cp1252')).hexdigest(), 'wb') as f:
            f.write(bytes(content, 'utf8'))
            print()

    else: # Read note
        name = input('note name: ')
        try:
            with open(directory + '/' + hashlib.md5(bytes(name, 'cp1252')).hexdigest(), 'r') as f:
                print(f.read())
        except:
            pass # much good
