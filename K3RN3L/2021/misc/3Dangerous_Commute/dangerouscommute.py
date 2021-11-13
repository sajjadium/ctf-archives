#!/usr/bin/env python3
#
# Polymero
#

# Imports
import numpy as np
import random

# Local imports
from Private import Private

PRIVATE = Private()

class HyperSpace3D:
    def __init__(self, dim=(21,21,81), difficulty_level=6):
        """ Initialise the HyperSpace3D object. """
        self.dim = dim
        self.difficulty = (dim[0]*dim[1]*dim[2]) // difficulty_level
        self.alp = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        print('Downloading most recent 3D-HyperSpace zone map...\n')
        tick = 0
        while True:
            print('Ticker: ' + '#'*tick, end='\r', flush=True)
            self.minemap = self.deploy_mines()
            self.zonemap = self.chart_zones()
            if PRIVATE.validify_zonemap(self.zonemap, verbose=False):
                print('Zone map succesfully downloaded and verified!'+' '*16)
                break
            tick += 1
        
    def get_danger(self, x, y, z):
        """ Calculate the danger of zone at location (x,y,z). """
        ret = []
        for k in [z-1, z, z+1]:
            for j in [y-1, y, y+1]:
                for i in [x-1, x, x+1]:
                    if k in range(self.dim[0]) and j in range(self.dim[1]) and i in range(self.dim[2]):
                        if [i,j,k] != [x,y,z]:
                            ret += [self.minemap[k][j][i]]
        return sum([1 if i == '#' else 0 for i in ret])
        
    def deploy_mines(self):
        """ Fill the HyperSpace with randomly placed mines. """
        zones = [[['.' for _ in range(self.dim[2])] for _ in range(self.dim[1])] for _ in range(self.dim[0])]
        mines = []
        while len(mines) < self.difficulty:
            rndpos = [random.choice(range(self.dim[0])), random.choice(range(self.dim[1])), random.choice(range(self.dim[2]))]
            if rndpos not in mines:
                mines += [rndpos]
        for mine in mines:
            zones[mine[0]][mine[1]][mine[2]] = '#'
        zones[0][0][0] = '.'
        zones[self.dim[0]-1][self.dim[1]-1][self.dim[2]-1] = '.'
        return zones
    
    def chart_zones(self):
        """ Chart the HyperSpace zones using their danger levels. """
        return [[[self.alp[self.get_danger(i,j,k)] for i in range(self.dim[2])] for j in range(self.dim[1])] for k in range(self.dim[0])]
    
    def check_route(self, movestr):
        """ Check validity and danger cost of given move string. """
        if not all( i in 'XxYyZz' for i in list(movestr) ):
            return False,'INPUT ERROR -- Invalid move string.'
        move_dic = {
            'X' : [ 0,  0,  1],
            'x' : [ 0,  0, -1],
            'Y' : [ 0,  1,  0],
            'y' : [ 0, -1,  0],
            'Z' : [ 1,  0,  0],
            'z' : [-1,  0,  0]
        }
        path = [[0,0,0]]
        for move in list(movestr):
            path += [[path[-1][j] + move_dic[move][j] for j in range(3)]]
        if '#' in [self.minemap[i[0]][i[1]][i[2]] for i in path]:
            return False,'SURVIVAL ERROR -- You died.'
        if path[-1] != [self.dim[0]-1,self.dim[1]-1,self.dim[2]-1]:
            return False, 'TRAVEL ERROR -- You have not reached your destination.'
        cost = sum([self.alp.index(self.zonemap[i[0]][i[1]][i[2]]) for i in path])
        return True, cost
    
    def check_win(self, movestr):
        """ Check win condition of given move string. """
        valid, cost = self.check_route(movestr)
        if not valid:
            print(cost)
            return
        assert valid
        print('You survived with a total danger of {}!'.format(cost))
        mincost, minpath = PRIVATE.solve_MCP(self.zonemap, self.minemap)
        if mincost == cost:
            print('CHALL END -- Congratulations with your new job. ^w^')
            print('\nTake my flag, {}'.format(PRIVATE.flag))
        elif mincost > cost:
            print('You... you beat me? HOW?!?!')
            print('Just take my flag... \n{}'.format(PRIVATE.flag))
        else:
            print('PUNCTUALITY ERROR -- You may have survived, but you were late for your job interview. :c')



print("""
+--------------------   CHALLENGE   --------------------+
|                                                       |
|      After some time in workforce-hibernation (aka    |
|   unemployed), you have received an offer for a job   |
|   interview. There is just one problem, it is at      |
|   the other end of the Universe! Luckily you know     |
|   your way around the HyperSpace, *ehem* nerd *mm*.   |
|                                                       |
|      Keep in mind, as of recent the HyperSpace has    |
|   danger zones you must avoid at all cost! To help    |
|   you find a way through, we will supply you with     |
|   the most recent zone map. The map displays the      |
|   danger level of each and every known zone. This     |
|   tells you the number of surrounding danger zones.   |
|                                                       |
|      Find the least dangerous* path from (0,0,0) to   |
|   (6,6,76) without crossing any of the danger         |
|   zones. If you can manage to survive your daily      |
|   commute, the new job at Hyperspatial Engineering    |
|   is surely yours!                                    |
|                                                       |
|      *least dangerous = lowest sum of danger level    |
|   along your commute route.                           |
|                                                       |
|                      DISCLAIMER                       |
|                                                       |
|      HYPERSPATIAL ENGINEERING IS IN NO WAY LEGALLY    |
|   RESPONSIBLE FOR ANY HARM OR DAMAGE CAUSED DURING    |
|   COMMUTES TO AND FROM OUR PROPERTY.                  |
|                                                       |
+-------------------------------------------------------+
""")

hs = HyperSpace3D((7,7,77), difficulty_level=8)

_ = input('\nPress enter to continue...')

print('\nHere is your up-to-date HyperSpace zone map:\n')

for mat in hs.zonemap:
    for row in mat:
        print(''.join(row))
    print()

print('Format: "X" is a move towards the positive x-direction and "x" towards the negative x-direction, etc.')
user_solution = input(' >>  ')

print()
hs.check_win(user_solution)
