
from crypto import get_entries
import math, string
from sage.all import EllipticCurve, Integer
from matrix import *



class Tabula:  
    def __init__(self) :  
        self.E = EllipticCurve(GF(37),[1,5])   
        self.G = self.E.gen(0)  
        global d,allowed 
        allowed = "abcdefghijKLMNOPQRSTUV0123467!#$%&*+,"  
        d = {}  
        for i in range(37) :   
            d[allowed[i]] = self.E.points()[i+1]   
        self.A = [[-1,5,-1],[-2,11,7],[1,-5,2]]  
        self.rows = 37
        self.table = [[' ']*self.rows for i in range(self.rows)]
        
    def update_table(self, rows , table_entries) :
        self.rows = rows
        for i in range(rows) :
            for j in range(rows) :
                self.table[i][j] = table_entries[i*rows + j]
            #print(self.table[i])


    
    def map_matrix(self, m) :
        inf = self.E.points()[0]  
        row = 3   
        col = math.ceil(len(m)/3)  
        E_arr = []  
        ind = 0
        for i in range(row) :   
            tmp = []  
            for j in range(math.ceil(len(m)/3)) :     
                if ( ind < len(m)) :   
                    tmp.append( d[m[ind]] )  
                else  :   
                    tmp.append(inf)
                ind += 1
            E_arr.append(tmp)  

        return Matrix((row,col),E_arr)

    def encrypt(self,m) : 
        mat = [[-1,5,-1],[-2,11,7],[1,-5,2]]
        A = Matrix((3,3), mat)
        P = self.map_matrix(m)
        Q = A.__mul__(P)

        (C1,C2) = (P.__mul__(25), Q.__add__(P.__mul__(325))) 
        points = []
        for i in range(P.rows) :
            for j in range(P.cols) :
                c1 = C1.M[i][j]
                c2 = C2.M[i][j]

                points.append(((c1[0],c1[1]),(c2[0],c2[1])))
                if((i*P.rows + j) == len(m)) :
                    break
        return points
    def gen_pass(self, website, master_pass , pass_len) :
        """
            website     : name of the website you want to generate the password for eg: www.amazon.com
            master_pass : master password for your stateless password manager
            pass_len    : length of the password to be generated/retrieved for the website
        """
        site = website.split(".")[1]
        entries = get_entries(master_pass)
        self.update_table( 37, entries) 
        table_row = sum([ord(i) for i in site])%self.rows 
        #print("website :", website)
        pswd = ''.join([self.table[table_row][i] for i in range(pass_len)])
        points = self.encrypt(pswd)
        pswd_set = [(self.table[points[i][0][0]][points[i][1][1]],(points[i][0],points[i][1])) for i in range(pass_len)]
        #print(pswd_set)
        pswd = ''.join(p[0] for p in pswd_set)
        return pswd
if __name__ == "__main__" :
    obj = Tabula()
    #master_pass = open("master_pass.key").read()
    #print(obj.gen_pass("www.gameison.com",master_pass,12))

