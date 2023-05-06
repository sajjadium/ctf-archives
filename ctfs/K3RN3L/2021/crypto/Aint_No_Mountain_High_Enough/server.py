#!/usr/bin/env python3
#
# Polymero
#

# Local imports
from mountaincipher import *

with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

# Encryption parameters
N = 5
P = 251
VERSION = '1.0'

HDR_3 = r"""|
|
|         ___ ___ ___        _________                                          _        
|       /   /   /   /\      (_________)                           _            (_)       
|      /___/___/___/  \      _   _   _    ___    _   _   ____   _| |_   _____   _   ____  
|     /   /   /   /\  /\    | | |_| | |  / _ \  | | | | |  _ \ (_   _) (____ | | | |  _ \ 
|    /___/___/___/  \/  \   | |     | | | |_| | | |_| | | | | |  | |_  / ___ | | | | | | |
|   /   /   /   /\  /\  /\  |_|     |_|  \___/  |____/  |_| |_|   \__) \_____| |_| |_| |_|
|  /___/___/___/  \/  \/  \ 
|  \   \   \   \  /\  /\  /  _______   _           _                   
|   \___\___\___\/  \/  \/  (_______) (_)         | |       
|    \   \   \   \  /\  /    _         _   ____   | |__    _____    ____
|     \___\___\___\/  \/    | |       | | |  _ \  |  _ \  | ___ |  / ___)
|      \   \   \   \  /     | |_____  | | | |_| | | | | | | ____| | | 
|       \___\___\___\/       \______) |_| |  __/  |_| |_| |_____) |_|  
|                                         |_| 
|"""

CUBE = r"""|
|
|                                     Key Cube (5x5x5)
|                                    ___ ___ ___ ___ ___           
|                                  /   /   /   /   /   /\          
|                                 /___/___/___/___/___/  \         
|                                /   /   /   /   /   /\  /\        
|                               /___/___/___/___/___/  \/  \       
|                              /   /   /   /   /   /\  /\  /\      
|                             /___/___/___/___/___/  \/  \/  \     
|                            /   /   /   /   /   /\  /\  /\  /\    
|                           /___/___/___/___/___/  \/  \/  \/  \   
|                          /   /   /   /   /   /\  /\  /\  /\  /\  
|   Message Cuboid --->   /___/___/___/___/___/  \/  \/  \/  \/  \   ---> Cipher Cuboid
|                         \   \   \   \   \   \  /\  /\  /\  /\  /       
|                          \___\___\___\___\___\/  \/  \/  \/  \/                   
|                           \   \   \   \   \   \  /\  /\  /\  /   
|                            \___\___\___\___\___\/  \/  \/  \/    
|                             \   \   \   \   \   \  /\  /\  /    
|                              \___\___\___\___\___\/  \/  \/     
|                               \   \   \   \   \   \  /\  /      
|                                \___\___\___\___\___\/  \/        
|                                 \   \   \   \   \   \  /         
|                                  \___\___\___\___\___\/     
|                                    |   |   |   |   |    
|                                    |   |   |   |   |
|                                    |   |   |   |   |
|                  Current slices:   {}  {}  {}  {}  {}
|"""

