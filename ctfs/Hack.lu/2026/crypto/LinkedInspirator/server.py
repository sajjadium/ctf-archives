#!/usr/bin/env python3

import random
import os

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad

FLAG = os.getenv("FLAG") or "flag{dummy}"

KEY = bytes.fromhex(os.getenv("KEY", 32 * "0"))

if len(KEY) != 16:
    raise ValueError("Invalid key length.")

BANNER = r"""
  _    _      _          _ ___              _          _           
 | |  (_)_ _ | |_____ __| |_ _|_ _  ____ __(_)_ _ __ _| |_ ___ _ _ 
 | |__| | ' \| / / -_) _` || || ' \(_-< '_ \ | '_/ _` |  _/ _ \ '_|
 |____|_|_||_|_\_\___\__,_|___|_||_/__/ .__/_|_| \__,_|\__\___/_|  
                                      |_|                            

Note: Your favorite LinkedIn quote generator has recently moved its truly inspirational quotes behind the Pro tier to keep up with rapidly scaling infrastructure demands.

Already purchased Pro for yourself or your team? Redeem the activation token associated with your Account ID from your billing confirmation.
"""

FREE_QUOTES = (
    "You miss 100% of the shots that you don't hit.",
    "The secret of getting ahead is getting further than all the others.",
    "Every expert was once someone who wasn't an expert.",
    "Fortune favors the bald.",
    "The road to success is paved with road.",
    "Rome wasn't built.",
    "The early bird gets up earlier than the late bird.",
    "There is light at the end of every tunnel with a light at the end.",
    "Great things come to those who receive great things.",
    "A penny saved is still just a penny.",
    "Time heals all wounds, except the ones requiring actual treatment.",
    "Money can't buy happiness, but neither can having no money.",
)
FREE_HASHTAGS = [
    "#ShowerThoughts",
    "#WordsToLiveBy",
    "#SilentBattles",
    "#LifeLessons",
    "#DarkestMoments",
    "#SuccessMindset",
    "#PersonalGrowth",
    "#SelfGrowth",
    "#Motivation",
    "#Impact",
    "#SeekTheTruth",
    "#AncientWisdom",
    "#Inspiration",
    "#HiddenKnowledge",
]


def xor_blocks(b: bytes, blocksize=16) -> bytes:
    if len(b) % blocksize != 0:
        raise ValueError("Input must contain complete blocks.")
    res = bytearray(blocksize)
    for i in range(0, len(b)):
        res[i % blocksize] ^= b[i]
    return bytes(res)


class Session:
    def __init__(self):
        self.sub_state = "free"
        self.user_id = ""
        self.username = ""

    def set_name(self, name: str) -> str:
        self.username = name
        self.user_id = SHA256.new(name.encode()).hexdigest()
        return f"Account ID: {self.user_id}"

    def upgrade(self, inp: str) -> str:
        try:
            inp_b = bytes.fromhex(inp)
        except ValueError:
            return "Invalid activation token format."

        if len(inp_b) < 16 * 3 or len(inp_b) % 16 != 0:
            return "Invalid activation token format."

        iv, ct, auth_tag = inp_b[:16], inp_b[16:-16], inp_b[-16:]
        cipher = AES.new(KEY, mode=AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(ct), 16)

        if pt.decode("latin-1").strip() != f"uid: {self.user_id}; tier: pro":
            return "Activation token does not match this account."

        auth_tag_dec = AES.new(KEY, AES.MODE_ECB).decrypt(auth_tag)
        if auth_tag_dec != xor_blocks(pt):
            return "Activation token integrity check failed."

        self.sub_state = "pro"
        return f"Welcome to Pro, {self.username}. Your thought leadership journey starts now."

    def get_quote(self) -> str:
        if self.sub_state == "pro":
            return f"Exclusive Pro insight: {FLAG}"
        tags = " ".join(random.sample(FREE_HASHTAGS, k=random.randint(1, 4)))
        return random.choice(FREE_QUOTES) + " " + tags


def main():
    session = Session()
    print(BANNER)
    try:
        print("Ready to be inspired?")
        print(session.set_name(input("Username: ")))
        print(f"Subscription state: {session.sub_state}\n")
        while True:
            print("Available operations: get_inspirational_quote, upgrade, exit")
            op = input("> ").strip().lower()
            try:
                match op:
                    case "upgrade":
                        print(session.upgrade(input("Pro activation token: ")))
                    case "get_inspirational_quote":
                        print(session.get_quote())
                    case "exit":
                        return
                    case _:
                        print("This operation does not exist.")
            except ValueError:
                pass
            print()
    except EOFError:
        return


if __name__ == "__main__":
    main()
