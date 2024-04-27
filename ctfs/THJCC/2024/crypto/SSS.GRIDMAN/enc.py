import numpy
import random
import os
from FLAG import FLAG

poly_enc = []

def random_ploy():
    poly=[]
    for i in range(2):
        poly.append(random.randint(99,999))

    return poly


def random_x():
    random_list=[i for i in range(100,999)]
    x_list=[]
    for i in range(3):
        choice=random.choice(random_list)
        x_list.append(choice)
        random_list.remove(choice)
    return x_list

def encrypt_secret(poly,x_list):
    share_list=[]
    
    for x in x_list:
        
        share=(x,int(poly(x)))
        share_list.append(share)

    print('share:',share_list)

try:
    WELCOME='''
   ________________ ________  _______  __  ______   _  
  / __/ __/ __// ___/ _ \/  _/ _ \/  |/  / _ | / |/ /
 _\ \_\ \_\ \_/ (_ / , _// // // / /|_/ / __ |/    / 
/___/___/___(_)___/_/|_/___/____/_/  /_/_/ |_/_/|_/  

    '''
    print(WELCOME)
    print("I don't remember anything.But one day, I looks a word \"GRIDMAN\".\nI want to know what is \"GRIDMAN\"")
    print("I find this computer.It may have secret about \"GRIDMAN\"")
    secret=os.urandom(4)
    secret=int.from_bytes(secret, byteorder='big')

    polyc =random_ploy()

    polyc.append(secret)
    poly_enc = numpy.poly1d(polyc)
    print("-"*20)

    
    encrypt_secret(poly_enc,random_x())
    print("Do you know PASSWORD?")
    print("-"*20)
    input_secret_num=int(input("PASSWORD? "))

    if input_secret_num==secret:
        print("This is SECRET")
        print(FLAG)
    else:
        print("end...")
        exit()

except:
    print("error...")
    exit()