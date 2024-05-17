import tkinter

global root, myCanvas
root = tkinter.Tk()
myCanvas = tkinter.Canvas(root, bg="white", height=320, width=320)
turn = 0

grid = [0]*64
def selectWhite():
    global turn
    turn = 1
    L3.config(text="Filling white")
def selectBlack():
    global turn
    turn = 0
    L3.config(text="Filling black")


def verify():
    b0 = int(''.join(str(i) for i in grid[0:8]), 2)
    b1 = int(''.join(str(i) for i in grid[8:16]), 2)
    b2 = int(''.join(str(i) for i in grid[16:24]), 2)
    b3 = int(''.join(str(i) for i in grid[24:32]), 2)
    b4 = int(''.join(str(i) for i in grid[32:40]), 2)
    b5 = int(''.join(str(i) for i in grid[40:48]), 2)
    b6 = int(''.join(str(i) for i in grid[48:56]), 2)
    b7 = int(''.join(str(i) for i in grid[56:64]), 2)
    b8 = int(''.join(str(i) for i in grid[0:64:8]), 2)
    b9 = int(''.join(str(i) for i in grid[1:64:8]), 2)
    b10 = int(''.join(str(i) for i in grid[2:64:8]), 2)
    b11 = int(''.join(str(i) for i in grid[3:64:8]), 2)
    b12 = int(''.join(str(i) for i in grid[4:64:8]), 2)
    b13 = int(''.join(str(i) for i in grid[5:64:8]), 2)
    b14 = int(''.join(str(i) for i in grid[6:64:8]), 2)
    b15 = int(''.join(str(i) for i in grid[7:64:8]), 2)
    b16 = int(''.join(str(i) for i in grid[0:64:9]), 2)
    b17 = int(''.join(str(i) for i in grid[7:63:7]), 2)


    touchesgrass = True

    touchesgrass &= grid[1]+grid[10]+grid[62] == 2
    touchesgrass &= (grid[15] > grid[23])
    touchesgrass &= grid[9]+grid[10]+grid[14] == 2
    touchesgrass &= grid[26] << 3 == grid[43]+grid[44]
    touchesgrass &= (grid[32]+grid[33] < grid[1] + grid[62])
    touchesgrass &= (sum(int(i)==int(j) for i,j in [*zip(format(b2,"#010b"),format(b4,"#010b"))][2:]))==3
    touchesgrass &= bin(b6).count('1') == 5
    touchesgrass &= grid[61] + grid[42] + grid[43] == grid[25] + grid[26] + grid[27]
    touchesgrass &= grid[38]+grid[46]+grid[54]+grid[62]+grid[39]+grid[47]+grid[55]+grid[63] == 5
    touchesgrass &= (grid[14]^1!=grid[15])
    touchesgrass &= grid[57] + grid[59] + grid[60] == 3
    touchesgrass &= grid[18] != grid[23]
    touchesgrass &= grid[11]^grid[19]==1
    touchesgrass &= grid[50]==grid[51]
    touchesgrass &= grid[20]^grid[7]==1
    touchesgrass &= (grid[63]>>1 != grid[63]<<1)
    touchesgrass &= (sum(int(i)!=int(j) for i,j in [*zip(format(b9,"#010b"),format(b1,"#010b"))][2:]))==2
    touchesgrass &= grid[57] + grid[58] + grid[59] == 2
    touchesgrass &= grid[37]|grid[38] == grid[2]
    touchesgrass &= grid[4]==grid[48]==grid[49]
    touchesgrass &= grid[17] >=grid[30]
    touchesgrass &= (grid[0] == grid[19])
    touchesgrass &= grid[26] + grid[28] + grid[29] == grid[51] << 1
    touchesgrass &= grid[3] + grid[5] + grid[55] == 1
    touchesgrass &= (grid[30]==grid[34])
    touchesgrass &= sum(grid[14:17]) > grid[56] + grid[30] + grid[47]
    touchesgrass &= grid[7]!=grid[52]
    touchesgrass &= (b16//4)%2==0
    touchesgrass &= grid[8] == grid[9]
    touchesgrass &= (sum(int(i)!=int(j) for i,j in [*zip(format(b16,"#010b"),format(b15,"#010b"))][2:]))==3
    touchesgrass &= grid[6]^grid[56]==0
    touchesgrass &= (sum(grid[30:36])==3)
    touchesgrass &= grid[24]+grid[40] == grid[2]
    touchesgrass &= ~(grid[27]^grid[22])==-1
    touchesgrass &= grid[11]^grid[12]^grid[13]==grid[12]==grid[4]
    touchesgrass &= grid[31] == grid[47]
    touchesgrass &= grid[47]^grid[46] == 1
    touchesgrass &= grid[10] * 2 == grid[25] * 2 + grid[41]

    if(touchesgrass): 
        return 'tjctf{'+chr(b2)+chr(b9)+chr(b15)+chr(b16)+chr(b7)+chr(b4)+chr(b10)+chr(b12)+'}'
    else:
        return touchesgrass

def clicked(event):
    row = max(0,min(320,event.y))//40
    col = max(0,min(320,event.x))//40
    grid[row*8+col] = turn
    myCanvas.create_oval(40*col+5, 40*row+5, 40*(col+1)-5, 40*(row+1)-5, fill=("white" if turn==1 else "black"))
    L2.config(text=f"{'Black wins' if grid.count(0)>grid.count(1) else 'White wins' if grid.count(0)<grid.count(1) else 'Tie' } {grid.count(0)}-{grid.count(1)}")
    if((thefunny:=verify())):
        print("yay you're a winner")
        print(thefunny)
        # exit()

def makeCanvas(root, myCanvas):
    global L2, L3
    L1 = tkinter.Label(root, text="Othello endgame generator")
    L1.config(font=("Courier",20))
    L1.pack()
    btn = tkinter.Button(root, text="Fill black", height=25, bd='5',command=selectBlack)
    btn.pack(side='left')
    btn = tkinter.Button(root, text="Fill white", height=25, bd='5',command=selectWhite)
    btn.pack(side='right')

    for r in range(0,8):
        for c in range(0,8):
            myCanvas.create_rectangle(r*40, c*40, (r+1)*40, (c+1)*40, fill='green')
            myCanvas.create_oval(40*r+5, 40*c+5, 40*(r+1)-5, 40*(c+1)-5, fill="black")
    myCanvas.bind("<Button-1>", clicked)
    myCanvas.pack()
    L2= tkinter.Label(root, text="Black wins 64-0")
    L2.config(font=("Courier",20))
    L2.pack()
    L3= tkinter.Label(root, text="Filling black")
    L3.config(font=("Courier",20))
    L3.pack()
makeCanvas(root, myCanvas)
root.mainloop()
