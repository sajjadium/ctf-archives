
global allowed , matrix_entries
allowed = "%UQh13S2dbjj,V6K1g$PTdaN4f!T023KUe#hi0PMOQiVN&cOcLR74+MLfeSgbaR*"
matrix_entries = 37*37 


class Cipher :

    def __init__(self, master_pass) :

        self.n = len(master_pass)
        self.key = [ord(i) for i in master_pass]
        self.mod = len(allowed)

    def create_key(self) :
        S= []
        for i in range(self.mod) :
            S.append(i)
        j = 0
        i = 0
        for i in range(self.mod - 1) :
            i = (i + 1) % self.mod 
            j = (j + S[i] + self.key[i%self.n]) %self.mod    
            S[i], S[j] = S[j], S[i]
        return S 
    
    def gen_stream(self , S , lgth = matrix_entries) :
        i = j = 0
        global key_stream
        key_stream = []
  
        for k in range(0, lgth):
            i = (i + 1) % self.mod
            j = (j + S[i]) % self.mod

            t = (S[i]+S[j]) % self.mod
            key_stream.append(S[t])
  

        return key_stream 
def get_entries(master_pass , lgth = matrix_entries) :
    obj = Cipher(master_pass)
    l = list(map(lambda x: allowed[x],obj.gen_stream(obj.create_key(),lgth)))
    return l

if __name__ == "__main__" :
    import random
    master_pass_len = 2**(random.choice(range(1,7)))
    master_pass = ''.join(chr(random.randint(0,64)) for i in range(master_pass_len))
    f = open("master_pass.key","w")
    f.write(master_pass)
    f.close()



