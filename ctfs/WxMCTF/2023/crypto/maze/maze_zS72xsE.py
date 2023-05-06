#!/usr/local/bin/python3
from random import getrandbits 
from hashlib import sha256
from console.utils import wait_key
from console.screen import Screen


class PRNG:
    def __init__(self, seed):
        self.state = seed
        self.mul = 25214903917
        self.add = 11
        self.mod = 1 << 48

    def next(self):
        self.state = (self.mul * self.state + self.add) % self.mod
        return (self.state >> 17) % 6





def generateMaze(seed):
    maze = []
    prng = PRNG(seed)
    for _ in range(144):
        maze.append(prng.next())
    maze = [maze[i:i + 12] for i in range(0, 144, 12)]
    for i in range(12):
        for j in range(12):
            if maze[i][j]:
                maze[i][j] = "0"
            else:
                maze[i][j] = " "
    maze[0][0] = "@"
    maze[11][11] = "X"
    return maze


SOLID = '╔║╗╚═╝0'


def draw():
    global screen, playerX, playerY
    print(screen.clear, end='')
    with screen.location(0, 0):
        print('╔' + '═' * 12 + '╗')
    for y in range(12):
        with screen.location(y + 1, 0):
            print('║' + ''.join(maze[y]) + '║')
    with screen.location(13, 0):
        print('╚' + '═' * 12 + '╝')


def processInput(key):
    global playerY, playerX
    if key in 'A':

        if playerY != 0 and maze[playerY - 1][playerX] != "0":
            maze[playerY][playerX] = " "
            maze[playerY - 1][playerX] = "@"
            playerY -= 1
    elif key in 'B':
        if playerY != 11 and maze[playerY + 1][playerX] != "0":
            maze[playerY][playerX] = " "
            maze[playerY + 1][playerX] = "@"
            playerY += 1
    elif key in 'C':
        if playerX != 11 and maze[playerY][playerX + 1] != "0":
            maze[playerY][playerX] = " "
            maze[playerY][playerX + 1] = "@"
            playerX += 1
    elif key in 'D':
        if playerX != 0 and maze[playerY][playerX - 1] != "0":
            maze[playerY][playerX] = " "
            maze[playerY][playerX - 1] = "@"
            playerX -= 1
    elif key in chr(3):
        print("Ctrl-C")
        exit()

def win():
    global screen
    draw()
    with screen.location(15, 0):
        print("Congratulations! "+open("flag.txt").read())
    with screen.location(17, 0):
        print("Press any key to exit...")
    wait_key()
    exit(0)


def playMaze(seeds):
    global screen, maze
    maze = generateMaze(seeds)
    with screen.fullscreen():
        while True:
            draw()
            key = wait_key()
            processInput(key)
            if playerX == 11 and playerY == 11:
                win()


screen = None
playerX = 0
playerY = 0
maze = None

def pow():
    val = hex(getrandbits(24))[2:]
    print("Give me a string containing only printable characters whose SHA256 hash ends in " + val.rjust(6, '0') + ".")
    s = input()
    if not (s.isprintable() and sha256(s.encode()).hexdigest().endswith(val)):
        print("Incorrect or your string was not printable")
        exit()
        
#Super jank pow solver but for those who are too lazy to make their own here you go
def solvepow(s):
    import random
    from hashlib import sha256
    a = random.randint(0, 1<<256)
    while True:
        if sha256(hex(a).encode()).hexdigest().endswith(s):
            return hex(a)
            break
        a+=1

def main():
    print("Give me your seed!")
    seed = int(input())
    print("Ready?")
    input()
    playMaze(seed)


if __name__=='__main__':
    pow()
    with Screen(force=True) as screen:
        main() 
