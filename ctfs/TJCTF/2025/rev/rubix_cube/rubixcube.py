import copy
import random
import numpy as np

class RubiksCube:
    def __init__(self):
        self.faces = {
            'U': [['⬜'] * 3 for _ in range(3)],
            'L': [['🟧'] * 3 for _ in range(3)],
            'F': [['🟩'] * 3 for _ in range(3)],
            'R': [['🟥'] * 3 for _ in range(3)],
            'B': [['🟦'] * 3 for _ in range(3)],
            'D': [['🟨'] * 3 for _ in range(3)]
        }

    def _rotate_face_clockwise(self, face_name):

        face = self.faces[face_name]

        new_face = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_face[i][j] = face[2-j][i]
        self.faces[face_name] = new_face

    def _rotate_face_counter_clockwise(self, face_name):

        face = self.faces[face_name]

        new_face = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_face[i][j] = face[j][2-i]
        self.faces[face_name] = new_face

    def display(self):
        for i in range(3):
            print("      " + " ".join(self.faces['U'][i]))
        for i in range(3):
            print(" ".join(self.faces['L'][i]) + "  " +
                  " ".join(self.faces['F'][i]) + "  " +
                  " ".join(self.faces['R'][i]) + "  " +
                  " ".join(self.faces['B'][i]))
        for i in range(3):
            print("      " + " ".join(self.faces['D'][i]))
        print("-" * 30)

    def get_flat_cube_encoded(self):
        return "".join([chr(ord(i) % 94 + 33) for i in str(list(np.array(self.faces).flatten())) if ord(i)>256])
    
    def get_cube(self):
        return self.faces
    
    def U(self):
        self._rotate_face_clockwise('U')
        temp_row = copy.deepcopy(self.faces['F'][0])
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = temp_row

    def L(self):
        self._rotate_face_clockwise('L')
        temp_col = [self.faces['U'][i][0] for i in range(3)]
        for i in range(3): self.faces['U'][i][0] = self.faces['B'][2-i][2]
        for i in range(3): self.faces['B'][2-i][2] = self.faces['D'][i][0]
        for i in range(3): self.faces['D'][i][0] = self.faces['F'][i][0]
        for i in range(3): self.faces['F'][i][0] = temp_col[i]

    def F(self):
        self._rotate_face_clockwise('F')
        temp_strip = copy.deepcopy(self.faces['U'][2])
        for i in range(3): self.faces['U'][2][i] = self.faces['L'][2-i][2]
        for i in range(3): self.faces['L'][i][2] = self.faces['D'][0][i]
        for i in range(3): self.faces['D'][0][2-i] = self.faces['R'][i][0]
        for i in range(3): self.faces['R'][i][0] = temp_strip[i]

    def D_prime(self):
        self._rotate_face_counter_clockwise('D')
        temp_row = copy.deepcopy(self.faces['F'][2])
        self.faces['F'][2] = self.faces['R'][2]
        self.faces['R'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['L'][2]
        self.faces['L'][2] = temp_row

    def R_prime(self):
        self._rotate_face_counter_clockwise('R')
        temp_col = [self.faces['U'][i][2] for i in range(3)]
        for i in range(3): self.faces['U'][i][2] = self.faces['B'][2-i][0]
        for i in range(3): self.faces['B'][2-i][0] = self.faces['D'][i][2]
        for i in range(3): self.faces['D'][i][2] = self.faces['F'][i][2]
        for i in range(3): self.faces['F'][i][2] = temp_col[i]

    def B_prime(self):
        self._rotate_face_counter_clockwise('B')
        temp_strip = copy.deepcopy(self.faces['U'][0])
        for i in range(3): self.faces['U'][0][i] = self.faces['L'][i][0]
        for i in range(3): self.faces['L'][i][0] = self.faces['D'][2][2-i]
        for i in range(3): self.faces['D'][2][i] = self.faces['R'][i][2]
        for i in range(3): self.faces['R'][i][2] = temp_strip[2-i]

    def apply_moves(self, moves_string):
        moves = moves_string.split()
        for move in moves:
            if move == "U": self.U()
            elif move == "D'": self.D_prime()
            elif move == "L": self.L()
            elif move == "R'": self.R_prime()
            elif move == "F": self.F()
            elif move == "B'": self.B_prime()
            else:
                print(f"Warning: Unknown move '{move}' ignored.")
    

moves = ["U", "L", "F", "B'", "D'", "R'"]

cube = RubiksCube()

#random scramble
for _ in range(1000):
    cube.apply_moves(moves[random.randint(0,len(moves)-1)])

flag = "tjctf{" + cube.get_flat_cube_encoded() + "}"

first = cube.get_flat_cube_encoded()

with open("flag.txt", "w",  encoding="utf-8") as f: f.write(flag)

random.seed(42)

for _ in range(20):
    order = [random.randint(0,len(moves)-1) for _ in range(50)]

    for i in range(len(order)):
        cube.apply_moves(moves[order[i]])
        
with open("cube_scrambled.txt", "w", encoding="utf-8") as f: f.write(str(cube.get_cube()))
