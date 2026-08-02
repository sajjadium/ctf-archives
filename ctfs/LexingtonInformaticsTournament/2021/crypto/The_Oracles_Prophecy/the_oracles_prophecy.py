#!/usr/bin/python3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import random
import binascii

spell = open('flag.txt','rb').read().decode("utf-8");

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

    def encryptHex(self,iv,pt):
        assert(len(bytes.fromhex(pt)) % self.BLOCK_SIZE == 0);
        ct = iv;
        prevXOR = iv;
        for i in range(0,len(pt),2 * self.BLOCK_SIZE):
            curBlock = pt[i:i + 2 * self.BLOCK_SIZE];
            e = self.encryptSingleBlock(self.xorHex(curBlock,prevXOR));
            ct += e;
            prevXOR = self.xorHex(curBlock,e);
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
            prevXOR = self.xorHex(curBlock,p);
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
        if(c > 0 and c < 17):
            return msg[2 * c:];
        else:
            return False;

    def check_MAC(self,msg):
        h = hashlib.sha1()
        mac = binascii.unhexlify(msg[-40:]);
        lastBlock = binascii.unhexlify(msg[223 * 2:239 * 2]);
        h.update(lastBlock);
        if(h.digest() == mac):
            return True;
        else:
            return False;

    def encrypt(self,pt):
        iv = ''.join(random.choice("0123456789abcdef") for _ in range(32));
        h = hashlib.sha1()
        h.update(pt[223:239].encode("utf-8"));
        msg = self.pad(pt.encode("utf-8").hex() + h.digest().hex());
        return self.encryptHex(iv,msg);

    def decrypt(self,ct):
        if(len(ct) % (2 * self.BLOCK_SIZE) != 0):
            print("Something went wrong while fulfilling the prophecy D:");
            return;
        iv = ct[:32];
        c = ct[32:];
        msg = self.decryptHex(iv,c);
        msg = self.check_padding(msg);
        if(msg):
            if self.check_MAC(msg):
                print("The prophecy is fulfilled!");
            else:
                print("Something went wrong while fulfilling the prophecy D:");
        else:
            print("Something went wrong while fulfilling the prophecy D:");
        return;

cipher = AESCipher()

Welcome = "Welcome, Great Wizard of Orz. You have arrived at the holy Oracle."
print(Welcome);
options = """Select an option:
Make a prophecy sound cryptic (E)
Fulfill a prophecy by decrypting it (V)
""";
while True:
    e_or_v = input(options);
    if("e" in e_or_v.lower()):
        prophecy = input("Please enter your prophecy: ");
        message = """Double, double toil and trouble;
Fire burn and caldron bubble.
When midnight strikes and the god dislikes,
I swear on my soul that
{0}
{1}
In thunder, lightning, and in rain.
Father of omens! Give me blood beyond sight!
""".format(spell,prophecy);
        print("Cryptic Prophecy: {}".format(cipher.encrypt(message)));
    elif("v" in e_or_v.lower()):
        cryptic = input("Please input the cryptic prophecy: ")
        cipher.decrypt(cryptic);
