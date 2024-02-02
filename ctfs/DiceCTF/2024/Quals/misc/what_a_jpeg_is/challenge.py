#!/usr/bin/python3
import os
import sys
os.environ['OPENBLAS_NUM_THREADS'] = '1'

print("Starting up")
sys.stdout.flush()

import base64
import numpy as np
import io
from PIL import Image
from transformers import ConvNextImageProcessor, ConvNextForImageClassification
import torch
import torchvision.transforms as T
from datasets import load_dataset

def pytorch_jpeg_compress(img_tensors):
    out_tensors = []
    for img_tensor in img_tensors:
        quality = np.random.randint(50, 90)
        img = Image.fromarray(
            (
                np.clip(img_tensor.cpu().numpy().swapaxes(0, 1).swapaxes(1, 2), 0, 1) * 255
            ).astype(np.uint8)
        )

        with io.BytesIO() as f:
            img.save(f, "JPEG", quality=quality)
            img = Image.open(io.BytesIO(f.getvalue()))

        out_tensor = torch.tensor(
            np.array(img).swapaxes(2, 1).swapaxes(1, 0) / 255,
            device=img_tensor.device,
            dtype=torch.float32,
        )
        out_tensors.append(out_tensor)
    out_tensors = torch.stack(out_tensors)
    return out_tensors

processor = ConvNextImageProcessor.from_pretrained("facebook/convnext-base-384-22k-1k", cache_dir="./cache")
HFmodel = ConvNextForImageClassification.from_pretrained("facebook/convnext-base-384-22k-1k", cache_dir="./cache").eval()
model = next(HFmodel.modules())

dataset = load_dataset("huggingface/cats-image", cache_dir="./cache", trust_remote_code=True)
np_original = np.array(dataset["test"]["image"][0])

print("Loaded HuggingFace")

mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]
openmybook = T.ToTensor()
normalize = T.Normalize(mean, std)
reading_glasses = T.RandomResizedCrop(384, antialias=True)

prompts = ["Let me take a closer look", "I need to put on my reading glasses", "Let me try from another angle"]

for target_id in range(383, 388 + 1):
    breed = model.config.id2label[target_id].split(",")[0]
    inp = input(f"I love cats! My favorite breed is {breed}. Can you show me a picture of one?\n")
    try:
        np_breed = np.frombuffer(base64.standard_b64decode(inp), dtype=np.uint8)
        np_breed = np_breed.reshape(np_original.shape)
        assert np.max(np.abs(np_original.astype(int) - np_breed.astype(int))) < 10
    except:
        print("Sorry I only like cats that look exactly like my cat!", flush=True)
        sys.exit(0)

    for i in range(3):
        print(prompts[i])

        image = Image.fromarray(np_breed.astype(np.uint8))
        x = openmybook(image)
        x = x.unsqueeze(0)
        x = pytorch_jpeg_compress(x)
        x = normalize(x)
        x = reading_glasses(x)

        with torch.no_grad():
            logits = model(x).logits

        if torch.argmax(logits).item() != target_id:
            print(f"That doesn't look like a {breed}!")
            sys.exit(0)

with open("flag.txt") as f:
    print(f.read())