from fastecdsa.curve import P192
from fastecdsa.point import Point
from secrets import randbelow,flag,banner,menu
from Crypto.Util.number import bytes_to_long,inverse
from string import ascii_uppercase
import json
#P192 Order
O=6277101735386680763835789423176059013767194773182842284081
d=randbelow(O)
G=Point(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012, 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811,curve=P192)
P=d*G

def pub_hash(m):
     return (bytes_to_long(m.encode())%O)>>60 
def ecdsa_sign(m):
        h = pub_hash(m)
        k = randbelow(O)
        r = (k * G).x % O
        s = (inverse(k, O) * (h + r * d)) % O
        return json.dumps({"r":r,"s":s})
def verify(msg,r,s):
    h=pub_hash(msg)
    if r > 0 and r < O and s > 0 and s < O:
        u1=(h*inverse(s,O))%O
        u2=(r*inverse(s,O))%O
        V=u1*G+u2*P
        if r==V.x:
            return True
    return False
print(banner)
print(menu)
normal_user=["JAKC","YASSINE"]
for i in range(2):
    try:
            
        choice=json.loads(input())
        if "option" not in choice or "name" not in choice:
            print("Give me a option and a message next time")
            continue
        if choice["option"]=="sign":
            name=choice["name"]
            if any(i not in ascii_uppercase for i in name) or len(name)!=40:
                print("give me a strong and long name next time")
            normal_user.append(name)
            payload=json.dumps({"username":name,"admin":"false"})
            print(ecdsa_sign(payload))
        if choice["option"]=="verify_admin":
            if "r" not in choice or 's' not in choice :
                print("Remember to return with the admin signature next time")
                continue
            if choice["name"] in normal_user:
                print("Dont Try to cheat your way through!")
                continue
            payload=json.dumps({"username":choice["name"],"admin":"truee"})
            if verify(payload,choice['r'],choice['s']):
                print("Welcome back admin",flag)
            else:
                print("You seemed to send something wrong try again")
                continue
    except:
        pass

        
          
          
     