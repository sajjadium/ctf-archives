#!/usr/bin/python3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import random
import binascii

flag = open('flag.txt','rb').read().decode("utf-8");

class AESCipher:
    def __init__(self):
        self.BLOCK_SIZE = 16;
        self.key = get_random_bytes(self.BLOCK_SIZE);

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

    def crissCross(self,a,b):
        assert(len(a) == len(b));
        n = len(a) * 4;
        a = int(a,16) % (1 << (n // 2));
        b = int(b,16) >> (n // 2);
        uwu = 0;
        for i in range(n):
            if(i % 2 == 1):
                uwu += ((a >> (i // 2)) & 1) << i;
            else:
                uwu += ((b >> (i // 2)) & 1) << i;
        return hex(uwu)[2:].zfill(32);

    def encryptHex(self,iv,pt):
        assert(len(bytes.fromhex(pt)) % self.BLOCK_SIZE == 0);
        ct = iv;
        prevXOR = iv;
        for i in range(0,len(pt),2 * self.BLOCK_SIZE):
            curBlock = pt[i:i + 2 * self.BLOCK_SIZE];
            e = self.encryptSingleBlock(self.xorHex(curBlock,prevXOR));
            ct += e;
            prevXOR = self.crissCross(curBlock,e);
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
            prevXOR = self.crissCross(p,curBlock);
        return pt;

    def pad(self,msg):
        l = (len(msg) % (2 * self.BLOCK_SIZE)) // 2;
        if(l == 0):
            msg = hex(self.BLOCK_SIZE)[2:] * self.BLOCK_SIZE + msg;
        else:
            msg = hex(self.BLOCK_SIZE - l)[2:].zfill(2) * (self.BLOCK_SIZE - l) + msg;
        return msg;


    def remove_padding(self,msg):
        c = int(msg[:2],16);
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
            print("The player failed the sussy test D:");
            return;
        iv = ct[:32];
        c = ct[32:];
        msg = self.decryptHex(iv,c);
        msg = self.remove_padding(msg);
        msg = self.check_MAC(msg);
        if msg:
            if len(msg[:-8]) == 2 * int(msg[-8:],16):
                print("The player is an imposter!");
            else:
                print("The player failed the sussy test D:");
        else:
            print("The player failed the sussy test D:");
        return;

cipher = AESCipher()

Welcome = "I created the new hit game Amongst Us! But I feel like the currently available cbc modes aren't on theme enough... I know! I will will make the Sussy CBC :D"
print(Welcome);
options = """Select an option:
Encrypt a message so that only the other imposters can understand (E)
See if a message is valid to check if another player is also an imposter (V)
""";
while True:
    e_or_v = input(options);
    if("e" in e_or_v.lower()):
        sussy = input("Please enter your sussy message: ");
        message = """I think the burning philosophical question must be asked, in that, what is the purpose of life? Think of an imposter. He was born that way, and we can't expect him to understand the expectations of our polite society! It's simply absurd to demand that he goes against his nature, so is he wrong for just existing, wrong for being born? If so, then why are we the arbitrater of morality and philosophy, what bequeaths us the rights of such judgement? And ofc, you may say that {0}, but I disagree, because you are not sussy enough!!! Anywho, here's flag: {1}""".format(sussy,flag);
        print("Sussified message: {}".format(cipher.encrypt(message)));
    elif("v" in e_or_v.lower()):
        cryptic = input("Please input the other player's sussy message for verification: ")
        cipher.decrypt(cryptic);
