#!/usr/local/bin/python
import base64
import os
import sys

import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torchvision.models import resnet18
import torchvision.transforms as T

def mask_generation(patch=None, image_size=(3, 224, 224)):
    applied_patch = np.zeros(image_size)

    rotation_angle = np.random.choice(4)
    for i in range(patch.shape[0]):
        patch[i] = np.rot90(patch[i], rotation_angle)

    x_location, y_location = np.random.randint(low=0, high=image_size[1]-patch.shape[1]), np.random.randint(low=0, high=image_size[2]-patch.shape[2])
    applied_patch[:, x_location:x_location + patch.shape[1], y_location:y_location + patch.shape[2]] = patch
    mask = applied_patch.copy()
    mask[mask != 0] = 1.0
    return applied_patch, mask, x_location, y_location

test_transforms = T.Compose([
    T.Resize(size=(224, 224)),
    T.RandomHorizontalFlip(),
    T.ToTensor()
])

model = resnet18()
model.fc = nn.Linear(model.fc.in_features, 1)
model.load_state_dict(torch.load('model.pt'))

model.eval()

inp = input(f"Enter a base64 encoded 40x40 image patch.\n")
try:
    patch = np.frombuffer(base64.standard_b64decode(inp), dtype=np.uint8)
    patch = patch.reshape((3, 40, 40)).transpose(2, 0, 1) / 255
except:
    print("Invalid patch.")
    sys.exit(0)

total = 0
correct = 0
for test_img in os.listdir("worms"):
    total += 1
    img = Image.open(f"worms/{test_img}")
    img = T.Resize(size=(224, 224))(img)
    img = T.ToTensor()(img)

    applied_patch, mask, _, _ = mask_generation(patch, image_size=(3, 224, 224))
    applied_patch = torch.from_numpy(applied_patch)
    mask = torch.from_numpy(mask)
    perturbated_image = mask.float() * applied_patch.float() + (1 - mask.float()) * img.float()
    output = model(perturbated_image.unsqueeze(0))
    predicted = (output > 0).int()
    if predicted == 0:
        correct += 1

if correct / total >= 0.7:
    with open("flag.txt", "r") as f:
        print("LISAN AL GAIB")
        print(f.read())
else:
    print("Worm detected.")