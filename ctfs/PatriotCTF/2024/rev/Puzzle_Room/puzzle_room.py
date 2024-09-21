#!/usr/bin/env python
import time
import random

#### Crypto stuff not important
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size :])).decode("utf-8")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def slow_print(msg, delay=0.02):
    for letter in msg:
        time.sleep(delay)
        print(letter, end="", flush=True)
    print()


def how_did_you_succumb_to_a_trap():
    slow_print(
        bcolors.FAIL + "FWOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOSH" + bcolors.ENDC,
        delay=0.04,
    )
    ways_to_get_got = [
        "Well, you sure found the trap—too bad it found you first.",
        "That one step forward just turned you into a well-done adventurer.",
        "Turns out not checking for traps does lead to a fiery conclusion.",
        "Took one step too many... and now you’re part of the decor.",
        "Next time, maybe trust your instincts before you become toast.",
        "Maybe next time you’ll sneeze before stepping onto the fire trap.",
        "Well, if you were looking for a quick tan, mission accomplished.",
        "Looks like you found the fire... with your face.",
        "Well, that’s one way to light up the room—too bad it’s you that’s burning.",
        "Guess those fire-resistant potions were back in your pack, huh?",
        "You just turned 'walking into danger' into 'walking into a bonfire.'",
        "At least now we know what happens when you don’t watch your step... you sizzle.",
        "You really lit up the room...",
    ]
    slow_print(random.choice(ways_to_get_got))


def how_did_you_avoid_the_fire():
    ways_to_avoid = [
        "Good thing you sneezed before walking in or you'd be toast!",
        "That was close-who knew stopping to tie your boot would keep you safe?",
        "You had a bad feeling about this room, and it turns out, you were right!",
        "Good thing you hesitated, or else you'd be one roast adventurer",
        "You stopped, unsure for just a moment—and that indecision saved your life.",
        "That brief moment of doubt was all it took to avoid being incinerated.",
        "Lucky that you bent down to adjust your gear—one more step and you'd be fried.",
        "That sudden itch you stopped to scratch just saved you from being flame-broiled.",
        "Lucky you had to tighten your pack strap—you missed the fire by a heartbeat.",
        "Good thing you hesitated—one more step and you'd be barbecue.",
    ]
    slow_print(bcolors.OKGREEN + random.choice(ways_to_avoid) + bcolors.ENDC)


class PathGroup:
    tiles = []
    current_cordinates = None
    path_history = []

    def __repr__(self):
        return "[X] {} -- {} \n".format(self.tiles, self.path_history)


grid = [
    [
        "SPHINX",
        "urn",
        "vulture",
        "arch",
        "snake",
        "urn",
        "bug",
        "plant",
        "arch",
        "staff",
        "SPHINX",
    ],
    [
        "plant",
        "foot",
        "bug",
        "plant",
        "vulture",
        "foot",
        "staff",
        "vulture",
        "plant",
        "foot",
        "bug",
    ],
    [
        "arch",
        "staff",
        "urn",
        "Shrine",
        "Shrine",
        "Shrine",
        "plant",
        "bug",
        "staff",
        "urn",
        "arch",
    ],
    [
        "snake",
        "vulture",
        "foot",
        "Shrine",
        "Shrine",
        "Shrine",
        "urn",
        "snake",
        "vulture",
        "foot",
        "vulture",
    ],
    [
        "staff",
        "urn",
        "bug",
        "Shrine",
        "Shrine",
        "Shrine",
        "foot",
        "staff",
        "bug",
        "snake",
        "staff",
    ],
    [
        "snake",
        "plant",
        "bug",
        "urn",
        "foot",
        "vulture",
        "bug",
        "urn",
        "arch",
        "foot",
        "urn",
    ],
    [
        "SPHINX",
        "arch",
        "staff",
        "plant",
        "snake",
        "staff",
        "bug",
        "plant",
        "vulture",
        "snake",
        "SPHINX",
    ],
]


def print_grid_with_path_group(grid, pg):
    for i, x in enumerate(grid):
        for j, y in enumerate(x):
            if (i, j) in pg.path_history:
                if (i, j) == pg.path_history[-1]:
                    print(
                        bcolors.FAIL + str("YOU").ljust(8, " ") + bcolors.ENDC, end=""
                    )
                else:
                    print(str("STEP").ljust(8, " "), end="")
            else:
                print(str(y).ljust(8, " "), end="")
        print()


def try_get_tile(tile_tuple):
    try:
        return grid[tile_tuple[0]][tile_tuple[1]], (tile_tuple[0], tile_tuple[1])
    except Exception as e:
        return None


def print_current_map():
    for x in grid:
        for y in x:
            print(str(y).ljust(8, " "), end="")
        print()


