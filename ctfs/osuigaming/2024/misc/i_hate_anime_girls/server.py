#!/usr/local/bin/python
import base64
import sys

import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms as T
from torchvision.models import resnet18

model = resnet18()
model.fc = nn.Linear(model.fc.in_features, 1)
model.load_state_dict(torch.load("model.pt"))

resize = T.Resize((224, 224))
to_tensor = T.ToTensor()
normalize = T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

original = np.array(Image.open("hitorigoto.png"))

inp = input(f"Enter a base64 encoded image.\n")
try:
    img = np.frombuffer(base64.standard_b64decode(inp), dtype=np.uint8)
    img = img.reshape(original.shape)
    assert np.max(np.abs(original.astype(np.int32) - img.astype(np.int32))) <= 8
except:
    print("That doesn't look like hitorigoto!")
    sys.exit(0)

image = Image.fromarray(img)
x = normalize(resize(to_tensor(image)).unsqueeze(0))
with torch.no_grad():
    y = torch.sigmoid(model(x))

if y < 0.5:
    print("That's obviously an anime girl.")
    sys.exit(0)
elif y < 0.825:
    print("I'm not fully convinced that's not an anime girl.")
    sys.exit(0)

with open("flag.txt") as f:
    print("Surely that's not an anime girl.")
    print(f.read())
