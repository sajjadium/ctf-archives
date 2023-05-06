#!/usr/bin/env python3

# Imports
import os

# Local imports
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

HDR = r"""|
|
|           15                           26
|             \  17    18     19    20  /
|    14   16   \ |     |       |     | /   21   25
|      \  |     \|     |       |     |/     |  /
|       \ |      |_____|       |_____|      | /
|   13   \|      /     \       /     \      |/   24
|     \   |_____/       \_____/       \_____|   /
|      \  /     \       /     \       /     \  /
|       \/       \_____/       \_____/       \/
|   12   \       /     \       /     \       /   23
|     \   \_____/       \_____/       \_____/   /
|      \  /     \       /     \       /     \  /
|       \/       \_____/       \_____/       \/
|   11  /\       /     \       /     \       /\  22
|     \/  \_____/       \_____/       \_____/  \/
|     /\  /     \       /     \       /     \  /\
|   10  \/       \_____/       \_____/       \/  31
|       /\       /     \       /     \       /\
|      /  \_____/       \_____/       \_____/  \
|     /   /     \       /     \       /     \   \
|    9   /       \_____/       \_____/       \   30
|       /\       /     \       /     \       /\
|      /  \_____/       \_____/       \_____/  \
|     /   |     \       /     \       /     |   \
|    8   /|      \_____/       \_____/      |\   29
|       / |      |     |       |     |      | \
|      /  |     /|     |       |     |\     |  \
|     7   0    / |     |       |     | \    5   28
|             /  1     2       3     4  \   
|            6                           27
|"""

# Encryption
class PandorasComb:
    def __init__(self,key_62):
        if type(key_62) == str:
            key_62 = bytes.fromhex(key_62)
        self.key = key_62
        key_62 = list(key_62)
        self.state = [[' ']+key_62[:9]+[' '],key_62[9:20],key_62[20:31],
                       key_62[31:42],key_62[42:53],[' ']+key_62[53:]+[' ']]
        
    def shoot(self, indir, ray, verbose=False):
        shoot_dic = {
            0  : [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9]],
            1  : [[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10]],
            2  : [[2,0],[2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10]],
            3  : [[3,0],[3,1],[3,2],[3,3],[3,4],[3,5],[3,6],[3,7],[3,8],[3,9],[3,10]],
            4  : [[4,0],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[4,7],[4,8],[4,9],[4,10]],
            5  : [[5,1],[5,2],[5,3],[5,4],[5,5],[5,6],[5,7],[5,8],[5,9]],
            6  : [[1,0],[2,0],[2,1],[3,1],[3,2],[4,2],[4,3],[5,3],[5,4]],
            7  : [[0,1],[1,1],[1,2],[2,2],[2,3],[3,3],[3,4],[4,4],[4,5],[5,5],[5,6]],
            8  : [[0,2],[0,3],[1,3],[1,4],[2,4],[2,5],[3,5],[3,6],[4,6],[4,7],[5,7],[5,8]],
            9  : [[0,4],[0,5],[1,5],[1,6],[2,6],[2,7],[3,7],[3,8],[4,8],[4,9],[5,9]],
            10 : [[0,6],[0,7],[1,7],[1,8],[2,8],[2,9],[3,9],[3,10],[4,10]],
            11 : [[0,4],[0,3],[1,3],[1,2],[2,2],[2,1],[3,1],[3,0],[4,0]],
            12 : [[0,6],[0,5],[1,5],[1,4],[2,4],[2,3],[3,3],[3,2],[4,2],[4,1],[5,1]],
            13 : [[0,8],[0,7],[1,7],[1,6],[2,6],[2,5],[3,5],[3,4],[4,4],[4,3],[5,3],[5,2]],
            14 : [[0,9],[1,9],[1,8],[2,8],[2,7],[3,7],[3,6],[4,6],[4,5],[5,5],[5,4]],
            15 : [[1,10],[2,10],[2,9],[3,9],[3,8],[4,8],[4,7],[5,7],[5,6]]
        }
        if indir > 15:
            indir %= 16
            path = shoot_dic[indir]
            for i in range(len(shoot_dic[indir])):
                ray ^= self.state[path[-(i+1)][0]][path[-(i+1)][1]]
                self.state[path[-(i+1)][0]][path[-(i+1)][1]] = ray
        else:
            path = shoot_dic[indir]
            for i in range(len(path)):
                ray ^= self.state[path[i][0]][path[i][1]]
                self.state[path[i][0]][path[i][1]] = ray
        if verbose:
            print(self.state)
        return ray
    
def __main__():

    try:

        PB = PandorasComb(os.urandom(62))
        print('|\n|\n|  "Here, this is that Comb I was talking about..."')
        print(HDR)
        print('|\n|\n|  "It seems any byte-ray we send in, interacts with the vertices of the Comb."')
        print('|  "At every vertex, the ray XORs itself with the internal state of the Comb at said vertex."')
        print('|  "So, we have new_state = new_ray = ray ^ state."')
        print('|\n|   "The numbers in the schematic represent the directions from which we can shoot our bytes through the Comb."')

        while True:
            print('|\n|\n|  "What shall we do with it?"')
            print('|')
            print('|   [1] Send a byte')
            print('|   [2] Press the button')
            print('|   [3] Shake the Comb (angrily)')
            print('|   [4] Run away')

            pick = input("|\n|  >> ")

            if pick == '1':
                print('|\n|\n|  "What do you want to send and where?" - (direction, byte) e.g. (1, 255)')
                send = input("|\n|  >> ")
                try:
                    recv = send.replace('(','').replace(')','').replace(' ','').split(',')
                    print('|\n|  And out comes:', PB.shoot(int(recv[0]),int(recv[1])))
                except:
                    print('|\n|  "Sorry I don\'t understand that..."')
                    continue

            elif pick == '2':
                    print('|\n|\n|  "Alright, here goes nothing..."\n|')
                    for i,byt in enumerate(FLAG):
                        indir = int(os.urandom(1)[0]/256*6)
                        print('|   ({}, {})'.format(indir, PB.shoot(indir, byt)))

            elif pick == '3':
                print("|\n|\n|  After some shaking, the Comb buzzes lightly. Hearing it fills you with Determination.")
                print("|  Its inner state has been randomised.")
                PB = PandorasComb(os.urandom(62))

            elif pick == '4':
                print("|\n|  You can't run away from Trainer Battles!")

            elif pick in ['exit','quit','leave']:
                print('\n|\n|  "Are you just gonna leave me with it?"\n|\n|')
                break

            else:
                print('|\n|  "I can\'t do that!?"\n|')
                continue

    except KeyboardInterrupt:
        print('\n|\n|  "Are you just gonna leave me with it?"\n|\n|')

    except:
        print('|')
        print('|  *BOOOOOM !!!*')
        print('|')
        print('|  "Hey.. hey! What have you done to my box!?"')
        print('|')
        print('|  "Get out you!"')
        print('|')
        
    
__main__()