# Server
def __main__():

    KEYS = ['K1','K2','K3','K4','K5']

    KEYCUBE, _ = keygen(N, P)
    K1, K2, K3, K4, K5 = KEYCUBE[::1]
    FL = [list(FLAG[i:i+N]) for i in range(0,N*N,N)]

    print(HDR_3)
    print('|\n|  Welcome to the Mountain Cipher Encryption Service!\n|')
    print('|    Current version: {} (Insert Challenge)\n|'.format(VERSION))

    while True:

        try:
            
            print('|')
            print('|  MENU:\n|   [0] Show info\n|   [1] Inspect key cube\n|   [2] Insert FLAG slice\n|\n|   [3] Encrypt\n|   [4] Decrypt\n|\n|   [5] Exit')


            choice_1 = input('|\n|  >> ')

            if choice_1 == '0':
                print('|\n|\n|  Mountain Cipher Encryption Service (MCES) v{}'.format(VERSION))
                print('|\n|    "Hills are easy to climb, but mountains? Hoho, they sure are something else!"')
                print('|\n|  KEY CUBE\n|   Dimensions (n): {0}x{0}x{0}\n|   Prime Modulus (p): {1}\n|\n|  CIPHER TEXT\n|   Matrix Output: True\n|   Hex Output: True'.format(N,P))
                print('|\n|  Challenge: recover the FLAG by inserting it into the KEY CUBE.\n|')
            elif choice_1 == '1':
                
                print(CUBE.format(KEYS[0],KEYS[1],KEYS[2],KEYS[3],KEYS[4]))


            elif choice_1 == '2':
                
                print("|\n|\n|  Current setup: {}".format(KEYS))
                print("|\n|  Swap KEY slice 'X' for FLAG slice (0 for None):")

                choice_2 = input('|\n|  >> X = ')

                if choice_2 == '0':
                    KEYS = ['K1','K2','K3','K4','K5']
                    KEYCUBE = [K1,K2,K3,K4,K5]
                elif choice_2 == '5':
                    KEYS = ['K1','K2','K3','K4','FL']
                    KEYCUBE = [K1,K2,K3,K4,FL]
                elif choice_2 == '4':
                    KEYS = ['K1','K2','K3','FL','K5']
                    KEYCUBE = [K1,K2,K3,FL,K5]
                elif choice_2 == '3':
                    KEYS = ['K1','K2','FL','K4','K5']
                    KEYCUBE = [K1,K2,FL,K4,K5]
                elif choice_2 == '2':
                    KEYS = ['K1','FL','K3','K4','K5']
                    KEYCUBE = [K1,FL,K3,K4,K5]
                elif choice_2 == '1':
                    KEYS = ['FL','K2','K3','K4','K5']
                    KEYCUBE = [FL,K2,K3,K4,K5]

                print('|\n|  Current setup: {}\n|'.format(KEYS))


            elif choice_1 == '3':
                
                print('|\n|\n|  Please enter ASCII message to encrypt (check [1] for key cube setup):')

                msg_to_enc = input('|  >> M = ')

                enc_msg = encMC(msg_to_enc, N, P, key=KEYCUBE)

                print('|\n|\n|  Key Cube: {}'.format(KEYS))

                print('|\n|  Cipher Cuboid:')
                for block in enc_msg:
                    for row in block:
                        print('|   [{:3d}, {:3d}, {:3d}, {:3d}, {:3d}]'.format(row[0],row[1],row[2],row[3],row[4]))
                    print('|')
                print('|')

                print('|  C = {}'.format(bytes([i for j in [i for j in enc_msg for i in j] for i in j]).hex()))
                print('|')


            elif choice_1 == '4':

                print('|\n|\n|  Please enter HEX cipher text to decrypt (check [1] for key cube setup):')

                cip_to_dec = input('|  >> C = ')

                dec_msg = decMC(cip_to_dec, N, P, key=KEYCUBE)

                print('|\n|\n|  Key Cube: {}'.format(KEYS))

                print('|\n|  Message Cuboid:')
                for block in dec_msg:
                    for row in block:
                        print('|   [{:3d}, {:3d}, {:3d}, {:3d}, {:3d}]'.format(row[0],row[1],row[2],row[3],row[4]))
                    print('|')
                print('|')

                print('|  M(hex) = {}'.format(bytes([i for j in [i for j in dec_msg for i in j] for i in j]).hex()))
                print('|')
                print('|  M(bytes) = {}'.format(bytes([i for j in [i for j in dec_msg for i in j] for i in j])))
                print('|')


            elif choice_1 in ['5','q','quit','exit']:
                raise KeyboardInterrupt


            else:

                print('|\n|  Option not recognised\n|')


        except KeyboardInterrupt:
            print('|\n|\n|  Goodbye!\n|')
            break

        except:
            break

__main__()