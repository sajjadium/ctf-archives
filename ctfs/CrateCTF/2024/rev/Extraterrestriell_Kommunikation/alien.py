from PIL import Image
from math import lcm

morse_code_dict = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '{': '---...', '}': '...---'
}
def convertTuple(tup):
    st = ''.join(map(str, tup))
    return st

ascii_to_coord = {}

for letter in morse_code_dict:
    ascii_to_coord[letter] = morse_code_dict[letter].count('-'), morse_code_dict[letter].count('.')

coord_to_ascii = {}
for a in ascii_to_coord:
    coord_to_ascii[convertTuple(ascii_to_coord[a])] = []
    for b in ascii_to_coord:
        if ascii_to_coord[a] == ascii_to_coord[b]:
            if b not in coord_to_ascii:
                coord_to_ascii[convertTuple(ascii_to_coord[a])].append(b)
                #print(a,b)

flag = ""
with open("flag.txt", "r") as f:
    flag = f.readlines()[0]

dummyPaint = [[0, 0, 0, 0, 0] for i in range(6)]

for ch in flag:
    dummyPaint[ascii_to_coord[ch][0]][ascii_to_coord[ch][1]] += 1

removedZeroes = sum(list(map(lambda i: list(filter(lambda j: j > 0, i)), dummyPaint)), [])
minRows = lcm(*removedZeroes)
pixels = 5 * minRows
image = Image.new('RGB', (pixels, pixels))

for index, ch in enumerate(flag):
    r = int(((coord_to_ascii[convertTuple(ascii_to_coord[ch])].index(ch)) / len(coord_to_ascii[convertTuple(ascii_to_coord[ch])]) *256) + 1)
    rgb = (r,  0, int((index/len(flag)*256) + 1))
    tot = 0
    isMany = False 
    strokeSize = minRows / dummyPaint[ascii_to_coord[ch][0]][ascii_to_coord[ch][1]]

    if dummyPaint[ascii_to_coord[ch][0]][ascii_to_coord[ch][1]] > 1:
        isMany = True
        for asc in coord_to_ascii[convertTuple(ascii_to_coord[ch])]:
            tot += flag[0:index].count(asc)

    for i in range(0, minRows):
        for j in range(0, minRows):
            if isMany and not (i+1 > (strokeSize * tot) and i < (strokeSize * (tot + 1))):
                continue
            x = (minRows * (ascii_to_coord[ch][0])) + i
            y = (minRows * (ascii_to_coord[ch][1])) + j
            image.putpixel((x,y), rgb)

image.save('flag.png')
