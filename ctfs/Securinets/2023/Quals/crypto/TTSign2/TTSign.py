#!/usr/bin/env python3.10
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import os, sys, hashlib
from random import randint
import json 

from APTX import Server,Client

rsa = RSA.generate(2048)


print("""
 /$$$$$$$$ /$$$$$$$$        /$$$$$$  /$$$$$$  /$$$$$$  /$$   /$$
|__  $$__/|__  $$__/       /$$__  $$|_  $$_/ /$$__  $$| $$$ | $$
   | $$      | $$         | $$  \\__/  | $$  | $$  \\__/| $$$$| $$
   | $$      | $$         |  $$$$$$   | $$  | $$ /$$$$| $$ $$ $$
   | $$      | $$          \\____  $$  | $$  | $$|_  $$| $$  $$$$
   | $$      | $$          /$$  \\ $$  | $$  | $$  \\ $$| $$\\  $$$
   | $$      | $$         |  $$$$$$/ /$$$$$$|  $$$$$$/| $$ \\  $$
   |__/      |__/          \\______/ |______/ \\______/ |__/  \\__/
""")



class TT_Sign:
    def __init__(self,client):
        self.key = os.urandom(16)
        self.client=client
        self.iv =os.urandom(16)
        self.nounce=os.urandom(16)
        self.msg=self._hash("Integrity is everything")
    def xor(self,x,y):
        return bytes([i^j for i,j in zip(x,y)])
    
    def check_sum(self,param):
        ctr = Counter.new(128, initial_value=bytes_to_long(self.nounce))
        enc_param=AES.new(self.key,AES.MODE_CTR,counter=ctr).encrypt(param)
        h_h=b"\x00"*16
        for i in range(0,len(enc_param),16):
            h_h=bytes(self.xor(h_h,enc_param[i:i+16]))
        return h_h
    
    def _hash(self, data):
        return hashlib.sha512(data.encode()).hexdigest()

    def _parse_keys(self, params):
        lp = bytes_to_long(params[:2])
        params = params[2:]
        p = bytes_to_long(params[:lp])
        params=params[lp:]
        integrety_check1=params.index(b"U cant fool me")+1
        params = params[integrety_check1+13:]
        lq = bytes_to_long(params[:2])
        params = params[2:]
        q = bytes_to_long(params[:lq])
        params=params[lq:]
        integrety_check2=params.index(b"Guess this one")+1
        params =  params[integrety_check2+13:]
        ld = bytes_to_long(params[:2])
        params = params[2:]
        d = bytes_to_long(params[:ld])
        return d, p, q,integrety_check1-1,integrety_check2-1
    
    def _get_proof(self, ref):
        transfer,err=self.client.get_transfer_by_ref(ref)
        if transfer["sender"]!=self.client.username:
            return "\nYou can only sign your transaction\n"
        self.msg=f"ref:{transfer['ref']};from:{transfer['sender']};to:{transfer['receiver']};amount:{str(transfer['amount'])};label:{transfer['label']}"
        assert len(self.msg) < 256
        s, enc_params = self._sign()
        return f"{s.hex()}|{enc_params.hex()}"      
    def prepare_param(self,pad1=randint(24,42),pad2=randint(24,42)):
        d_bytes = long_to_bytes(rsa.d)
        p_bytes = long_to_bytes(rsa.p)
        q_bytes = long_to_bytes(rsa.q)
        params = long_to_bytes(len(p_bytes), 2) + p_bytes+b"\x00"*pad1+b'U cant fool me'
        params += long_to_bytes(len(q_bytes), 2) + q_bytes+b"\x00"*pad2+b"Guess this one"
        params += long_to_bytes(len(d_bytes), 2) + d_bytes
        return params
    
    def _sign(self):
        h = int(self._hash(self.msg), 16)
        s = pow(h, rsa.d, rsa.n)
        self.nounce=os.urandom(16)
        params=self.prepare_param()  
        params_padded=pad(params,16)+self.check_sum(pad(params,16))
        enc_params = self.iv + AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(params_padded)
        return long_to_bytes(s), enc_params

    def _create_transfer(self):
        receiver = str(input("Receiver: "))
        amount = int(input("Amount: "))
        label = str(input("Label: "))
        ref ,err= self.client.set_transfer(receiver, amount, label)
        if len(err)==0:
            print(f"Here is your reference: {ref},sign it to finilize transaction here is your signature {self._get_proof(ref)}\n\n")
        else:
            print(err)
    def _sign_transfer(self):
        ref=str(input("ref: "))
        proof = str(input("Proof: "))
        s, enc_params = proof.split('|')
        s = int(s, 16)
        enc_params = bytes.fromhex(enc_params)
        if self._verify(self.msg, s,ref, enc_params):
            self.client.update_transfer(ref)
        else:
            print("Failed to sign the transaction !")

    def _verify(self, msg, s,ref, enc_params):
        transfer,err=self.client.get_transfer_by_ref(ref)
        if len(err)!=0:
            print("Transaction doesnt exist !")
            return False
        msg=f"ref:{transfer['ref']};from:{transfer['sender']};to:{transfer['receiver']};amount:{str(transfer['amount'])};label:{transfer['label']}"
        h = int(self._hash(msg), 16)
        params = AES.new(self.key, AES.MODE_CBC, enc_params[:16]).decrypt(enc_params[16:])
        sum=params[-16:]
        params=params[:-16]
        d, p, q,pad1,pad2 = self._parse_keys(params)

        if p!=rsa.p or q!=rsa.q and d!=rsa.d:
            print("Dont try to touch my precious parameters")
            return False
        padded_params=self.prepare_param(pad1,pad2)
        new_sum=self.check_sum(pad(padded_params,16))
        if new_sum!=sum:
            print(f"Somedata go corrupted durring transfer {new_sum}")
            return False
        e = inverse(d, (p-1)*(q-1))
        n = p*q
        m = pow(s, e, n)
        if m == h:
            return True
        else:
            print(f"\n[-] Invalid transfer : {long_to_bytes(m).hex()}\n\n")
            return False




def main():
    server = Server()
    
    print(f"~ Welcome to TT_Sign ~")
    print("\nPlease login.")
    username = str(input("Username: "))
    password = str(input("Password: "))

    if server.login(username, password):
        client=Client(username,password)
        tt_sign = TT_Sign(client)
        while True:
                print("1- Create Transfer\n2- Sign Transfer\n3- show info \n4- list Transfers\n")
                choice = str(input("> "))
                if choice == '1':
                    tt_sign._create_transfer()
                elif choice == '2':
                    tt_sign._sign_transfer()
                elif choice == '3':
                    tt_sign.client.show_info()
                elif choice =="4":
                    tt_sign.client.list_transfers()
                elif choice =="5":
                    tt_sign.client.list_clients()
                else:
                    print("\n[-] Invalid Choice!\n\n")


    else:
        sys.exit()

if __name__ == '__main__':
    main()