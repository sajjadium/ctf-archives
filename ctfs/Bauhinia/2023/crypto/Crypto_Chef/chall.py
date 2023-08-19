import galois
import numpy as np
import base64

from OV import OilVinegar
from FruitHill import Fruit

from secret import WATER_TAP, flag

def getPepperOrSalt(q, v):
    return galois.GF(q).Random(v // 2)

def getSauce(q, n):
    secret_sauce = galois.GF(q).Random((n, n))
    while np.linalg.matrix_rank(secret_sauce) < n:
        secret_sauce = galois.GF(q).Random((n, n))
    return secret_sauce

def vec2Hex(vec):
    vec = np.char.mod('%x', vec.view(np.ndarray))
    return ''.join(vec)

def encodeRecipe2Pub(recipe2):
    return ':'.join([vec2Hex(pub.flatten()) for pub in recipe2.pub])

def printRecipesPub(recipe1, recipe2):
    print("=========================================================================")
    print(f"Recipe 1: Sorry this recipe is highly secret so I cannot give you any info about it!")
    print(f"Recipe 2: {encodeRecipe2Pub(recipe2)}")
    print("=========================================================================")


def main():
    
    k = 4
    q = 2**k
    o = 16
    v = 16
    n = o + v

    assert len(WATER_TAP) == (k * (v // 2)) # WATER_TAP is ont-hot encoding of the water tabs
    salt = getPepperOrSalt(q, v)
    pepper = getPepperOrSalt(q, v)
    secret_sauce = getSauce(q, n)
    
    recipe1 = Fruit(q, n, secret_sauce)
    recipe2 = OilVinegar(q, o, v, WATER_TAP, salt, pepper, secret_sauce)

    print("Please give me the following two dishes!")
    print("1. Cooked with recipe 1 using the MSG 'cryptochefisgood'")
    print("2. Cooked with recipe 2 using the MSG 'ilovemsg'")
    print("Oh yes, unlike other chef, I am very strict on it.")
    print("I won't check whether you have added the MSG in the dish, but would require you to have the EXACT SAME dish as mine!")
    print("Of course, you can cook a few dishes with me to learn my style first.")

    comm_limit = 38
    exam_status = [False, False]

    try:
        for comm_count in range(1, comm_limit + 1):
            
            cmd = input(f"[{comm_count}/{comm_limit}] > ")
            args = cmd.split(' ')

            if args[0] == 'pub':
                printRecipesPub(recipe1, recipe2)
                
            elif args[0] == 'cook':
                rec, msg_hex = int(args[1]), args[2]

                if rec != 1 and rec != 2:
                    raise Exception("Invalid recipe!")
                recipe = recipe1 if rec == 1 else recipe2

                msg = bytes.fromhex(msg_hex)
                if msg == b'cryptochefisgood' or msg == b'ilovemsg':
                    raise Exception("Sorry, but you have to learn the dishes yourself!")
                
                msg_vec = [int(c, 16) for c in msg_hex]
                print(f"Cooked dish: {vec2Hex(recipe.cook(msg_vec))}")
            
            elif args[0] == 'check':
                rec, sig_hex, msg_hex = int(args[1]), args[2], args[3]

                if rec != 1 and rec != 2:
                    raise Exception("Invalid recipe!")
                recipe = recipe1 if rec == 1 else recipe2

                sig_vec = [int(c, 16) for c in sig_hex]
                msg_vec = [int(c, 16) for c in msg_hex]

                if recipe.verify(sig_vec, msg_vec):
                    print("Yes! This dish is made from that msg.")
                else:
                    print("Hum... Seems a bit off.")
            
            elif args[0] == 'exam':
                rec, dish_hex = int(args[1]), args[2]

                if rec != 1 and rec != 2:
                    raise Exception("Invalid recipe!")
                recipe = recipe1 if rec == 1 else recipe2
                
                if exam_status[rec - 1]:
                    print("You have already passed the exam on that recipe! Please choose the another one!")
                    continue
                
                target_msg = b'cryptochefisgood' if rec == 1 else b'ilovemsg'
                target_msg = [int(c, 16) for c in target_msg.hex()]
                dish = [int(c, 16) for c in dish_hex]

                if not np.array_equal(recipe.cook(target_msg), dish):
                    print("Hum... Please come again after you have sharpened your cooking skills.")
                    exit(0)
                
                exam_status[rec - 1] = True
                if exam_status[0] and exam_status[1]:
                    print("Congratulations! You have mastered all the recipes!")
                    print(f"Here's your reward: {flag}")
                    exit(0)
                else:
                    print("Nice! You have mastered this recipe!")
                    print("Please continue on your journey!")
        
        print("Too slow! Please come again after you have sharpened your cooking skills :(")

    except Exception:
        print("Nope.")

if __name__ == '__main__':
    main()