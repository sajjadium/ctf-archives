from Crypto.Util.number import *
from random import randrange
from secret import flag

def pr(msg):
    print(msg)

pr(br"""
                        ....''''''....                        
                     .`",:;;II;II;;;;:,"^'.                    
                  '"IlllI;;;;;;;;;;;;;Il!!l;^.                 
                `l><>!!!!!!!!iiiii!!!!!!!!i><!".               
             ':>?]__++~~~~~<<<<<<<<<<<<<<<<~~+__i".            
           .:i+}{]?-__+++~~~~~~<<<<<~~~~~~+_-?[\1_!^           
          .;<_}\{]-_++~<<<<<<<<<<<<<<<<<<<~+-?]\|]+<^          
          .!-{t|[?-}(|((){_<<<<<<<<<_}1)))1}??]{t|]_"          
           !)nf}]-?/\){]]]_<<<<<<<<<_]]}}{\/?-][)vf?`          
          '!tX/}]--<]{\Un[~~<<<<<~~<~-11Yz)<--?[{vv[".         
         .<{xJt}]?!ibm0%&Ci><<<<<<<<!0kJW%w+:-?[{uu)},         
          !1fLf}]_::xmqQj["I~<<<<<<>"(ZqOu{I^<?[{cc)[`         
          `}|x\}]_+<!<+~<<__~<<<<<<+_<<_+<><++-[1j/(>          
           !\j/{]-++___--_+~~<i;I>~~~__-______?}(jf}`          
            ;~(|}?_++++~~++~+]-++]?+++~~~~+++-[1/]>^           
              ;\([?__+_-?]?-_-----__-]?-_+++-]{/].             
               l||}?__/rjffcCQQQQQLUxffjf}+-]1\?'              
                ,[\)[?}}-__[/nzXXvj)?__]{??}((>.               
                 .I[|(1{]_+~~~<~~<<<~+_[}1(1+^                 
                    ,~{|\)}]_++++++-?}1)1?!`                   
                      ."!_]{11))1{}]-+i:'                      
                          .`^","^`'.                           
""".decode())

def gen_prime(bit):
    while 1:
        P = getPrime(bit)
        if len(bin(P)) - 2 == bit:
            return P

pq_bit = 512
offset = 16

P,Q = [gen_prime(pq_bit) for i in range(2)]
N = P * Q
gift = int(bin(P ^ (Q >> offset))[2+offset:],2)
pr(N)
pr(gift)

inpP = int(input())
if inpP != P:
    pr(b"you lose!")
    exit()

secret = randrange(0,P)
bs = [randrange(0,P) for _ in range(38)]

results = [(bi * secret) % P for bi in bs]
rs = [ri & (2 ** offset - 1)  for ri in results]

pr(bs)
pr(rs)
inpsecret = int(input())
if inpsecret == secret:
    pr(flag)