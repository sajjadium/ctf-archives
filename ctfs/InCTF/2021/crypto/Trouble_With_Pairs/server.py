#!/usr/bin/env python3
from BLS import G2ProofOfPossession as bls
from secret import data, bytexor, fake_flag, flag
from json import loads
import sys


class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream

   def write(self, data):
       self.stream.write(data)
       self.stream.flush()

   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()

   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)


header =    '''We are testing a new Optimised Signature scheme for Authentication in Voting System.

               You can send the Published Result in Specified Format
               Json Format : {'Name' : name, 'Vote' : vote, 'Sign' : signature}
            '''
invalid_json = "Invalid Json!"
invalid_sign = "Invalid signature!"
flag = f"Seems like we could never patch this bug, here is your reward : {bytexor( flag, fake_flag ).hex()}"
fake_flag = f"but, this one is already known, so here is your fake reward : {fake_flag.decode()}"

class Challenge():
    def __init__(self):
        self.data = data
        self.Names = [i["Name"] for i in self.data]
        self.result = []
        for i in range(len(data)):  self.result.append(self.Read(input("> ").strip()))
    

    def Read(self, inp):
        try:
            data = loads(inp)
            Name = data["Name"]
            Vote = data["Vote"]
            Sign = bytes.fromhex(data["Sign"])

            assert Name in self.Names and Vote in ["R","D"]
            
            self.data[self.Names.index(Name)]["Vote"] = Vote
            self.data[self.Names.index(Name)]["Sign"] = Sign
        except:
            print(invalid_json)
            sys.exit()
    

    def Verify_aggregate(self):
        try:
            for j in ["D", "R"]:
                aggregate_sign = bls.Aggregate([i["Sign"] for i in self.data if i["Vote"] == j])
                aggregate_Pk = bls._AggregatePKs([i["PK"] for i in self.data if i["Vote"] == j])
                if not bls.Verify(aggregate_Pk, j.encode(), aggregate_sign):
                    return False
            return True
        except:
            print(invalid_sign)
            sys.exit()


    def Verify_individual(self):
        try:
            return all ( bls.Verify(i["PK"], i["Vote"].encode(), i["Sign"]) for i in self.data)
        except:
            print(invalid_sign)
            sys.exit()


    def Get_Majority(self):
        return max( ["D","R"] , key = lambda j : sum( [ i["Count"] for i in self.data if i["Vote"] == j ] ) )


if __name__ == "__main__":
    print(header)
    challenge = Challenge()

    if challenge.Verify_aggregate():
    
        if challenge.Get_Majority() == "R":
            print("WOW!!!  You found the bug.")
        else:
            print("Everything is Verified and Perfect.")
            sys.exit()
    
    else:
        print("Not Verified!")
        sys.exit()
    
    if challenge.Verify_individual():
        print(flag)
        sys.exit()
    
    else:
        print(fake_flag)
        sys.exit()
