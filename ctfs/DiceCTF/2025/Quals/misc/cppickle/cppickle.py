#!/usr/bin/python3
import torch
import io

b = bytes.fromhex(input("> "))
assert b[4:8] != b"PTMF"
torch.jit.load(io.BytesIO(b))
