import os
import random
from PIL import Image

köttbullar_dir = './assets/köttbullar'
hotdogs_dir = './assets/hotdogs'
output_dir = './encoded'
os.makedirs(output_dir, exist_ok=True)

köttbullar_files = [os.path.join(köttbullar_dir, f) for f in os.listdir(köttbullar_dir)]
hotdogs_files = [os.path.join(hotdogs_dir, f) for f in os.listdir(hotdogs_dir)]

with open('./secret.txt', 'r') as f:
    FLAG = f.read().strip()

bin_str = ''.join(format(ord(c), '08b') for c in FLAG)

for i, bit in enumerate(bin_str):
    src = random.choice(köttbullar_files) if bit == '0' else random.choice(hotdogs_files)
    dst = os.path.join(output_dir, f'{i:04}.jpeg')
    with Image.open(src) as img:
        img.save(dst, format='JPEG', quality=95)

print(f'Encoded {len(bin_str)} bits with CODEBULLAR encoding')
