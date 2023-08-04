import random
import string

characters = string.printable[:-6]
digits = string.digits
ascii_letters = string.ascii_letters


def Ran_str(seed : int, origin: str):
    random.seed(seed)
    random_sequence = random.sample(origin, len(origin))
    return ''.join(random_sequence)

rseed = int(input())
assert rseed <= 1000 and rseed >= 0

map_string1 = Ran_str(rseed, characters)
map_string2 = Ran_str(rseed * 2, characters)
map_string3 = Ran_str(rseed * 3, characters)


def util(flag):
    return flag[9: -1]

def util1(map_string: str, c):
    return map_string.index(c)

def str_xor(s: str, k: str):
    return ''.join(chr((ord(a)) ^ (ord(b))) for a, b in zip(s, k))

def mess_sTr(s : str, index : int):
   
    map_str = Ran_str(index, ascii_letters + digits)
    new_str = str_xor(s, map_str[index])
    
    if not characters.find(new_str) >= 0:
        new_str = "CrashOnYou??" + s
    
    return new_str, util1(map_str, s)
    

def crypto_phase1(flag):
    flag_list1 = util(flag).split('_')
    newlist1 = []
    newlist2 = []
    index = 1
    k = 0
    for i in flag_list1:
        if len(i) % 2 == 1:
            i1 = ""
            for j in range(len(i)):
                p, index = mess_sTr(i[j], index)
                i1 += p
           
            p, index = mess_sTr(i[0], index)
            i1 += p
            
            i1 += str(k)
            k += 1
            newlist1.append(i1)
        
        else:
            i += str(k)
            k += 1
            newlist2.append(i)
    
    return newlist1, newlist2
        
def crypto_phase2(list):
    newlist = []
    for i in list:
        str = ""
        for j in i:
            str += map_string1[util1(map_string3, j)]
           
        newlist.append(str)
    return newlist

def crypto_phase3(list):
    newlist = []
    for i in list:
        str = ""
        for j in i:
            str += map_string2[util1(map_string3, j)]
            
        newlist.append(str)
    return newlist

def crypto_final(list):
    str=""
    for i in list[::-1]:
        str += i
    return str

if __name__ == '__main__':
    format="sixstars{XXX}"
    flag="Nothing normal will contribute to a crash. So when you find nothing, you find A Crashhhhhhhh!!! "   
    
    flaglist1, flaglist2 = crypto_phase1(flag)
    cipher = crypto_final(crypto_phase3(crypto_phase2(flaglist1) + flaglist1) + crypto_phase2(crypto_phase3(flaglist2)))
    
    print("map_string2: " + map_string2)
    print("cipher: " + cipher)
    
    
