import torch
import torch.nn as nn
import torch.nn.functional as F

class ReplayFlow(nn.Module):
    def __init__(self, D=8, W=256):
        super(ReplayFlow, self).__init__()
        self.linears = nn.ModuleList(
            # input: (t, x, y)
            [nn.Linear(3, W)] +
            [nn.Linear(W, W) for _ in range(D)]
        )
        # (dx/t, dy/dt)
        self.vel_output = nn.Linear(W, 2)

    def forward(self, x):
        for l in self.linears:
            x = F.leaky_relu(l(x))
        v = self.vel_output(x)
        return v

model = ReplayFlow()
model.load_state_dict(torch.load("model.pt"))