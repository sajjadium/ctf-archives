import sys
import string
import random
import hashlib
import time
import subprocess

FLAGS = [
    '<real new moon flag is on the server>',
    '<real waxing crescent flag is on the server>',
    '<real waxing gibbous flag is on the server>',
    '<real full moon flag is on the server>'
]
NUM_TRIALS = 50
PHASES = ['new moon', 'waxing crescent', 'waxing gibbous', 'full moon']
PHASE_FILES = ['new_moon.js', 'waxing_crescent.js', 'waxing_gibbous.js', 'full_moon.js']
MAXTIMES = [15, 15, 15, 30]
USE_POW = True

if USE_POW:
    # proof of work
    prefix = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    print("Give me a string starting with {} of length {} so its sha256sum ends in ffffff.".format(prefix, len(prefix)+8), flush=True)
    l = input().strip()
    if len(l) != len(prefix)+8 or not l.startswith(prefix) or hashlib.sha256(l.encode('ascii')).hexdigest()[-6:] != "ffffff":
        print("Nope.", flush=True)
        sys.exit(1)

while True:
    phase = input(f'which phase? [{", ".join(PHASES)}]\n')
    if phase not in PHASES:
        continue
    phase = PHASES.index(phase)
    break

for trial in range(NUM_TRIALS):
    print(f'{PHASES[phase]}: trial {trial+1}/{NUM_TRIALS}', flush=True)
    tick = time.time()
    p = subprocess.run(['node', PHASE_FILES[phase]])
    tock = time.time()
    if abs(tock-tick) > MAXTIMES[phase]:
        print(f'⌛️❗️ ({tock-tick:.3f})', flush=True)
        sys.exit(1)
    if p.returncode != 42:
        print(f'🔮️🚫️❗️', flush=True)
        sys.exit(1)

print('congrats!', flush=True)
print(FLAGS[phase])
