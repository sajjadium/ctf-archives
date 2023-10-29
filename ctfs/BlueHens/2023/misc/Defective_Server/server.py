import enum
import json

CHALLENGES = [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0]

class Challenge(enum.Enum):
    RS = 0
    R = 1

CHALLENGES = [Challenge(c) for c in CHALLENGES]

class Authenticator():
    N: int
    e: int
    ssq: int

    def __init__(self, e: int, N: int, ssq: int):
        self.e = e
        self.N = N
        self.ssq = ssq

    def round(self, rsq: int, ans: int, chal: Challenge)->bool:
        if chal == Challenge.RS and pow(ans,self.e,self.N) == (rsq * self.ssq) % self.N:
            return True
        elif chal == Challenge.R and pow(ans,self.e,self.N) == rsq:
            return True
        else:
            return False
    
def main():
    with open("public_key.json",'r') as f:
        key = json.loads(f.read())

    ssq = key["s^e"]
    e = key['e']
    N = key['N']

    auth = Authenticator(e,N,ssq)

    for challenge in CHALLENGES:
        rsq = int(input().strip())
        print(challenge.value)
        answer = int(input().strip())

        if not auth.round(rsq,answer,challenge):
            return
    
    with open("flag.txt",'r') as f:
        print(f.read())


if __name__ == "__main__":
    main()




    
        
    


