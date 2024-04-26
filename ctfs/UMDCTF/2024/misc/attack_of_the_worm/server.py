#!/usr/local/bin/python
import sys

import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torchvision.models import resnet18

model = resnet18()
model.fc = nn.Linear(model.fc.in_features, 1)
model.load_state_dict(torch.load('model.pt'))

original = np.array(Image.open("worm.png"))
modified = original.copy()

inp = input(f"Enter a list of pixels to change, in the format 'x,y,r,g,b;x,y,r,g,b;...':\n")
try:
    pixels = inp.split(";")
    assert len(pixels) <= 30
    for pixel in pixels:
        x, y, r, g, b = map(int, pixel.split(","))
        modified[y, x] = [r, g, b]
except:
    print("Too many pixel changes.")

x = torch.tensor(modified.transpose(2, 0, 1) / 255.0, dtype=torch.float32).unsqueeze(0)
with torch.no_grad():
    y = torch.sigmoid(model(x))

if y >= 0.5:
    print("that's clearly a worm buddy")
    sys.exit(0)

with open("flag.txt", "r") as f:
    print("LISAN AL GAIB")
    print(f.read())