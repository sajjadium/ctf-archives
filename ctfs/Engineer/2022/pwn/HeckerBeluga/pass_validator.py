def ValidatePassword(password):
    valid = False
    print("Attempting to validate password...")

    if(len(password[::-2]) != 8):
        print("Nah, you're not even close!!")
        return False

    pwlen = len(password)
    chunk1 = 'key'.join([chr(0x98 - ord(password[c])) 
                            for c in range(0, int(pwlen / 2))])
    if "".join([c for c in chunk1[::4]]) != '&e"3&Ew*':
        print("Seems you're a terrible reverse engineer, come back after gaining some skills!")
        return False

    chunk2 = [ord(c) - 0x1F if ord(c) > 0x60
                  else (ord(c) + 0x1F if ord(c) > 0x40 else ord(c))
                  for c in password[int(pwlen / 2) : int(2 * pwlen / 2)]]
    rand = [54, -45, 9, 25, -42, -25, 31, -79]
    for i in range(0, len(chunk2)):
        if(0 if i == len(chunk2) - 1 else chunk2[i + 1]) != chunk2[i] + rand[i]:
            print("You're not a real hecker, try again! " + str(i))
            return False
        
    print("Password accepted!")
    return True

print("\n************** Password Validator ***************")
print("Please enter password")
while True:
    if  ValidatePassword(input()):
        exit()
    else:
        print("Try again!")
