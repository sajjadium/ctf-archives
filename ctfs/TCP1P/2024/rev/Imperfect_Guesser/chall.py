import torch, random
import torch.nn
import numpy as np

flag = "TCP1P{REDACTED}"

def floatify(ip):
	flag = [float(ord(i)) for i in ip]
	normalized = torch.tensor([flag], dtype=torch.float32)
	return normalized

def tf(_in,_out):
	weight = np.round(np.random.uniform(-1, 1, (_out, _in)).astype(np.float32),2)
	bias = np.round(np.random.uniform(-1, 1, _out).astype(np.float32),2)
	return torch.from_numpy(weight), torch.from_numpy(bias)

np.random.seed(0x544350)
model = torch.nn.Sequential(
	torch.nn.Linear(24, 450),
	torch.nn.Linear(450, 128),
	torch.nn.Linear(128, 17)
)

layer_shapes = [(24, 450), (450, 128), (128, 17)]

for i, (input_dim, output_dim) in enumerate(layer_shapes):
	weight, bias = tf(input_dim, output_dim)
	model[i].weight.data = weight
	model[i].bias.data = bias
 
print([i.detach().numpy().tolist() for i in model(floatify(flag))[0]])
# Output:
# [38883.9140625, 18747.87890625, -15371.05078125, 12231.2080078125, -56379.48046875, -33719.13671875, 9454.150390625, 9346.9814453125, 1701.4693603515625, -6380.3759765625, 12019.501953125, -4850.94140625, 14421.296875, 44332.0390625, -11196.283203125, -19712.0859375, -36390.265625]