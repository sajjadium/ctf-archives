import os
from Crypto.Util.number import *

def rng():
    m = 1<<48
    a = 25214903917
    b = 11
    s = bytes_to_long(os.urandom(6))
    while True:
        yield (s>>24)%6+1
        s = (a*s+b)%m

r = rng()

cpuPlayers = [0]*6
yourPlayers = [0]*6

def printBoard(cpu, your):
    board = [[] for i in range(100)]
    for i in range(6):
        if cpuPlayers[i]!=None:
            board[cpuPlayers[i]].append("C"+str(i))
        if yourPlayers[i]!=None:
            board[yourPlayers[i]].append("Y"+str(i))
    print(*board)

cpuScore = 0
yourScore = 0

while any(i!=None for i in yourPlayers) and any(i!=None for i in cpuPlayers):
    printBoard(cpuPlayers, yourPlayers)
    #CPU goes first
    x = next(r)-1
    while cpuPlayers[x]==None:
        x = next(r)-1
    cpuPlayers[x]+=next(r)
    for i in range(6):
        if yourPlayers[i]==cpuPlayers[x]:
            yourPlayers[i] = None
    for i in range(6):
        if cpuPlayers[i]!=None and cpuPlayers[i]>=100:
            cpuPlayers[i]=None
            cpuScore+=1
    printBoard(cpuPlayers, yourPlayers)
    #your turn next
    x = int(input())
    assert 0<=x<=5 and yourPlayers[x]!=None
    yourPlayers[x]+=(next(r)-1)%3+1 #player disadvantage
    for i in range(6):
        if yourPlayers[x]==cpuPlayers[i]:
            cpuPlayers[i] = None
    for i in range(6):
        if yourPlayers[i]!=None and yourPlayers[i]>=100:
            yourPlayers[i]=None
            yourScore+=1

cpuScore+=6-cpuPlayers.count(None)
yourScore+=6-yourPlayers.count(None)
if cpuScore==0 and yourScore==6:
    print("Congrats on winning! here's your flag")
    print(os.environ.get("FLAG", "wxmctf{dummy}"))
else:
    print("Not good enough or you lost :/")
