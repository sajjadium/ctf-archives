from random import randint 

FLAG = "grey{fake_flag}"

print("Lo and behold! The GreyCat Wizard, residing within the Green Tower of PrimeLand, is a wizard of unparalleled prowess")
print("The GreyCat wizard hath forged an oracle of equal potency")
print("The oracle hath the power to bestow upon thee any knowledge that exists in the world")
print("Gather the requisite elements to triumph over the three trials, noble wizard.")
print()

a = int(input("The first element: "))
b = int(input("The second element: "))
print()

all_seeing_number = 23456789

# FIRST TRIAL
if b <= 0:
    print("Verily, those who would cheat possess not the might of true wizards.")
    exit(0)

if pow(all_seeing_number, a - 1, a) != 1:
    print("Alas, thy weakness hath led to defeat in the very first trial.")
    exit(0)

# SECOND TRIAL
trial_numbers = [randint(0, 26) for i in range(26)]

for number in trial_numbers:
    c = a + b * number 
    if pow(all_seeing_number, c - 1, c) != 1:
        print("Thou art not yet strong enough, and thus hast been vanquished in the second trial")
        exit(0)

# THIRD TRIAL
d = a + b * max(trial_numbers) 
if (d.bit_length() < 55): 
    print("Truly, thou art the paramount wizard. As a reward, we present thee with this boon:")
    print(FLAG)
else:
    print("Thou art nigh, but thy power falters still.")