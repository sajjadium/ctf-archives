class Matrix:
    def __init__(self,dims , A=None) :
        self.rows = dims[0]
        self.cols = dims[1]
        if(A == None)  :
            self.M = [[0] * self.cols for i in range(self.rows)]
        else :
            self.M = A
        
    def __str__(self) :
        m = ""
        for i in range(self.rows) :
            m += str(self.M[i])+"\n"
        return m
    def __add__(self,other) :
        C = Matrix(dims = (self.rows,self.cols))
        if isinstance(other,Matrix) :
            for i in range(self.rows) :
                for j in range(self.cols) :
                    C.M[i][j] = self.M[i][j] + other.M[i][j]
        else :
            print("Not matching type")
        return C
    def __radd__(self,other) :
        return self.__add__(other)
    def __mul__(self, other) :

        if isinstance(other,Matrix) :
            C = Matrix(dims = (self.rows,other.cols))
            for i in range(self.rows) :
                for j in range(other.cols) :
                    acc = 0
                    for k in range(other.rows) :
                        acc += self.M[i][k] * other.M[k][j]
                    #print(acc)
                    C.M[i][j] = acc
        else :
            C = Matrix(dims = (self.rows,self.cols))

            for i in range(self.rows) :
                for j in range(self.cols) :
                    C.M[i][j] = self.M[i][j] * other
        return C
    def __rmul__(self,other) :
        return self.__mul__(other)

    def __getitem__(self,key) :
        if isinstance(key, tuple) :
            i = key[0]
            j = key[1]
            return self.M[i][j]
    def __setitem__(self,key,value) :
        if isinstance(key,tuple) :
            i = key[0]
            j = key[1]
            self.M[i][j] = value
    def __sub__(self,other) : 
        C = Matrix(dims = (self.rows,self.cols)) 
        if isinstance(other,Matrix) : 
            for i in range(self.rows) : 
                for j in range(self.cols) : 
                    C.M[i][j] = self.M[i][j] - other.M[i][j] 
        else : 
            print("Not matching type") 
        return C 
    def __rsub__(self,other) : 
        return self.__sub__(other)


if __name__ == "__main__" :
    X = [[1,2,3],[4,5,6],[7,8,9]]                       
    Y = [[10,11,12],[13,14,15],[16,17,18]]              
    R = [[84,90,96],[201,216,231],[318,342,366]]        
    X = Matrix((3,3),X)                                 
    Y = Matrix((3,3),Y)                                 
    Res = X.__mul__(Y).M                                

    assert Res == R
    print("Script successful")