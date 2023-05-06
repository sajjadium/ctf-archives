import random
from sympy import *
from Crypto.Util.number import *

welcome_message = "Nowadays, clients just keep changing their requirements. They said e=65537 is too boring for RSA and that they wanted a dynamic encryption system instead. Oh, I'll give it to them!";
print(welcome_message);

flag = open('flag.txt','rb').read();

m = bytes_to_long(flag);
e = 65537;
p = getPrime(200);
q = getPrime(200);
random.seed(e);
phi = (p-1) * (q-1);
n = p * q;
ct = pow(m, e, n)
print("My secret flag is " + str(ct));

def gcd(a,b):
  # Client said the loading screen is too boring
  # So they want something with more flair and movement while they wait
  if(a == 0):
    return b;
  if(b == 0):
    return a;
  print(".,"[(b // a) & 1], end = "");

  return gcd(b % a,a);

# Clients keep complaining that making e always 65537 is too boring
# So they changed their requirements and wanted a "dynamic encryption system"
# I literally can't
def e_gen():
  print("Loading", end = "")
  test_e = nextprime(random.randint(1, 100000));
  # Okay but I literally can't use a random e if gcd is not 1
  # It's like most fundamental part of RSA!!!
  new_e = test_e // gcd(test_e,phi);
  print()
  return new_e

while True:
  inp = input("Guess Private Key (1) or Encrypt Message (2): ");
  if (inp == "1"):
    d = int(input("Enter Private Key: "));
    print(long_to_bytes(pow(ct, d, n)));
    exit()
    
  elif (inp == "2"):
    test_e = e_gen()
    inp = bytes_to_long(input("Enter Message: ").encode());
    test_ct = pow(inp, test_e, n);
    print("Your Message (remember to convert): " + str(test_ct));
    
  else:
    print("BAD OPTION");
    exit();