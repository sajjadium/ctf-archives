import pickle
import base64
import sys
import pickletools

def check_flag(flag_guess: str):
  """REDACTED FOR PRIVACY"""

cucumber = base64.b64decode(input("Give me your best pickle (base64 encoded) to taste! "))

for opcode, _, _ in pickletools.genops(cucumber):
  if opcode.code == "c" or opcode.code == "\x93":
    print("Eww! I can't eat dill pickles.")
    sys.exit(0)

pickle.loads(cucumber)