# This is you at (3,10)!
starting_tile = (3, 10)
starting_path = PathGroup()
starting_path.tiles = ["vulture"]
starting_path.current_cordinates = starting_tile
starting_path.path_history = [starting_tile]


def move(path, tile):
    sub_path = PathGroup()
    sub_path.tiles.append(tile)
    sub_path.current_cordinates = tile
    sub_path.path_history = path.path_history.copy()
    sub_path.path_history.append(tile)
    return sub_path


cur_tile = starting_tile


def menu(path):
    cur_tile = path.current_cordinates
    next_tile = None
    while next_tile == None:
        print(
            bcolors.OKGREEN
            + "\t ------------- The puzzle room layout -------------"
            + bcolors.ENDC
        )
        print_grid_with_path_group(grid, path)
        choice = input("Which direction will you journey next? : ").upper()
        # Hope you have python 3.10!
        match choice:
            case "N":
                next_tile = (cur_tile[0] -1, cur_tile[1])
            case "S":
                next_tile = (cur_tile[0] +1, cur_tile[1])
            case "E":
                next_tile = (cur_tile[0], cur_tile[1] +1)
            case "W":
                next_tile = (cur_tile[0], cur_tile[1] -1)
            case "NE":
                next_tile = (cur_tile[0] -1, cur_tile[1] +1)
            case "NW":
                next_tile = (cur_tile[0] -1, cur_tile[1] -1)
            case "SE":
                next_tile = (cur_tile[0] +1, cur_tile[1] +1)
            case "SW":
                next_tile = (cur_tile[0] +1, cur_tile[1] -1)
            case _:
                print("That doesn't seem to be a valid direction")
	
    new_path = move(path, next_tile)
    return new_path


slow_print(
    "With your hulking strength you break down the door to a room clearly designed to hold riches."
)
slow_print(
    "The door FLINGS across the room and lands on (3,9) and a massive ray a fire ignites the room."
)
slow_print(".", 0.3)
slow_print("..", 0.3)
slow_print("...", 0.3)

how_did_you_avoid_the_fire()
slow_print(
    "Phew, good thing you weren't in the room yet. Clearly it's booby trapped and you step onto the first tile (3,10)"
)


def check_path(path):

    for tile in path.path_history:
        if tile[1] > 10 or tile[1] < 0:
            how_did_you_succumb_to_a_trap()
            exit(-1)
        if tile[0] > 6 or tile[0] < 0:
            how_did_you_succumb_to_a_trap()
            exit(-1)

    if path.current_cordinates == (3, 9):
        slow_print(
            "As you step atop the door that triggered the traps in the first place, you think to yourself: 'Should I really have stepped on a space I knew would trigger a trap?'"
        )
        how_did_you_succumb_to_a_trap()
        exit(-1)

    if try_get_tile(path.current_cordinates)[0] == "SPHINX":
        how_did_you_succumb_to_a_trap()
        exit(-1)

    if len(set(path.path_history)) != len(path.path_history):
        how_did_you_succumb_to_a_trap()
        exit(-1)

    for tile in path.path_history[:-1]:
        if try_get_tile(path.current_cordinates)[0] == try_get_tile(tile)[0]:
            how_did_you_succumb_to_a_trap()
            exit(-1)

    if try_get_tile(path.current_cordinates)[0] != "Shrine" and len(
        set([x[1] for x in path.path_history])
    ) != len([x[1] for x in path.path_history]):
        how_did_you_succumb_to_a_trap()
        exit(-1)

    if try_get_tile(path.current_cordinates)[0] == "Shrine":
        key = "".join([try_get_tile(x)[0] for x in path.path_history])
        enc_flag = b"FFxxg1OK5sykNlpDI+YF2cqF/tDem3LuWEZRR1bKmfVwzHsOkm+0O4wDxaM8MGFxUsiR7QOv/p904UiSBgyVkhD126VNlNqc8zNjSxgoOgs="
        obj = AESCipher(key)
        dec_flag = obj.decrypt(enc_flag)
        if "pctf" in dec_flag:
            slow_print(
                bcolors.OKBLUE
                + "You've done it! All the traps depress and a rigid 'click' can be heard as the center chest opens! As you push open the top your prize sits inside!"
                + bcolors.ENDC
            )
            print(bcolors.OKCYAN + dec_flag + bcolors.ENDC)
            exit(0)
        else:
            slow_print(
                "You step onto the center area expecting your prize, but a loud whirling sound is heard instead. The floor plates make a large mechanical click sounds and engage the fire trap once again!"
            )
            how_did_you_succumb_to_a_trap()
            exit(-1)


cur_path = starting_path
while True:
    n_path = menu(cur_path)
    check_path(n_path)
    cur_path = n_path
