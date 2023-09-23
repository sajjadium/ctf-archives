"""
CREDIT: https://github.com/java-abhinav07/Befunge93_Interpreter
"""
import random


class Stack:

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, data):
        self.items.append(data)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return 0

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def get_stack(self):
        return self.items

    def duplicate(self):
        if not self.is_empty():
            self.push(self.items[-1])
        else:
            self.push(0)

    def swap(self):
        if not self.is_empty():
            if len(self.items) > 1:
                num_0 = self.pop()
                num_1 = self.pop()
                self.push(num_0)
                self.push(num_1)
            elif len(self.items) == 1:
                num = self.pop()
                self.push(num)
                self.push(0)


def math_op(a, b, current):
    operations = {
        '+': a + b,
        '-': b - a,
        '/': b // a if a != 0 else 0,
        '%': b % a if a != 0 else 0,
        '*': a * b
    }

    return operations[current]


def befunge(code, max_moves=100):

    code = code.split('\n')
    directions = {">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}
    math = ['+', '-', '/', "*", "%"]
    logical = ["`", "!"]
    conditional = ["_", "|"]

    strmode = False

    length = len(code)
    width = len(code[0])

    current = code[0][0]
    coordinates = [0, 0]
    move = (0, 1)
    Stk = Stack()

    moves = 0  # please don't break my interpreter T-T
    while moves <= max_moves and (current != '@' or strmode):
        if strmode:
            if current == '"':
                strmode = False
            else:
                Stk.push(ord(current))
        else:

            if current.isdigit():
                Stk.push(int(current))

            elif current in math:
                Stk.push(math_op(Stk.pop(), Stk.pop(), current))

            elif current in logical:
                if current == '!':
                    Stk.push(int(Stk.pop == 0))
                elif current == '`':
                    num_0 = Stk.pop()
                    num_1 = Stk.pop()
                    Stk.push(int(num_1 > num_0))

            elif current in conditional:
                if current == '_':
                    val = Stk.pop()
                    if val == 0:
                        move = (0, 1)
                    else:
                        move = (0, -1)
                elif current == '|':
                    val = Stk.pop()
                    if val == 0:
                        move = (-1, 0)
                    else:
                        move = (1, 0)

            elif current in directions:
                move = directions.get(current)

            elif current == '?':
                move = random.choice([(0, 1), (1, 0), (-1, 0), (0, -1)])
            elif current == ':':
                Stk.duplicate()
            elif current == '$':
                Stk.pop()
            elif current == '.':
                num = Stk.pop()
                if num:
                    print(num, end="")
            elif current == ',':
                letter = Stk.pop()
                if letter:
                    print(chr(letter), end="")
            elif current == '#':
                move = (2 * move[0], 2 * move[1])
            elif current == '"':
                strmode = True
            elif current == "\\":
                Stk.swap()

            elif current == 'g':
                xc = Stk.pop()
                yc = Stk.pop()
                Stk.push(chr(code[yc][xc]))

            elif current == 'p':
                xc = Stk.pop()
                yc = Stk.pop()
                vc = Stk.pop()
                tobepushed = chr(vc)
                code[xc][yc] = tobepushed

        # move in a given direction
        coordinates[0] = coordinates[0] + move[0]
        coordinates[1] = coordinates[1] + move[1]

        # rationalize coordinates
        if coordinates[1] > width:
            coordinates[1] = coordinates[1] % width
            coordinates[0] = coordinates[0] + (coordinates[1] // width)
            if coordinates[0] > length:
                coordinates[0] = coordinates[0] % length
        if coordinates[0] > length:
            coordinates[0] = coordinates[0] % length
            coordinates[1] = coordinates[1] + (coordinates[0] // length)
            if coordinates[0] > width:
                coordinates[0] = coordinates[0] % width

        # set pointer
        current = code[coordinates[0]][coordinates[1]]
        moves += 1
    print()
