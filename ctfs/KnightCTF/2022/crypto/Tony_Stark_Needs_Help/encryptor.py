secret = input("Enter your string to encrypt: ")

key = input("Enter the key: ")

secarr = []

keyarr = []

x = 0
 
def keyfunc(key,keyarr,x):

    for character in key:

        keyarr.append(ord(character))

    for i in keyarr:

        x += i

def secretfucn(secret,secarr,key,x):

    for character in secret:

        secarr.append(ord(character))

    for i in range(len(secarr)):

        if 97 <= secarr[i] <= 122:
            
            secarr[i] = secarr[i]-6
        else:
            if 65 <= secarr[i] <= 90:
                
                secarr[i] = secarr[i]-11

    if len(key) % 2 == 0:

        x = x + 1

    else:

        x = x + 3

    if x % 2 == 0:

        secarr[i] = secarr[i] + 3

    else:

        secarr[i] = secarr[i] + 2

    encrypted = ""

    for val in secarr:

        encrypted = encrypted + chr(val)

    print("Encrypted Text: " + encrypted)

            
keyfunc(key,keyarr,x)

secretfucn(secret,secarr,key,x)

