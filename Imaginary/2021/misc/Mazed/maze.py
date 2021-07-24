#!/usr/local/bin/python -u

from random import choice
from copy import deepcopy
# https://pypi.org/project/timeout-decorator/
import timeout_decorator

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
        self.set(*self.loc, val='.')
        walls = self.adj(*self.loc)

        while len(walls) > 0:
            rand = choice(list(walls))
            nbhd = self.neighbors(*rand, typ='.')
            if len(nbhd) == 1:
                self.set(*rand, val='.')
                walls = walls | self.neighbors(*rand, typ='#')
            walls = walls - {rand}
        self.set(*([0]*self.dim), val='@')

        self.set(*([self.size-1]*self.dim), val='F')
        for i in self.neighbors(*([self.size-1]*self.dim)):
            self.set(*i, val='.')

    def move(self, s):
        for c in s:
            myloc = list(self.loc)
            moveidx = ord(c.lower())-ord('a')
            myloc[moveidx] += -1+2*(c<'a')
            if self.get(*myloc) == '.':
                self.set(*self.loc, val='.')
                self.set(*myloc, val='@')
                self.loc = tuple(myloc)
            elif self.get(*myloc) == 'F':
                print("Flag:")
                print(open('flag.txt').read())
                exit(0)

@timeout_decorator.timeout(10)
def getinput():
    move = input("Enter your move: ")
    maze.move(move)

def fail():
    print("You failed to find the flag, and are trapped forever.")

if __name__ == '__main__':
    try:
        print("Generating maze...")
        print("Please allow about 90 seconds.")
        import sys; sys.stdout.flush()
        maze = Maze(4, 10)
        print("This is your maze:")
        print(maze)
        print("="*80)
        print()
        print("The above is a 50x50x50 maze. That is to say, it's a hypercube with side length 50.")
        print("You have 10 seconds (minus any time you spend reading!) to find the flag. You are denoted as the '@', and the flag is 'F'.")
        print()
        print("The maze is represented internally as a 5 dimensional list. The 5 dimensions are labelled A, B, C, D, and E, respectively. You will input a string denoting a series of moves. A capital 'A' denotes moving 1 unit in the positive A direction, while a lowercase 'c' denotes moving 1 step in the negative C direction.")
        print()
        print("Good luck!")
        print()
        getinput()
        fail()
    except Exception as e:
        raise
        fail()
