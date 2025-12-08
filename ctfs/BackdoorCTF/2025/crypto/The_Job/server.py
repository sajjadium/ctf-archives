import random
rand = random.SystemRandom()
from flag import FLAG
k = 256
mod = 10**9+7
hash_table = [[] for i in range(k)]
print("Your friend, a full stack developer, was asked to implement a hash table by his boss. Your friend, being an experienced individual, created a hash table which has 256 slots, and each slot can hold multiple values using a linked list.\n\nWhen a number arrives as input, it will be hashed and if the hash is x, the number will be inserted into the xth slot of the hash table at the end of the respective list. Although, if the xth slot doesn't exist, the program will die.\n")
print("However when he went to submit his code, he was presented with an unreasonable request. His manager demands that the inputs need to be equally divided among all slots. So, the difference in sizes of any two slots of the table should not be 2 or more.\n\nNow, your friend is not an expert when it comes to hashing. So, he comes to you, a cryptography genius. All you have to do is create a hash polynomial that equally divides the input. The polynomial will be evaluated on the input number and the remainder from the modulus 1e9+7 will be taken as the hash to determine the slot where that number goes.\nFor example: if the polynomial is x^2 + 2x - 3, and the input is 5: f(5) = 32 mod 1000000007. So it will go into slot 32. (slots are from 0 to k-1)\n")
print("Now even your friend knows that this task is impossible. So he took the help of your unethical hacker friend to leak the input numbers on which his manager will test the hash table.\n")

input("Press Enter to start > ")

n = 896
number_array = [rand.randint(0,mod-1) for i in range(n)]
while len(set(number_array))!=n:
    number_array = [rand.randint(0,mod-1) for i in range(n)]

print(f"Here are the leaked numbers : {','.join([str(num) for num in number_array])}\n")
coeff_str = input("Enter the coefficients of the polynomial.\nExample: if the polynomial is x^2 + 2x - 3, Enter 1,2,1000000004\nThe degree of the polynomial should be less than the count of input numbers.\n> ")
try:
    coeff_arr = list(map(int,coeff_str.split(',')))
except:
    print("Incorrect input format")
    exit()
if len(coeff_arr)>n:
    print("The degree of the polynomial should be less than the count of input numbers.")
    exit()
coeff_arr = [coeff%mod for coeff in coeff_arr]

def get_hash(num,coeff_arr):
    hash = 0
    mult = 1
    for i in range(len(coeff_arr)):
        hash = (hash + mult * coeff_arr[len(coeff_arr)-1-i])%mod
        mult = (mult*num)%mod
    return hash

for i in range(n):
    hash = get_hash(number_array[i],coeff_arr)
    if hash>=k:
        print(f"Input {i} : Faulty Hash function! Slot {hash} doesn't exist.")
        exit()
    hash_table[hash].append(number_array[i])

for i in range(k):
    if len(hash_table[i])>(n+k-1)/k:
        print("You have failed your friend in need. How can you be called a cryptography genius, if you can't even forge a hash function. Go back to solving ciphers. Maths isn't your thing.")
        exit()

print("You have successfully created a hash that your friend can use. You retain your title as the cryptography genius.\n")

print("OR SO YOU THOUGHT. Turns out your friend is not a genius himself. While creating the architecture for the hash table, he inserted a random value into the a random index of the hash table. Now everytime you use an empty hash table, it's never empty. There is always one extra number in one particular index which can ruin your plans of dividing all inputs equally.\n")

print("Your friend doesn't remember which index he used. And he can't modify the architecture of the hash table since he has already submitted it.\n\nBut he has 6 free trials provided by his manager. Where he can submit a hash polynomial and the manager will tell if the hash table is balanced or not (if the difference between the maximum size at any index and minimum size at any index is less than 2).\n")

print("Now the mission falls back to you. You have to devise valid hash polynomials that the manager will test and tell if the hash table is balanced or not. And at the end of all free trials, you have to tell which index contains the unnecessary number.\n\n*The input numbers will remain the same as previously leaked.\n")

input("Press Enter to continue > ")

target = rand.randint(0,k-1)
junk = rand.randint(0,mod-1)

for turn in range(6):
    print(f"Trial {turn+1} : ")
    coeff_str = input("Enter the coefficients of the polynomial.\n> ")
    try:
        coeff_arr = list(map(int,coeff_str.split(',')))
    except:
        print("Incorrect input format")
        exit()
    coeff_arr = [coeff%mod for coeff in coeff_arr]
    if len(coeff_arr)>n:
        print("The degree of the polynomial should be less than the count of input numbers.")
        exit()
    hash_table = [[] for i in range(k)]
    hash_table[target].append(junk)
    for num in number_array:
        hash = get_hash(num,coeff_arr)
        if hash>=k:
            print(f"Input {i} : Faulty Hash function! Slot {hash} doesn't exist.")
            exit()
        hash_table[hash].append(number_array[i])
    good = True
    for i in range(k):
        if len(hash_table[i])>(n+k-1)/k:
            good = False
            print("Manager says the hash failed in distributing input equally.\n\n")
            break
    if good:
        print("Manager says the hash passed in distributing input equally\n\n")

try:
    index = int(input("Tell your friend the index : "))
except:
    print("Wrong format, Enter an integer.")
    exit()
if index != target:
    print("Your friend tried to remove the number at the index you told him. The hash table crashed a burned. Your friend has lost the job.")
    exit()
else:
    print("Your friend tried to remove the number at the index you told him. It worked! You have saved your friend's job.\n")
print("You truly are a cryptography genius!")
print(f"Here is the flag : {FLAG}")
