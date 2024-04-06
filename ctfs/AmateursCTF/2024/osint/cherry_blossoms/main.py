#!/usr/bin/env python3
# modified from HSCTF 10 grader
import json
with open("locations.json") as f:
	locations = json.load(f)
wrong = False
for i, coords in enumerate(locations, start=1):
	x2, y2 = coords
	x, y = map(float, input(f"Please enter the lat and long of the location: ").replace(",","").split(" "))
    # increase if people have issues
	if abs(x2 - x) < 0.0010 and abs(y2 - y) < 0.0010:
		print("Correct! You have successfully determined the position of the camera.")
	else:
		print("Wrong! Try again after paying attention to the picture.")
		wrong = True

if not wrong:
	with open("flag.txt") as f:
		print("Great job, the flag is ",f.read().strip())
else:
	print("Better luck next time ʕ·ᴥ·ʔ")