import hashlib

def flagify(f):
    fl = str(int(f)**5)
    l1 = list(fl)
    l2 = [115, 110, 102, 60, 75, 69, 114, 112, 51, 43, 87, 50, 91, 89, 43, 106, 94, 47, 43, 49, 44, 122]
    flag = []
    for i in range(len(l1)):
        flag.append(chr(int(l1[i])+l2[i]))
    return "".join(flag)

code = input("Enter the code:")
chk = "6799b5a7f2b55b86346ba9cc9fe1b5239282274a46d4c63bb78bf17223f8ca8d"
if chk == hashlib.sha3_256(code.encode()).hexdigest():
    print("Inside the suitcase you find a dozen eggs!\nAlso, " + flagify(code))
else:
    print("The suitcase doesn't open")