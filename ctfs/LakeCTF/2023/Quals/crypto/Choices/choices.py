import random, string
flag = ''.join(random.SystemRandom().sample(string.ascii_letters, 32))
print(f"EPFL{{{flag}}}")
open("output.txt", "w").write(''.join(random.choices(flag, k=10000)))
