import sympy 
flag = open('flag','r').read()
admin = False
adminKey = (7024170033995563248669070948202275621832659349979887130360116095557494224289964760016097751188998415, 3170315055328760291009922771816122, 250376935805204674013389241468539348499776429965769848974957007209785494103442398289504600645160477724, 43395542902454917488842651277236247)
publicKey = 51133059403872132269736212485462945485381032580683758205093039961914793947944949374017744787298892843604322756848647643991762827932760
def verify(key):
    if key==adminKey:
        if not admin:
            print("Sorry, you must be an admin to use this key.")
            return False
        return True
    if sympy.sympify(sympy.sqrt(key[0]*key[0]*key[3]*key[3]+key[1]*key[1]*key[2]*key[2])).is_integer and sympy.sympify(4*key[0]*key[2])/(key[1]*key[3])==publicKey and sympy.gcd(key[0],key[1])==1 and sympy.gcd(key[2],key[3])==1 and sympy.sympify(key[0])/key[1]<sympy.sympify(key[2])/key[3] and len(str(key[0]))>3000and len(str(key[1]))>3000and len(str(key[2]))>3000and len(str(key[3]))>3000:
        return True
    return False
print("Hello! To open this vault, you must provide the correct password.")
if verify((int(input("First key: ")),int(input("Second key: ")),int(input("Third key: ")),int(input("Fourth key: ")))):
    print("You're in!")
    print(flag)
else:
    print("Incorrect. Better luck next time.")