import torch
from torch import nn
import numpy as np
from functools import reduce
import base64


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.stack = nn.Sequential(*([nn.Linear(8, 8, bias=False)] * 7))

    def forward(self, x):
        x = self.stack(x)
        return x


device = "cuda" if torch.cuda.is_available() else "cpu"

model = NeuralNetwork().to(device)
torch.save(model.state_dict(), "model.pth")

flag = b"buckeye{???????????????????????????????????????????????????????}"
assert len(flag) == 64
X = np.reshape(list(flag), (8, 8)).astype(np.float32)

Xt = torch.from_numpy(X).to(device)
Y = model(Xt).detach().numpy()

print(base64.b64encode(Y).decode())
# Output: 1VfgPsBNALxwfdW9yUmwPpnI075HhKg9bD5gPDLvjL026ho/xEpQvU5D4L3mOso+KGS7vvpT5T0FeN284inWPXyjaj7oZgI8I7q5vTWhOj7yFEq+TtmsPaYN7jxytdC9cIGwPti6ALw28Pm9eFZ/PkVBV75iV/U9NoP4PDoFn72+rI8+HHZivMwJvr2s5IQ+nASFvhoW2j1+uHE98MbuvdSNsT4kzrK82BGLvRrikz6oU66+oCGCPajDmzyg7Q69OjiDPvQtnjxwWw2+IB9ZPmaCLb4Mwhc+LimEPXXBQL75OQ8/ulQUvZZMsr3iO88+ZHz3viUgLT2U/d68C2xYPQ==
