#!/usr/local/bin/python3 -u
import torch
import secrets
import hashlib
from config import FLAG

MAX_QUERY = 4000
SECRET_SCALE_RANGE = (500000, 1000000)
PARAM_RANDOM_RANGE = (-999, 999)
PARAM_SCALE = 1000

class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = torch.nn.Conv2d(
            in_channels = 1,
            out_channels = 1,
            kernel_size = (5, 5),
            stride = 1,
            padding = 0,
            dilation = 1,
            groups = 1,
            bias = True,
        )
        self.fc1 = torch.nn.Linear(
            in_features = 9,
            out_features = 2,
            bias = True,
        )

    def forward(self, x):
        out = self.conv1(x)
        out = out.view(-1,9)
        out = torch.nn.functional.relu(out)
        out = self.fc1(out)
        return out

    def secureRandRange(self, Range, scale, reject = None):
        v = (secrets.randbelow(Range[1] + 1 - Range[0]) + Range[0]) / scale
        if reject is not None and reject(v):
            v = (secrets.randbelow(Range[1] + 1 - Range[0]) + Range[0]) / scale
        return v

    def generateParams(self, flag):
        assert type(flag) == bytes
        assert len(flag) <= 25
        paramsCnt = 25 + 1 + 18 + 2
        secretScale = self.secureRandRange(SECRET_SCALE_RANGE, 1)
        paddedFlag = list(flag) + [self.secureRandRange((0, 0xff), 1) for i in range(paramsCnt - len(flag))]
        augmentedFlag = [c / secretScale for c in paddedFlag]
        reject = lambda v : v < 0.1 and v > -0.1
        params = [self.secureRandRange(PARAM_RANDOM_RANGE, PARAM_SCALE, reject = reject) + augmentedFlag[i] for i in range(paramsCnt)]
        for i in range(5):
            for j in range(5):
                self.conv1.weight.data[0][0][i][j] = params[i * 5 + j]
        self.conv1.bias.data[0] = params[25]
        for i in range(2):
            for j in range(9):
                self.fc1.weight.data[i][j] = params[25 + 1 + i * 9 + j]
        for i in range(2):
            self.fc1.bias.data[i] = params[25 + 1 + 18 + i]

def exitMsg(msg):
    print(msg)
    exit()

def main():
    torch.set_grad_enabled(False) 
    m = Model()
    m.generateParams(FLAG)
    m.eval()
    print(f'secret digest : {hashlib.sha256(FLAG).hexdigest()}')
    for i in range(MAX_QUERY):
        try:
            inp = input().strip()
            if inp == 'DONE':
                exitMsg('done')
            image = list(map(float, inp.split(',')))
        except Exception as e:
            print(e)
            exitMsg('bad input')
        if len(image) != 49:
            exitMsg('bad input')
        classification = int(torch.max(m.forward(torch.tensor(image).reshape(1, 7, 7)), 1)[1])
        print(classification)

if __name__ == '__main__':
    main()
