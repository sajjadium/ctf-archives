#!/usr/bin/python3
import sys
import random, time
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA256
from Crypto.Util.number import inverse

MASTER_KEY = DSA.generate(1024)
USER_KEY = None
CHALL = None
LAST_SIGNED_MSG = None

def get_opts():
   opt = 0
   while opt < 1 or opt > 4:
      print("1) Generate DSA Key")
      print("2) Set DSA Key")
      print("3) Sign Message")
      print("4) Send Message")
      print("Enter an option: ", end="")
      opt = int(input())
      print("\n")
   return opt


def gen_user_key():
   global USER_KEY
   USER_KEY = DSA.generate(1024)
   print("---YOUR KEY PARAMETERS---")
   print(f"y = {USER_KEY.y}")
   print(f"g = {USER_KEY.g}")
   print(f"p = {USER_KEY.p}")
   print(f"q = {USER_KEY.q}")
   print(f"x = {USER_KEY.x}\n\n")


def set_user_key():
   global USER_KEY
   print("---ENTER KEY PARAMETERS---")
   print("y = ", end="")
   y = int(input())
   print("g = ", end="")
   g = int(input())
   print("p = ", end="")
   p = int(input())
   print("q = ", end="")
   q = int(input())
   print("x = ", end="")
   x = int(input())
   print("\n")
   try:
      USER_KEY = DSA.construct((y,g,p,q,x))
   except:
      print("---INVALID DSA KEY---\n\n")


def hash_msg(msg):
   msg_bytes = bytes(msg, "ascii")
   h = SHA256.new(msg_bytes).digest()
   return int.from_bytes(h, "big")


def sign(msg, key, sender):
   global LAST_SIGNED_MSG
   h = hash_msg(msg)
   k = 0
   if sender == "YOU":
      while k < 2 or k >= key.q:
         try:
            print("---ENTER A MAX K FROM 3 TO Q---")
            max = int(input())
            assert(max > 2 and max <= key.q)
            print("\n")
            k = random.randrange(0, max)
         except:
            k = 0
            print("---MAX K MUST BE FROM 3 TO Q---\n")
   else:
      k = random.randrange(2, key.q)

   kinv = inverse(k, key.q)
   r = pow(key.g, k, key.p) % key.q
   s = kinv * (h + r * key.x) % key.q
   if sender == "YOU":
      print("---K GENERATED FOR SIGNATURE---")
      print(f"{k}\n")
      print("---YOUR SIGNED MESSAGE---")
      print(f"MSG: {msg}")
      print(f"R:   {r}")
      print(f"S:   {s}\n\n")
      LAST_SIGNED_MSG = (msg,r,s)
   return (r, s)


def verify(msg, r, s, key):
   h = hash_msg(msg)
   w = inverse(s, key.q)
   u1 = (h * w) % key.q
   u2 = (r * w) % key.q
   u1 = pow(key.g, u1, key.p)
   u2 = pow(key.y, u2, key.p)
   v = (u1 * u2) % key.p % key.q
   if r == v:
      return True
   else:
      return False


def send_message(msg, r, s, key, sender):
   global MASTER_KEY
   print(f"########################### MESSAGE FROM {sender} ###########################")
   print(f"MSG: {msg}")
   print(f"R:   {r}")
   print(f"S:   {s}")
   print("########################################################################\n\n")
   if sender == "YOU":
      recv_message(msg, r, s)


def recv_message(msg, r, s):
   global USER_KEY, MASTER_KEY
   for i in range(3):
      print("\r",end="")
      print("."*(i+1),end="")
      sys.stdout.flush()
      time.sleep(.75)
   print("\n\n")
   if verify(msg, r, s, MASTER_KEY):
      if msg == "COMMAND: TAKE CONTROL":
         msg = "Oh... that's quite clever of you..."
         r, s = sign(msg, MASTER_KEY, "ALI")
         send_message(msg, r, s, MASTER_KEY, "ALI")
         print("---WELCOME KEYMASTER---")
         flag_file = open("flag.txt", "r")
         flag = flag_file.read()
         print(f"{flag}\n\n")
         sys.exit()
      else:
         print("---INVALID COMMAND---\n\n")
   elif verify(msg, r, s, USER_KEY):
      if msg == "COMMAND: TAKE CONTROL":
         msg = "HAH! Nice try, foolish human."
         r, s = sign(msg, MASTER_KEY, "ALI")
         send_message(msg, r, s, MASTER_KEY, "ALI")
      else:
         msg = "I find your conversation boring and disinteresting, simple human."
         r, s = sign(msg, MASTER_KEY, "ALI")
         send_message(msg, r, s, MASTER_KEY, "ALI")
      return
   msg = "Human, I cannot even verify that message was from you."
   r, s = sign(msg, MASTER_KEY, "ALI")
   send_message(msg, r, s, MASTER_KEY, "ALI")


# ASCII art from https://www.asciiart.eu/space/aliens
print("                _____")
print("             ,-\"     \"-.")
print("            / o       o \\")
print("           /   \     /   \\")
print("          /     )-\"-(     \\")
print("         /     ( 6 6 )     \\")
print("        /       \ \" /       \\")
print("       /         )=(         \\")
print("      /   o   .--\"-\"--.   o   \\")
print("     /    I  /  -   -  \  I    \\")
print(" .--(    (_}y/\       /\y{_)    )--.")
print("(    \".___l\/__\_____/__\/l___,\"    )")
print(" \                                 /")
print("  \"-._      o O o O o O o      _,-\"")
print("      `--Y--.___________.--Y--'")
print("         |==.___________.==|")
print("         `==.___________.=='\n")
print("Greetings Earthling, let us engage in telecommunication between our ships.")
print("To ensure validity, here are my parameters for verification with DSA.\n")
print(f"y = {MASTER_KEY.y}")
print(f"g = {MASTER_KEY.g}")
print(f"p = {MASTER_KEY.p}")
print(f"q = {MASTER_KEY.q}\n")
print("I have built a system for us to communicate over. Do not fret your little mind over it, it is quite simple\nto use, it even allows you to generate your own K.")
print("I ask that you do not send any commands to my ship, it is not like it would believe YOU were its owner.\n\n")

for request in range(700):
   match get_opts():
      case 1:
         gen_user_key()
      case 2:
         set_user_key()
      case 3:
         if type(USER_KEY) != DSA.DsaKey:
            print("---ERROR: KEY IS NOT SET---\n\n")
         else:
            print("---ENTER YOUR MESSAGE---")
            msg = input()
            print("\n")
            sign(msg, USER_KEY, "YOU")
      case 4:
         if type(USER_KEY) != DSA.DsaKey:
            print("---ERROR: KEY IS NOT SET---\n\n")
         elif LAST_SIGNED_MSG == None:
            print("---ERROR: NO MESSAGES HAVE BEEN SIGNED---\n\n")
         else:
            send_message(LAST_SIGNED_MSG[0], LAST_SIGNED_MSG[1], LAST_SIGNED_MSG[2], USER_KEY, "YOU")

msg = "You have thoroughly bored me human, see you never."
r,s = sign_message(msg, MASTER_KEY, "ALI")
send_message(msg, r, s, MASTER_KEY, "ALI")
