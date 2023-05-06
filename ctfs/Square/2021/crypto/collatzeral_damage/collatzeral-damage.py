# idk just pick some random numbers for that 's box' thing, there might be a couple repeats...
stupid_box = [99, 171, 124, 123, 89, 76, 120, 89, 26, 91, 136, 26, 37, 190, 27, 59, 91, 123, 155, 91, 11, 19, 153, 11, 225, 27, 139, 155, 27, 155, 19, 147]

def ben_seq(starter):
    sequence = []
    current_step = starter
    max_steps = 14
    steps = 0
    while current_step > 1:
        sequence.append(current_step)
        current_step = ben_step(current_step)
        steps += 1
    return sequence[1:]

def ben_step(inp):
    if inp % 2 == 0:
        return inp / 2
    return (inp * 3) + 1

def find_longest(start, stop):
    largest_seq = []
    for i in range(start, stop):
        curr_seq = ben_seq(i)
        if len(curr_seq) > len(largest_seq):
            largest_seq = curr_seq

def bad_hash(flag_str):
    final_hash = [0] * 32

    final_touched_set = []

    for i, c in enumerate(flag_str):
        final_hash[i % len(final_hash)] = ord(c) ^ final_hash[i % len(final_hash)]

    for i in range(32):
        seq = ben_seq(final_hash[i])
        indexes = [step % len(final_hash) for step in seq]
        for j in indexes:
            if j != i:
                final_hash[j] = (final_hash[i] ^ stupid_box[j]) & final_hash[j]
    return final_hash

with open('flag.txt', 'r') as f:
    flag = f.read()
print "".join([chr(b).encode('hex') for b in bad_hash(flag)])