#! /usr/bin/python3


from random import randint

def and_encr(key):
    mess = [randint(32, 127) for x in range(0,len(key))]
    return "".join([hex(ord(k) & m)[2:].zfill(2) for (k,m) in zip(key, mess)])
    
flag = 'fake-flag'

while True:
    while True:
        choise = input("1. Прислать шифр\n2. Проверить флаг\nВаш выбор: ")
        if choise in ['1','2']:
            break
    if choise == '1':
        print (and_encr(flag))
    else:
        if flag == input("Flag: "):
            print (f"Правильно !\nВаш флаг: {flag})
            break
        else:
            print (f"Ошибка, сэр !")
            break