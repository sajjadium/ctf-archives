#!/usr/bin/env python3

from random import choice
from copy import deepcopy
# https://pypi.org/project/console/
from console.utils import wait_key

class Maze:
    def __init__(self, dim, size):
        self.dim = dim
        self.size = size
        self.maze = '#'
        self.loc = tuple([0]*dim)
        for i in range(dim):
            self.maze = [deepcopy(self.maze) for _ in range(size)]
        self.gen()

    def __str__(self):
        if type(self.maze[0]) == str:
            return ''.join(self.maze)+'\n'
        ret = ''
        for i in self.maze:
            temp = deepcopy(self)
            temp.dim -= 1
            temp.maze = i
            ret += str(temp)
        ret += "\n"
        return ret

    @staticmethod
    def fromstr(s):
        dim = 0
        for i in s[-max(len(s), 50):][::-1]:
            if i == '\n':
                dim += 1
            else:
                break
        size = 0
        for i in s[:max(len(s), 50):]:
            if i == '\n':
                break
            size += 1

        ret = Maze(2, 2)
        ret.maze = Maze.fromstrhelp(s, dim, size)
        ret.dim = dim
        ret.size = size
        ret.loc = tuple([0]*dim)
        return ret

    @staticmethod
    def fromstrhelp(s, dim, size):
        s = s.strip()
        if dim == 1:
            return list(s)
        return [Maze.fromstrhelp(i+'\n'*(dim-1), dim-1, size) for i in s.split('\n'*(dim-1))]


    def get(self, *pt):
        ret = self.maze
        for idx in pt:
            ret = ret[idx]
        return ret

    def set(self, *pt, **kwargs):
        temp = self.maze
        for idx in pt[:-1]:
            temp = temp[idx]
        temp[pt[-1]] = kwargs['val']

    def check(self, *pt):
        for i in pt:
            if i >=self.size or i < 0:
                return False
        return True

    def adj(self, *pt):
        ret = set()
        for i in range(len(pt)):
            newpt = [i for i in pt]
            newpt[i] += 1
            if self.check(*newpt):
                ret = ret | {tuple(newpt)}
            newpt[i] -= 2
            if self.check(*newpt):
                ret = ret | {tuple(newpt)}
        return ret

    def neighbors(self, *pt, typ=None):
        ret = set()
        for pt in self.adj(*pt):
            if typ is None or self.get(*pt) in typ:
                ret = ret | {pt}
        return ret

    def gen(self):
        self.set(*self.loc, val=' ')
        walls = self.adj(*self.loc)

        while len(walls) > 0:
            rand = choice(list(walls))
            nbhd = self.neighbors(*rand, typ=' ')
            if len(nbhd) == 1:
                self.set(*rand, val=' ')
                walls = walls | self.neighbors(*rand, typ='#')
            walls = walls - {rand}

        self.set(*([0]*self.dim), val='@')
        for i in self.neighbors(*([0]*self.dim)):
            self.set(*i, val=' ')

        self.set(*([self.size-1]*self.dim), val='F')
        for i in self.neighbors(*([self.size-1]*self.dim)):
            self.set(*i, val=' ')

    def move(self, mv):
        newLoc = (self.loc[0] + mv[0], self.loc[1] + mv[1])
        if (
            newLoc[0] < 0 or newLoc[0] >= self.size or
            newLoc[1] < 0 or newLoc[1] >= self.size or
            self.get(*newLoc) == '#'
        ):
            print("BONK")
            return
        if self.get(*newLoc) == 'F':
            print(open("flag.txt").read())
            wait_key()
            exit(0)
        self.set(*self.loc, val=' ')
        self.set(*newLoc, val='@')
        self.loc = newLoc

def getKey():
    key = wait_key()
    if key == chr(3): # Ctrl-C
        exit(1)
    return key

moveDict = {
    'w': (-1, 0),
    's': (1, 0),
    'd': (0, 1),
    'a': (0, -1),
}

def waitForMove():
    key = None
    while key not in moveDict:
        key = getKey()

    return moveDict[key]
    

def main():
    maze = Maze(2, 40)
    print("Find the flag in this maze. Good luck!")
    print("WASD to move.")
    while True:
        # print(maze)
        move = waitForMove()
        maze.move(move)

if __name__ == '__main__':
    main()

