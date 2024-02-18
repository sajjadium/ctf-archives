#!/usr/local/bin/python3

import secrets
from super_secret_stuff import flag, f, f_inverse

seed = secrets.randbits(16)
function_uses = 0
oracle_uses = 0
done = False

def compute_output_bit(state, pred):
    return bin((state & pred)).count("1") % 2

def prng(pred):
    cur_state = seed
    outputs = []
    for i in range(16):
        cur_state = f(cur_state)
        outputs.append(compute_output_bit(cur_state, pred))
    cur_state = f(cur_state)
    cur_state_bits = format(cur_state, 'b').zfill(16)
    all_bits = ("".join([str(i) for i in outputs]) + cur_state_bits)[::-1]
    return all_bits

def pprngc(pred, stream):
    state = int("".join(stream[:16][::-1]), 2)
    for i in range(16, len(stream)):
        state = f_inverse(state)
        if not compute_output_bit(state, pred) == int(stream[i]):
            return None
    state = f_inverse(state)
    return compute_output_bit(state, pred)

print("All you need to know about f is that it's a function from 16 bits to 16 bits")
print("The output on today's secret seed is:", f(seed))
if __name__ == "__main__":
    while not done:
        choice = input("What can I do for you? 1. get random bits 2. use f 3. predict next bit 4. guess seed ").strip()
        if choice == "1":
            rand_pred = secrets.randbelow(2**16)
            output = prng(rand_pred)
            print(output)
            print("Using predicate", rand_pred)
            print("Ignore the fact that the first 16 bits are always the same (or don't, your choice)")
        elif choice == "2":
            if function_uses == 15:
                print("Nah, you've had enough.")
                continue
            num = input("Gimme a number! ").strip()
            try:
                num = int(num)
                if num < 0 or num >= 2**16:
                    print("Out of range!")
                else:
                    print(f(num))
                    function_uses += 1
            except:
                print("Uh something went wrong.")
        elif choice == "3":
            if oracle_uses == 16:
                print("Nah, you've had enough.")
                continue
            stream = input("Gimme the bitstream you want to predict! ").strip()
            if len(stream) < 16:
                print("Out of range!")
            else:
                pred = input("Oh, can you also give a predicate with that? ").strip()
                try:
                    pred = int(pred)
                    if pred < 0 or pred >= 2 ** 64:
                        print("Out of range!")
                    else:
                        output = pprngc(pred, stream)
                        if output is None:
                            print("Uh lemme get back to you on that...")
                            print("*liquidates assets, purchases fake identity, buys one way ticket to Brazil*")
                            done = True
                        else:
                            print(output)
                            oracle_uses += 1
                except:
                    print("Uh something went wrong.")
        elif choice == "4":
            guess = input("Well, let's see it! ").strip()
            if str(seed) == guess:
                print(flag)
            else:
                print("Nope! Sorry!")
            done = True
        else:
            print("Buh bye!")
            done = True
