#!/usr/bin/python3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import random
import binascii

flag = open('flag.txt','rb').read().decode("utf-8");

class YourDidItRNG:
    def __init__(self,size):
        self.mask = (1 << size) - 1;
        self.mod = 79563462179368165893806602174110452857247538703309854535186209058002907146727;
        self.seed = 0;

    def infuseYourDidItPower(self,power,step):
        self.seed = (step * power) % self.mod;

    def next(self):
        self.seed = ((self.seed * 573462395956462432646177 + 7453298385394557473) % self.mod); # try converting these to text ;)
        return self.seed & self.mask;

    def yourdidit(self,goodjob):
        # Priming the your did it star power!
        for i in range(5 * 5):
            self.next();
        # It is known that the Your Did it star has 5 sides and 5 vertices. Thus, we must combine its powers 5 times for the ultimate Your Did It Star Power!
        YourSoDidIt = self.next() | self.next() | self.next() | self.next() | self.next();
        YourSoDidIt = ((YourSoDidIt & goodjob) ^ self.next()) & self.mask;
        return YourSoDidIt;

class YourDidItAESCipher:
    def __init__(self):
        self.BLOCK_SIZE = 16;
        self.key = get_random_bytes(self.BLOCK_SIZE);
        self.YourDidIt = YourDidItRNG(self.BLOCK_SIZE * 8);

    def encryptSingleBlock(self,block):
        assert(len(bytes.fromhex(block)) == self.BLOCK_SIZE);
        cipher = AES.new(self.key,AES.MODE_ECB);
        return cipher.encrypt(bytes.fromhex(block)).hex().zfill(32);

    def decryptSingleBlock(self,block):
        assert(len(bytes.fromhex(block)) == self.BLOCK_SIZE);
        cipher = AES.new(self.key,AES.MODE_ECB);
        return cipher.decrypt(bytes.fromhex(block)).hex().zfill(32);

    def xorHex(self,a,b):
        assert(len(a) == len(b));
        return hex(int(a,16) ^ int(b,16))[2:].zfill(32);

    def YourDidItCalculator(self,a):
        a = int(a,16);
        owo = self.YourDidIt.yourdidit(a);
        return hex(owo)[2:].zfill(32);

    def encryptHex(self,iv,pt):
        assert(len(bytes.fromhex(pt)) % self.BLOCK_SIZE == 0);
        ct = iv;
        prevXOR = iv;
        for i in range(0,len(pt),2 * self.BLOCK_SIZE):
            curBlock = pt[i:i + 2 * self.BLOCK_SIZE];
            e = self.encryptSingleBlock(self.xorHex(curBlock,prevXOR));
            ct += e;
            self.YourDidIt.infuseYourDidItPower(int(e,16),i);
            prevXOR = self.YourDidItCalculator(curBlock);
        return ct;

    def decryptHex(self,iv,ct):
        assert(len(bytes.fromhex(ct)) % self.BLOCK_SIZE == 0);
        prevXOR = iv;
        pt = "";
        for i in range(0,len(ct),2 * self.BLOCK_SIZE):
            curBlock = ct[i:i + 2 * self.BLOCK_SIZE];
            d = self.decryptSingleBlock(curBlock);
            p = self.xorHex(d,prevXOR);
            pt += p;
            self.YourDidIt.infuseYourDidItPower(int(curBlock,16),i);
            prevXOR = self.YourDidItCalculator(p);
        return pt;

    def pad(self,msg):
        l = (len(msg) % (2 * self.BLOCK_SIZE)) // 2;
        if(l == 0):
            msg = hex(self.BLOCK_SIZE)[2:] * self.BLOCK_SIZE + msg;
        else:
            msg = hex(self.BLOCK_SIZE - l)[2:].zfill(2) * (self.BLOCK_SIZE - l) + msg;
        return msg;


    def check_padding(self,msg):
        c = int(msg[:2],16);
        for i in range(c):
            if(int(msg[i * 2:i * 2 + 2],16) != c):
                return False;
        return msg[2 * c:];


    def check_MAC(self,msg):
        h = hashlib.sha1()
        mac = binascii.unhexlify(msg[-40:]);
        lastBlock = binascii.unhexlify(msg[-40 - 2 * 20 - 8:-40 - 8]);
        h.update(lastBlock);
        if(h.digest() == mac):
            return msg[:-40];
        else:
            return False;

    def encrypt(self,pt):
        iv = ''.join(random.choice("0123456789abcdef") for _ in range(32));
        h = hashlib.sha1()
        h.update(pt[-20:].encode("utf-8"));

        msg = self.pad(pt.encode("utf-8").hex() + hex(len(pt))[2:].zfill(8) + h.digest().hex());
        return self.encryptHex(iv,msg);

    def decrypt(self,ct):
        if(len(ct) % (2 * self.BLOCK_SIZE) != 0):
            print("Your did not do it D:");
            return;
        iv = ct[:32];
        c = ct[32:];
        msg = self.decryptHex(iv,c);
        msg = self.check_padding(msg);
        if not msg:
            print("Your did not do it D:");
            return;
        msg = self.check_MAC(msg);
        if msg:
            if len(msg[:-8]) == 2 * int(msg[-8:],16):
                print("YOUR DID IT!");
            else:
                print("Your did not do it D:");
        else:
            print("Your did not do it D:");
        return;

cipher = YourDidItAESCipher()

Welcome = "UwU the Your Did It Star wants to see if Your can did this challenge. I've heard that even the yourdidit star's cipher is different because of how yourdidit it is! Can you break it?"
print(Welcome);
options = """Select an option:
Encrypt a message so that yourdidit star can understand (E)
See if a message can be understood by the yourdidit star to check if your did it or not (V)
""";
while True:
    e_or_v = input(options);
    if("e" in e_or_v.lower()):
        yourdidit = input("Please enter your pre-yourdidit message: ");
        message = """There is something to be said about the your did it star. That somehow, despite its childishly cartoonish aesthetics (or perhaps more likely, because of), the people LOVE it. Such is the appeal of modern art, the decomposition and unraveling of conventions, mocking it through ironic depicitons, thus engendering sincerity. Sincerity? How could irony be a source of sincerity, you may ask. We as a society are so used to the insincere messages at the end of some grand services. The "thank you for choosing us" after the Airline cancelled your plane and rebooked you for one 30 hours after, and the "Great job!" on standard exams after you clearly bombed it. It is as if they don't acutally care about the message. They are but blindly following the nicities of yesterday's, churning out phrases one after the other. Thus, the Your Did It star stands as a beacon of sincerity and irony. The organizers know that most contestants probably didn't do as well as they hoped -- they didn't solve a problem despite their best efforts, they couldn't implement a solution before the time ran out, or they simply did worse than they wanted to. After all, there are only so many winners. Most don't stand out. So the Your Did It Star tells them: "It's ok! I know you probably didn't do so well, just like how I am not well-drawn. But it doesn't matter, because you had fun solving the problems, and ultimately this is just a silly contest. So regardless of what happened, your did it, even if your did it not so well." But you may argue that {0}. But I disagree!!! Because YOUR DID NOT DO IT!!!!!! Anywho, thanks for coming to my Ted-Talk. Here's the flag: {1}""".format(yourdidit,flag);
        print("Yourdidit-fied message: {}".format(cipher.encrypt(message)));
    elif("v" in e_or_v.lower()):
        cryptic = input("Please input a yourdidit message for verification: ")
        cipher.decrypt(cryptic);
