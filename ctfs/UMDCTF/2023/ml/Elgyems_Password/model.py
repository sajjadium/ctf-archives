from torch import nn

model = nn.Sequential(
    nn.Linear(22, 69),
    nn.Linear(69, 420),
    nn.Linear(420, 800),
    nn.Linear(800, 85),
    nn.Linear(85, 13),
    nn.Linear(13, 37)
)