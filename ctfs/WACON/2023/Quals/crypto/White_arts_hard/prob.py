import math
import os
from Generator import Generator1, Generator2, Generator3, Generator4, Generator5

query_left = 266

def guess_mode(G, query_num):
    for _ in range(query_num):
        q = bytes.fromhex(input("q? > "))
        inverse = input("inverse(y/n)? > ") == 'y'
        assert len(q) == G.input_size
        print(G.calc(q, inverse).hex())
    
    # Time to guess
    assert input("mode? > ") == str(G.mode) # 0(gen) / 1(random)
        
def challenge_generator(challenge_name, Generator):
    global query_left
    print(f"#### Challenge = {challenge_name}")
    query_num = int(input(f"How many queries are required to solve {challenge_name}? > "))
    query_left -= query_num
    for _ in range(40):
        G = Generator()
        guess_mode(G, query_num)


challenge_generator("Generator1", Generator1)
challenge_generator("Generator2", Generator2)

if query_left < 0:
    print("You passed all challenges for EASY but query limit exceeded. Try harder :(")
    exit(-1)

print("(Only for a junior division) Good job! flag_baby =", open("flag_baby.txt").read())

challenge_generator("Generator3", Generator3)

if query_left < 0:
    print("You passed all challenges for EASY but query limit exceeded. Try harder :(")
    exit(-1)

print("Good job! flag_easy =", open("flag_easy.txt").read())

challenge_generator("Generator4", Generator4)
challenge_generator("Generator5", Generator5)

if query_left < 0:
    print("You passed all challenges for HARD but query limit exceeded. Try harder :(")
    exit(-1)

print("(Only for general/global divisions) Good job! flag_hard =", open("flag_hard.txt").read())
