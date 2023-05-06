# below from https://stackoverflow.com/a/10238140
# (licensed CC BY-SA 3.0, by John Gaines Jr.)
def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([b for b in bits])
    return result
# end copied text

txt = open("flag.txt", "r").read()
f = open("shuffled", "wb")
order = [ 0, 1, 1, 0, 0, 0, 1, 0 ]
deck = tobits(txt)
for i in order:
    newdeck = []
    for j in range(int(len(deck)/2)):
        if i == 0:
            newdeck.append(deck[j])
            newdeck.append(deck[j+int(len(deck)/2)])
        else:
            newdeck.append(deck[j+int(len(deck)/2)])
            newdeck.append(deck[j])
    deck = newdeck
f.write(int("".join(deck),2).to_bytes(len(deck)//8, byteorder="big"))