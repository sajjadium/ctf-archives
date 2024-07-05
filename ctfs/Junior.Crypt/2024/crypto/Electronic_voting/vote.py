# pip install lightphe
from lightphe import LightPHE
import pickle
from random import randint

# build a cryptosystem
cs = LightPHE(algorithm_name = 'Paillier')
with open(f'vote/cs.pickle', 'wb') as f:
    pickle.dump(cs, f, protocol=pickle.HIGHEST_PROTOCOL)

N = 250    # number of voting participants 
k = 8      
kand = 6   # number of candidates

# define ciphers
for i in range(N):
    kandid = randint(1,kand)
    
    vote = cs.encrypt(2**(k*(kandid-1)))

    with open(f'vote/vote.{i}.pickle', 'wb') as f:
        pickle.dump(vote, f, protocol=pickle.HIGHEST_PROTOCOL)

