import random

with open('sample.txt') as file:
    line = file.read()

with open('flag.txt') as file:
    flag = file.read()

samples = [line[i:i+28] for i in range(0, len(line) - 1 - 28, 28)]

samples.insert(random.randint(0, len(samples) - 1), flag)

i = 0
while len(samples) < 40:
    samples.append(samples[len(samples) - i - 2])
    i = random.randint(0, len(samples) - 1)

encrypted = []
for i in range(len(samples)):
    x = samples[i]
    if i < 10:
        nonce = str(i) * 28
    else:
        nonce = str(i) * 14
    encrypted.append(''.join(str(ord(a) ^ ord(b)) + ' ' for a,b in zip(x, nonce)))

with open('output.txt', 'w') as file:
    for i in range(0, 4):
        file.write('input: ' + samples[i] + '\noutput: ' + encrypted[i] + '\n')
    file.write('\n')
    for i in range(4, len(samples)):
        file.write('\ninput: ???\n' + 'output: ' + encrypted[i])
