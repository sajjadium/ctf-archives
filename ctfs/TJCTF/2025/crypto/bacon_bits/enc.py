with open('flag.txt') as f: flag = f.read().strip()
with open('text.txt') as t: text = t.read().strip()

baconian = {
'a': '00000',	'b': '00001',
'c': '00010',	'd': '00011',
'e': '00100',	'f': '00101',
'g': '00110',	'h': '00111',
'i': '01000',    'j': '01000',
'k': '01001',    'l': '01010',
'm': '01011',    'n': '01100',
'o': '01101',    'p': '01110',
'q': '01111',    'r': '10000',
's': '10001',    't': '10010',
'u': '10011',    'v': '10011',
'w': '10100',	'x': '10101',
'y': '10110',	'z': '10111'}

text = [*text]
ciphertext = ""
for i,l in enumerate(flag):
    if not l.isalpha(): continue
    change = baconian[l]
    ciphertext += "".join([ts for ix, lt in enumerate(text[i*5:(i+1)*5]) if int(change[ix]) and (ts:=lt.upper()) or (ts:=lt.lower())]) #python lazy boolean evaluation + walrus operator

with open('out.txt', 'w') as e:
    e.write(''.join([chr(ord(i)-13) for i in ciphertext]))