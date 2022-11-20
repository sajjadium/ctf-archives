"""
Author : @koopaenhiver
"""

import hashlib

ninlist1 = ["", "The Legend of ", "Super ", "Paper ", "Final ", "Tales of ", \
            "Star ", "Call of "]
ninlist2 = ["Zelda", "Link", "Pokemon", "Pikachu", "Mario", "Luigi", \
            "Metroid", "Samus", "Fire Emblem", "Donkey Kong", "Smash Bros.", \
            "Banjo-Kazooie", "Fantasy", "Pikmin", "Fox", "Kirby"]
ninlist3 = [" Adventure", "'s Mansion", " Tactics", "'s Awakening", " Dread", \
            " Prime", " Odyssey", " Echoes", " Corruption", " Kart", \
            " Sunshine", " Galaxy", " Let's Go", " Zero Mission", " Chronicles", \
            " Legends"]
ninlist4 = ["", " 1", " 2", " 3", " 4", " VII", " X", " 64", " 128",
          " Remastered", " Remake", " 3D", " Trilogy", " Deluxe", \
          " Prequel", " Ultimate"]
ninlist5 = ["", " : Tears of the Kingdom", " : The Wind Waker", \
            " : Twilight Princess", " : Breath of the Wild", \
            " : Dawn of the New World", " : Version Ecarlate", \
            " : Ocarina of Time", " : Version Violet", " : Version Or", \
            " : The Last Hope", " : Version Argent", \
            " : Till the End of Time", " : The Origami King", \
            " : The Thousand-Year Door", " : Color Splash" ]

ninlists = [ninlist1, ninlist2, ninlist3, ninlist4, ninlist5]

def Nintendhash(message):
    m = hashlib.sha256()
    m.update(message)
    digest = m.hexdigest()
    lastfivehex = digest[-5:]
    nintendigest = ""
    for i in range(0,5):
        digit = int(lastfivehex[i], base=16)
        if i == 0:
            nintendigest = nintendigest + ninlists[i][digit%8]
        else:
            nintendigest = nintendigest + ninlists[i][digit]
            
    return nintendigest
    
