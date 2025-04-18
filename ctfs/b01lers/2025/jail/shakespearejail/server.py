#!/usr/local/bin/python3
import io
import random
import sys

from shakespearelang.shakespeare import Shakespeare
print("You're nothing like a summers day.")
print("enter your play > ")

blacklist = [
"Heaven",
"King",
"Lord",
"angel",
"flower",
"happiness",
"joy",
"plum",
"summer's",
"day",
"hero",
"rose",
"kingdom",
"pony",
"animal",
"aunt",
"brother",
"cat",
"chihuahua",
"cousin",
"cow",
"daughter",
"door",
"face",
"father",
"fellow",
"granddaughter",
"grandfather",
"grandmother",
"grandson",
"hair",
"hamster",
"horse",
"lamp",
"lantern",
"mistletoe",
"moon",
"morning",
"mother",
"nephew",
"niece",
"nose",
"purse",
"road",
"roman",
"sister",
"sky",
"son",
"squirrel",
"stone",
"wall",
"thing",
"town",
"tree",
"uncle",
"wind",
"Hell",
"Microsoft",
"bastard",
"beggar",
"blister",
"codpiece",
"coward",
"curse",
"death",
"devil",
"draught",
"famine",
"flirt-gill",
"goat",
"hate",
"hog",
"hound",
"leech",
"lie",
"pig",
"plague",
"starvation",
"toad",
"war",
"wolf"
]


blacklist += ["open",
			  "listen"]


blacklist += ["am ",
              "are ",
              "art ",
              "be ",
              "is "]

solution = ""
for line in sys.stdin:
    solution += line.lower()
    if line.strip().lower() == "[exeunt]":
        break

print("play received")
 
disallowed = False
for word in blacklist:
    if word.lower() in solution:
        print(f"You used an illegal word: {word}")
        disallowed = True
        break

if not solution.isascii():
    print("there were non-ascii characters in your solution.")
    disallowed = True

if (not disallowed):
    old_stdout = sys.stdout
    old_stdin = sys.stdin
    sys.stdout = io.StringIO()
    sys.stdin = io.StringIO()
    
    try: 
        interpreter = Shakespeare(play=solution, input_style='basic', output_style='basic')
        interpreter.run()
        payload = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        
    eval(payload)
else:
    with open("insults.txt", "r") as file:
        insults = file.readlines()
        random_insult = random.choice(insults).strip()
        print(random_insult)