import random
import ast
import sys

p = random_prime(2^64-1, False, 2^63)
print(p)
R = Integers(p)

def gen_rand_string(n):
    return "".join([chr(random.randint(65, 90)) for _ in range(n)])

g = mod(primitive_root(p), p)
target_str = open("flag.txt").readline()

#print(target_str)

open("target.txt","w+").write(target_str)

def send_msg(sender, recipient, content):
    print(f"{sender} {recipient} {content}")

for pos in range(len(target_str)):
    fixed_eve = gen_rand_string(1)
    for iter in range(20):
        a = random.randint(1, p-1)
        b = random.randint(1, p-1)
        send_msg("Alice", "Bob", g^a)
        send_msg("Bob", "Alice", b)
        send_msg("Bob", "Alice", g^b)
        if random.randint(1, 2) == 1:
            # interception occurs
            c = random.randint(1, p-1)
            send_msg("Alice", "Bob", fixed_eve)
            send_msg("Alice", "Bob", g^c)
        else:
            send_msg("Alice", "Bob", target_str[pos])
            send_msg("Alice", "Bob", g^(a * b))
        print()

def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')
    raise Exception


try:
    answer = input_with_timeout('', 20)
    try:
        answer = ast.literal_eval(answer)
        if target_str == answer:
            print(":o")
            print(flag)
        else:
            print("im upset")
    except Exception as e:
        print("im very upset")
except Exception as e:
    print("\nyou've let me down :(")
