import random

chars = [chr(i) for i in range(48, 58)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
alphabet = []

while len(alphabet) < 26:
    run = True
    while run:
        string = ""
        for _ in range(3): string += chars[random.randint(0, len(chars) - 1)]
        if string in alphabet: pass
        else: run = False
    alphabet.append(string)

keyboard_chars = [chr(i) for i in range(97, 123)]

dic = {char: term for char, term in zip(keyboard_chars, alphabet)}

msg = "REDACTED"
encoded = ""

for word in msg:
    for letter in word:
        if letter.lower() in dic.keys():
            encoded += dic[letter.lower()]
        else: encoded += letter

print(encoded)