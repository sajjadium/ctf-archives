import os
import time
import sys
import re
import math
import random
import statistics
import glob
import torch
import torch.nn as nn
import torch.optim as optim
from datetime import date
from torchvision import models
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from geotask.split_earth_s2 import get_classes
from haversine import haversine


classes = get_classes()


def get_model():
    model = models.resnet50()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Modify the first layer to accommodate the larger input
    model.conv1 = nn.Conv2d(3, 64, kernel_size=(15, 15), stride=(4, 4), padding=(6, 6), bias=False)

    num_classes = len(classes)
    # Replace the last layer with a fully connected layer for our number of classes
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    model = model.to(device)
    return model

