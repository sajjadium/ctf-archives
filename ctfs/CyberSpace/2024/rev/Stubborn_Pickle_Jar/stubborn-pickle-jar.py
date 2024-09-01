import pickle
from io import BytesIO

with open("chall.pkl", 'rb') as f:
    p = f.read()
    up = pickle.Unpickler(BytesIO(p))
    result = up.load()
