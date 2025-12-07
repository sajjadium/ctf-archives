import hashlib
import random
import json
from secret import flag

RSP = ['Rock', 'Scissors', 'Paper']
HASH_LIST = ['md5', 'sha1', 'sha256']
SALT_MAX = 10
ROUND = 2000

class Alice:
    def __init__(self):
        self.rsp_list = [random.choice(RSP) for _ in range(ROUND)]
        self.hash_choice = [random.choice(HASH_LIST) for _ in range(ROUND)]
        self.index = 0
    
    def hash(self, rspnsalt):
        if self.hash_func == 'md5':
            return hashlib.md5(rspnsalt).hexdigest()
        elif self.hash_func == 'sha1':
            return hashlib.sha1(rspnsalt).hexdigest()
        elif self.hash_func == 'sha256':
            return hashlib.sha256(rspnsalt).hexdigest()
        else:
            pass

    def next(self):
        self.rsp = self.rsp_list[self.index].encode()
        self.salt = random.randbytes(SALT_MAX-len(self.rsp))
        self.hash_func = self.hash_choice[self.index]
        self.hash_val = self.hash(self.rsp + self.salt)
        self.index += 1
        return {"my_hash" : self.hash_val}, {"rsp" : self.rsp.decode(), "salt" : self.salt.hex(), "hash_func" : self.hash_func}
    
    def verify(self, rsp, salt, hash_func, hash_val):
        self.hash_func = hash_func
        return bytes.fromhex(self.hash(rsp.encode() + salt)) == hash_val
    
class Game:
    def __init__(self):
        self.score = 0

    def judge(self, Alice, you):
        rules = {"Rock" : "Scissors", "Scissors" : "Paper", "Paper" : "Rock"}
        if Alice == you:
            self.draw()
        elif rules[you] == Alice:
            self.win()
        else:
            self.lose()

    def win(self):
        print('win')
        self.score +=1
    def lose(self):
        print('lose')
        self.score +=0
    def draw(self):
        print('draw')
        self.score +=0
    def result(self):
        return self.score > 1600

def main():
    print("""======================================
this is rock scissors paper game
you must win 1600 times in 2000 chance
======================================""")
    game = Game()
    alice = Alice()
    for _ in range(ROUND):
        first_submit, second_submit = alice.next()
        print(f'this is my hash -> {json.dumps(first_submit)}')
        try:
            recv = json.loads(input("what is your hash?\n"))
            recv_hash = bytes.fromhex(recv['my_hash'])
        except Exception as e:
            print(e)
            exit(0)
        print(f'this is my rsp, salt and hash_func -> {json.dumps(second_submit)}')
        try:
            recv = json.loads(input("what is your conponents?\n"))
            rsp = recv["rsp"]
            salt = bytes.fromhex(recv["salt"])
            hash_func = recv["hash_func"]
        except Exception as e:
            print(e)
            exit(0)
        assert alice.verify(rsp, salt, hash_func, recv_hash)
        game.judge(second_submit['rsp'], rsp)

    if game.result():
        print(flag)
        print(game.score)
    else:
        print('fail')
        print(game.score)
        exit(0)

if __name__ == "__main__":
    main()
