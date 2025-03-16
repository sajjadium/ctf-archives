import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import base64
import random

FLAG = "JlLScp2qTzfFZ7kIYP6Jm5Mv/2h6p26S0OWgmXYdEMAl1Sjg6hwW95bPsZdtiggvHVVv8zM+x7vRw2qOr3ORbw=="
RED = "\033[0;31m"
PURPLE = "\033[0;35m"
ITALIC = "\033[3m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END = "\033[0m"

# don't mind the crypto stuff
class Cipher:
    def encrypt(self, plainText, key):
        iv = os.urandom(16) 
        privateKey = hashlib.sha256(key.encode("utf-8")).digest() 
        cipher = AES.new(privateKey, AES.MODE_CBC, iv)
        encryptedBytes = cipher.encrypt(pad(plainText.encode(), AES.block_size))  
        return base64.b64encode(iv + encryptedBytes).decode()

    def decrypt(self, encrypted, key):
        encryptedData = base64.b64decode(encrypted) 
        iv = encryptedData[:16] 
        privateKey = hashlib.sha256(key.encode("utf-8")).digest()  
        cipher = AES.new(privateKey, AES.MODE_CBC, iv) 
        try:
            decryptedBytes = unpad(cipher.decrypt(encryptedData[16:]), AES.block_size)  
        except:
            die(1)
        return decryptedBytes.decode()


places = ["Cemetery of Ash", "Grand Archives", "Profaned Capital", "Farron Keep", "Anor Londo", "High Wall of Lothric", "Undead Settlement", "Firelink Shrine", "Road of Sacrifices", "Irithyll Dungeon", "Catacombs of Carthus", "Lothric Castle", "Cathedral of the Deep","Irithyll of the Boreal Valley","Untended Graves","Kiln of the First Flame"]

routes = [
    [60, "Firelink Shrine", "Kiln of the First Flame", "Undead Settlement", "High Wall of Lothric"],
    [-10, "Lothric Castle", "High Wall of Lothric", "Irithyll of the Boreal Valley", "Untended Graves"],
    [12, "Irithyll Dungeon", "Grand Archives", "Undead Settlement", "Kiln of the First Flame"],
    [-5555, "Road of Sacrifices", "Catacombs of Carthus", "Anor Londo", "Cathedral of the Deep"],
    [555, "Irithyll of the Boreal Valley", "Irithyll Dungeon", "High Wall of Lothric", "Cemetery of Ash"],
    [3, "Firelink Shrine", "Undead Settlement", "Lothric Castle", "Untended Graves"],
    [1015, "High Wall of Lothric", "Road of Sacrifices", "Irithyll Dungeon", "Grand Archives"],
    [35, "Kiln of the First Flame", "High Wall of Lothric", "Cemetery of Ash", "Irithyll of the Boreal Valley"],
    [143, "Cathedral of the Deep", "Farron Keep", "Undead Settlement", "Lothric Castle"],
    [1551, "Irithyll of the Boreal Valley", "Profaned Capital", "High Wall of Lothric", "Farron Keep"],
    [70, "Farron Keep", "Irithyll of the Boreal Valley", "Grand Archives", "Firelink Shrine"],
    [77, "High Wall of Lothric", "Untended Graves", "Grand Archives", "Farron Keep"],
    [718640, "Farron Keep", "Road of Sacrifices", "Profaned Capital", "Anor Londo"],
    [869, "Anor Londo", "Irithyll Dungeon", "Catacombs of Carthus", "Road of Sacrifices"],
    [6969, "Lothric Castle", "High Wall of Lothric", "Kiln of the First Flame", "Cathedral of the Deep"]
]

position = ""
path = []

def checkFlag():
    global path
    aes = Cipher()

    a = "" 
    b = ""
    for p in path:
        if path.index(p) % 2 == 0:
            a += f"{p[0]+p[-1]}"
        else:
            b += f"{p[0]+p[-1]}"

    key = a+b
    attempt = aes.decrypt(FLAG,key)

    if "KSUS" not in attempt:
        die(1)
    else:
        print(f"\nYou hear that sweet female voice again, this time clearer.\n{ITALIC}Well done, Unflagged...{END}, she muses as a torn piece of parchment manifests itself in front of you:")
        print(f"{PURPLE}{attempt}{END}")
        exit()


def printLocationDetails():
    global position
    print(f"\nYou find yourself in a place called {PURPLE}{BOLD}{position.upper()}{END}.")
    print("A number of dangerous paths, crawling with enemies, open in front of you... An infinite sea of possibilities.\nWhere will you go?\n")
    for i,r in enumerate(routes[places.index(position)][1:]):
        print(f"\t{i}. {r}")


def die(way):
    quotes = [
        f"As you make your next step, you waste a second to glance at the bloodied path you are about to leave behind. \nOne second too long, as a blazing sword piercing right through you suddenly reminds you. \n{ITALIC}This spot marks our grave, but you may rest here too, if you would like...{END} a young prince whispers.",
        f"The earth trembles and you feel the sudden urge to look to the greyish sky above you.\n{ITALIC}Ignorant slaves, how quickly you forget{END}, a twisted dragon-man spits as he crushes you under his feet.",
        f"The deadly scythe of a woman grabs you by the waist.\n{ITALIC}Return from whence thou cam'st. For that is thy place of belonging{END}, the Sister commands before taking you to your grave.",
        f"In the thick mist, a nun-like figure reveals herself in front of you.\n{ITALIC}Return Lord of Londor. You have your own subjects to attain to{END}, she whispers as she cuts right through you with her scythe."
    ]
    if way:
        print(f"\n{random.choice(quotes)}")
    else:
        print(f"{ITALIC}What is taking you so long?{END}, Patches croons before kicking you off a cliff again.")

    print(f"\n\t{RED}YOU DIED{END}\n")
    exit()


def proceed(next):
    global position
    if sum([0, 0, 0, 1][routes[places.index(position)][0]:routes[places.index(position)][0]+1]) == 1:
        if next > ((221^216)>>True)*((len("...Rise, if you would...for that is our curse...")^53)>>1):
            die(1)
    elif sum(int(d) for d in str(abs(routes[places.index(position)][0]))) % 3 == 0:   
        if next > (int(bool(len("Why, Patches, why?")))):
            die(1)
    elif str(abs(routes[places.index(position)][0]))[-1] in "05":  
        if next > (True << True):
            die(1)
    elif (sum(int(str(routes[places.index(position)][0])[i]) for i in range(0, len(str(routes[places.index(position)][0])), 2)) - sum(int(str(routes[places.index(position)][0])[i]) for i in range(1, len(str(routes[places.index(position)][0])), 2))) % 11 == 0: 
        if next > (sum(map(int,str(111111)[::2]))):
            die(1)

    path.append(routes[places.index(position)][next])   
    position = routes[places.index(position)][next]
        

def play():
    global position
    global path
    while True:
        if position != "Kiln of the First Flame" and len(path) < 22: 
            printLocationDetails() 
            next = int(input("\nChoose a number >   "))
            if next < 0 or next > 3:
                exit()
            proceed(next+1)
        elif position == "Kiln of the First Flame":   
            checkFlag()
        elif len(path) >= 22:
            die(0)


def main():
    global position
    print(f"\n{ITALIC}You slowly rise as you are awaken by a sweet and ageless voice. \n'Let the Flame guide thee in this search for the flag', she whispers softly into your ear. \nBefore you can ask any questions, she disappears. \n\nYou are now left in utter silence.{END}\n")
    print(f"\t{UNDERLINE}PRESS ENTER TO CONTINUE{END}")
    input()
    position = "Cemetery of Ash"
    path.append(position)  
    play()


if __name__ == "__main__":
    main()