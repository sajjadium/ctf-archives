import random
from itertools import product
from collections import deque

dims = [20, 20, 5, 5]
mine_count = 800
size = len(dims)


def neighbors(cell, dim_sizes):
    result = []
    for offset in product([-1, 0, 1], repeat=size):
        if any(offset):
            new_cell = tuple(cell[i] + offset[i] for i in range(size))
            if all(0 <= new_cell[i] < dim_sizes[i] for i in range(size)):
                result.append(new_cell)
    return result


def bordering_mines(cell, dim_sizes, mine_set):
    return sum(n in mine_set for n in neighbors(cell, dim_sizes))


all_coords = [tuple(x) for x in product(*(range(d) for d in dims))]
mines = set(random.sample(all_coords, mine_count))
revealed = set()


def reveal(start):
    queue = deque([start])
    newly_revealed = []
    while queue:
        current = queue.popleft()
        if current in revealed:
            continue
        revealed.add(current)
        newly_revealed.append(current)
        if bordering_mines(current, dims, mines) == 0:
            for nbr in neighbors(current, dims):
                if nbr not in revealed:
                    queue.append(nbr)
    return newly_revealed


while True:
    pt = tuple(map(int, input("Enter points (space-separated): ").split()))
    if (len(pt) != size) or any(not (0 <= pt[i] < dims[i]) for i in range(size)):
        print(
            f"Invalid input. Please enter coordinates within the grid dimensions: {dims}.")
        continue
    else:
        if pt in mines:
            print("BOOM! You hit a mine.")
            break
        if pt not in revealed:
            new_cells = reveal(pt)
            for c in new_cells:
                print(c, "has", bordering_mines(
                    c, dims, mines), "bordering mine(s).")
            if len(revealed) + len(mines) == len(all_coords):
                print(
                    "You win! The flag is squ1rrel{minesweeper}")
                break
