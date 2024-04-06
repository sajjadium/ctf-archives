server_map = open('out.txt').read()
player_map = open('player.txt').read()
w, l, server_map = server_map.split("/")
w2, l2, player_map = player_map.split("/")
assert w == w2 and l == l2 and len(server_map) == len(player_map)
w, l = int(w), int(l)

grid = [[] for i in range(l)]
for i in range(len(server_map)//2):
    idx = slice(2*i, 2*i+2)
    server, player = server_map[idx], player_map[idx]
    if server == "^0":
        assert player_map[2*i:2*i+2] in [";3", "$0"]
    else:
        assert player == server
    grid[i//w].append(player)

def neighs(r,c):
    return sum(grid[r-1+i//3][c-1+i%3] == "$0" for i in range(9))

qq = {"$0": "S", ";3": " ", "g0": "."}

for i in range(l):
    for j in range(w):
        if grid[i][j] == ";3" and neighs(i,j) == 1:
            grid[i][j] = "$0"

if grid[-4][-4] == "$0":
    bitstring = ""
    for i in range(len(server_map)//2): # shut up i know it's inefficient, deal with it.
        idx = slice(2*i, 2*i+2)
        if server_map[idx] == "^0":
            bitstring += str([";3", "$0"].index(player_map[idx]))
    print("Correct! Your flag is amateursCTF{" + bytes.fromhex(hex(int(bitstring, 2))[2:]).decode() + "}")
