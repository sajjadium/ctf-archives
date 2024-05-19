import torch

flag = open("flag.txt").read().strip()

class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.f1 = torch.nn.Linear(len(flag), 22)
        self.relu = torch.nn.ReLU()
        self.f2 = torch.nn.Linear(22, 18)

    def forward(self, x):
        x = self.relu(self.f1(x))
        return self.f2(x)

model = Model()

model.f1.weight = torch.nn.Parameter(torch.randint(0, 10, (22, len(flag)), dtype=torch.float64))
model.f1.bias = torch.nn.Parameter(torch.randint(0, 10, (22,), dtype=torch.float64))
model.f2.weight = torch.nn.Parameter(torch.randint(0, 10, (18, 22), dtype=torch.float64))
model.f2.bias = torch.nn.Parameter(torch.randint(0, 10, (18,), dtype=torch.float64))

torch.save(model.state_dict(), "model.pth")

x = torch.tensor([ord(c) for c in flag], dtype=torch.float64).unsqueeze(0)
y = model(x)

torch.save(y.detach(), "output.pth")
