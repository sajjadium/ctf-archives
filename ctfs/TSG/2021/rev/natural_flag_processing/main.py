import string

import torch
from torch import nn

FLAG_CHARS = string.ascii_letters + string.digits + "{}-"
CHARS = "^$" + FLAG_CHARS
def sanity_check(text):
    global FLAG_CHARS
    assert text[:7] == "TSGCTF{"
    assert text[-1:] == "}"
    assert all([t in FLAG_CHARS for t in text])

def embedding(text):
    global CHARS
    x = torch.zeros((len(text), len(CHARS)))
    for i, t in enumerate(text):
        x[i, CHARS.index(t)] = 1.0
    return x

class Model(nn.Module):
    def __init__(self, inpt, hidden):
        super().__init__()
        self.cell = nn.RNNCell(inpt, hidden)
        self.out = nn.Linear(hidden, 1)
    def forward(self, xs):
        h = None
        for x in xs:
            h = self.cell(x, h)
        return self.out(h)

def inference(model, text):
    model.eval()
    with torch.no_grad():
        x = embedding("^"+text+"$").unsqueeze(1)
        y = model(x)[0].sigmoid().cpu().item()
    return y

model = Model(len(CHARS), 520)
model.load_state_dict(torch.load("model_final.pth"))
text = input("input flag:")
sanity_check(text)
if inference(model, text) > 0.5:
    print("Congrats!")
else:
    print("Wrong.")