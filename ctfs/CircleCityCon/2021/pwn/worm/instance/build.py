import os
import random
import subprocess
import shutil

max_depth = int(os.environ["MAX_DEPTH"])

name = lambda i: i % 2
left_index = lambda i: 2 * i + 1
right_index = lambda i: 2 * i + 2
parent = lambda i: (i - 1) // 2
depth = lambda i: (i + 1).bit_length()


def build_node(i):
    d = depth(i)
    os.chmod(".", 0o550)
    if d == max_depth:
        shutil.chown(".", f"user{d}", f"user{d}")
    else:
        shutil.chown(".", f"user{d}", f"user{d + 1}")
        shutil.copyfile(f"/keys/key{d + 1}", "./key")
        shutil.chown("./key", f"user{d + 1}", f"user{d}")
        os.chmod("./key", 0o4550)
        subprocess.run(["setcap", "cap_setuid,cap_setgid=ep", "./key"])


def build_tree(i=0):
    if depth(i) > max_depth:
        return

    os.mkdir(f"room{name(i)}")
    os.chdir(f"room{name(i)}")

    build_tree(left_index(i))
    build_tree(right_index(i))

    build_node(i)
    os.chdir("..")


def plant_flag():
    os.chdir("room0")
    while len(os.listdir()) > 0:
        os.chdir(f"room{random.randint(0, 1)}")

    os.rename("/flag.txt", "./flag.txt")


print(f"[*] Building tree with {2 ** max_depth - 1} nodes ...")
build_tree()
print("[*] Planting flag in a random leaf node ...")
plant_flag()
print("[+] Ready")
