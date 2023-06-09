import sys
import ast
def check_factors(a,b,ab):
    if abs(a)<=1 or abs(b)<=1:
        print("too easy")
        return False
    if type(a*b) == float:
        print("no floats please")
        return False
    return a*b == ab 


factors = [4,10,0x123120,38201373467,247867822373,422943922809193529087,3741]

for composite in factors:
    print(f"Factor {composite}")
    a = ast.literal_eval(input("a:").strip())
    b = ast.literal_eval(input("b:").strip())
    
    if check_factors(a,b,composite):

        continue
    break
else:
    print("Here is your Flag. Good Job!")
    print(open("flag.txt").read())

