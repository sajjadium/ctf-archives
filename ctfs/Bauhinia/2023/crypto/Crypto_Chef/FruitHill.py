# Found a fruit hill!
# Let's use the fruits here too!

import galois # galois is used just because it's more lightweighted when compared to sage 
import numpy as np

class Fruit:

    def __init__(self, q, n, secret_sauce):
        
        self.n = n
        self.GF = galois.GF(q)
        self.SS = self.GF(secret_sauce)
        self.madness = 0
        self.tolerance = 100

    # Do you know what is msg? msg makes everything good. If your dish is not delicious, add msg.
    # If your life is not good, add msg, it will be a lot better.
    def cook(self, msg):
        if self.madness >= self.tolerance:
            print("I feel like you are not trying to learn with me but just want to steal my secret sauce from me!")
            raise Exception("Bad guy.")
        assert len(msg) == self.n
        self.madness += 3.84
        msg = self.GF(msg)
        tastyDish = self.SS @ msg
        return tastyDish
    
    # Verify whether you really add the msg in that tasty dish!
    def verify(self, tastyDish, msg):
        tastyDish = self.GF(tastyDish)
        msg = self.GF(msg)
        taste = np.linalg.inv(self.SS) @ tastyDish
        return np.all(taste == msg)
        