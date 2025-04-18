import os

FLAG_OFFSET = REDACTED
FLAG = REDACTED

BURGER_LAYERS = ["Bun (1)", "Lettuce (2)", "Tomato (3)", "Cheese (4)", "Patty (5)", "Onion (6)", "Pickle (7)", "Mayonnaise (8)", "Egg (9)", "Avocado (10)"]

def print_towers(towers):
    for i, tower in enumerate(towers):
        print(f"Tower {i + 1}: {[BURGER_LAYERS[layer - 1] for layer in tower]}")
    print()

def move_disk(towers, from_tower, to_tower):
    if not towers[from_tower]:
        print("Invalid move: Source plate is empty.")
        return False
    if towers[to_tower] and towers[to_tower][-1] < towers[from_tower][-1]:
        print("Invalid move: Cannot place larger burger layer on smaller burger layer.")
        return False
    towers[to_tower].append(towers[from_tower].pop())
    return True

def towers_of_hanoi():
    num_disks = int(input("Enter the number of burger layers (1-10): "))
    while num_disks < 1 or num_disks > 10:
        print("Please enter a number between 1 and 10 inclusive.")
        num_disks = int(input("Enter the number of burger layers (1-10): "))
    towers = [list(range(num_disks, 0, -1)), [], []]

    print_towers(towers)

    while len(towers[2]) != num_disks:
        try:
            from_tower = int(input("Move from plate (1-3): ")) - 1
            to_tower = int(input("Move to plate (1-3): ")) - 1
            if from_tower not in range(3) or to_tower not in range(3):
                print("Invalid input. Please enter a number between 1 and 3.")
                continue
            if move_disk(towers, from_tower, to_tower):
                print_towers(towers)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    print(f"Congratulations! You solved the puzzle. The last { num_disks} bits of the offset used to encrypt the flag are {bin(FLAG_OFFSET & ((1 << ( num_disks )) - 1))}.")
    if num_disks >= 9:
        print("Waoh, that is a big sandwich! The offset only has 6 bits though...")

def key_gen_func(i: int) -> int:
    # a deterministic function that generates a key based on the index using a very cool sequence of non-negative integers
    REDACTED
    
def encrypt(message: bytes, offset = FLAG_OFFSET) -> str:
    encrypted = bytearray()
    
    if offset is None:
        offset = os.urandom(1)[0]
        
    for (i, char) in enumerate(message):
        encrypted.append(char ^ (key_gen_func(i + offset) & 0xFF))
    return encrypted.hex()

if __name__ == "__main__":
    choice = input("Options\n1. Make a Burger\n2. Encrypt with random offset\n3. Get encrypted flag\nSelect an option: ")
    if(choice == '1'):
        towers_of_hanoi()
    elif(choice == '2'):
        str = input("Enter a string to encrypt: ")
        print(encrypt(str.encode(), offset=None))
    elif(choice == '3'):
        print(encrypt(FLAG, offset=FLAG_OFFSET))