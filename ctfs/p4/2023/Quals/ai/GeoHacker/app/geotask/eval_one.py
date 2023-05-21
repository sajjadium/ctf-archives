from sqlite3 import DatabaseError
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
import glob
import os 
import json
import random
import math
from geotask.downloader.get_one_by_coords import get_image_by_coords, get_image_by_panoid
from geotask.train_resnet import get_model, classes
from haversine import haversine


from torch import nn
from PIL import Image
import sys


def load_model(model_path):
    model = get_model()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))["model_state_dict"])
    model.eval()
    return model

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    #RandomPanoramaShift()
])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def eval_multi(model, panoids=None):

    images = []
    for panoid in panoids:
        image = get_image_by_panoid(panoid)
        image = transform(image.convert('RGB')).to(device)
        images.append(image)
    imgs = torch.stack(images)

    inference = model(imgs)
    inference = inference.detach()

    out = torch.max(inference, 1)[1]
    preds = []
    for idx in out:
        pred = None
        for cl in classes:
            if idx.item() == cl[0]:
                pred = cl[1]
                break
        preds.append(pred)
    return preds


def eval_one(model, coords=None, panoid=None):
    if coords:
        lat, lon = coords
        image = get_image_by_coords(lat, lon)
    if panoid:
        image = get_image_by_panoid(panoid)

    data = transform(image.convert('RGB')).to(device).unsqueeze(0)

    inference = model(data)
    inference = inference.detach()
    out = torch.max(inference, 1)
    idx = out.indices[0].item()
    pred = None
    for cl in classes:
        if idx == cl[0]:
            pred = cl
            break
    class_, pred_coords = pred[0], pred[1]
    pred_lat, pred_lon = pred[1]
    pred_coords = (pred_lat, pred_lon)
    return class_, pred_coords

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Provide arg to eval")
        exit()
    if len(sys.argv) == 3:
        eval_one(load_model(sys.argv[1]), image_path=sys.argv[2])
    if len(sys.argv) == 4:
        lat, lon = sys.argv[2], sys.argv[3]
        eval_one(load_model(sys.argv[1]), coords=(float(lat), float(lon)))

