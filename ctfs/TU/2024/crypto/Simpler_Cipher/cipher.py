import time

exptables=[REDACTED]

def main():
    while(2>1):
        time.sleep(2)
        inp = input('''Please Select Your Mode\n
                    [1] Encrypt a message with a custom key
                    [2] Decrypt a message 
                    [3] Get the flag 
                    [4] Exit
                    \n''')
        if not(inp in ('1','2','3','Encrypt a message with a custom key','Decrypt a message','Get the flag','4','Exit')):
            print('Sorry, please try again!')
        else:
            if inp=='1' or inp=='Encrypt a message with a custom key':
                try:
                    encrypt()
                except Exception as e:
                    print('Error Encrypting! Please try again\n' + e)
            elif inp=='2' or inp=='Decrypt a message':
                try:
                    decrypt()
                except Exception as e:
                    print('Error decrypting!  Please try again\n' + e)
            elif inp=='4' or inp=='Exit':
                return True
            else:
                try:
                    getFlag()
                except:
                    print('Error getting flag! Please try again')

def encrypt():
    pt = str(input('Enter your plaintext: '))
    try:
        key = input('Enter your 6 byte key (ex. 0011AABBCCDD): ').strip()
        binKey = str(bin(int('1'+key,base=16)))[3:]
    except:
        print('Invalid Key! Please ensure that your input is 6 bytes!')
        return -1
    if(len(binKey)!=48):
        print('Error with key! Please ensure key is 6 bytes long!')
        return -1
    binPT=''
    for chr in pt:
        binPT+='{0:08b}'.format(ord(chr)) 
    binCText=''
    binPT=pad(binPT)
    for i in range(0,len(binPT),48):
        binCText+=expand(xor(binPT[i:i+48],binKey))
    print('\nYour ciphertext is: \n' + binCText+'\n\n')


def decrypt():
    ctext = str(input('Enter your ciphertext as binary (ex. 0011001101010101000011110000000011111111): ')).strip()
    try:
        key = input('Enter your 6 byte key (ex. 0011FFDDCCBB): ').strip()
        binKey = str(bin(int('1'+key,base=16)))[3:]
    except:
        print('Invalid Key! Please ensure that your input is 6 bytes!')
        return -1
    if(len(binKey)!=48):
        print('Error with key! Please ensure key is 6 characters long!')
        return -1
    binPText=''
    for i in range(0,len(ctext),72):
        binPText+=xor(unexpand(ctext[i:i+72]),binKey)
    decodedMessage=''
    for i in range(0,len(binPText),8):
        decodedMessage+=str(chr(int(binPText[i:i+8],2))) 
    print('\nHere is your plaintext back: \n ' + decodedMessage+'\n\n')

def getFlag():
    print('''
          111100010001010001101000000101110001010001100001100001100001000101101010010010010001100001101010000101010010111000011001010001101110111000101110010010010001111000000101101101110001010001110001010001000101000101111100010010010101000101110001111000010101100001011001010001011110011001010001101010010010100001010010010001011001111000110011010001010010010001010101111100101010100001101010101101110001100001010001011001110011000101100001010010110011101101010010100001110011011001101101101101011001101101100001
          ''') 


def unexpand(ctext):
    unexp = ''
    for i in range(0,len(ctext),6):
        for j in range(0,4):
            try:
                lsb = exptables[j].index(ctext[i:i+6])
                unexp += '{0:02b}'.format(j)
                unexp += '{0:02b}'.format(lsb)
            except:
                continue
    return unexp


def pad(ptext): ##DONE 
    if len(ptext)%48!=0:
        bytesToAdd = (48-(len(ptext)%48))//8
        for i in range(0,bytesToAdd):
            ptext+='{0:08b}'.format(i)   
    elif len(ptext)==0:
        raise ValueError("Invalid plaintext length")    
    return ptext


def xor(ptext,key):
    text=''
    for i in range(0,48):
        text+=str(int(ptext[i])^int(key[i]))
    return text


def expand(ctext):
    ct=''
    for i in range(0,len(ctext),4):
        msb = ctext[i:i+2]
        lsb = ctext[i+2:i+4]
        exp = exptables[int(msb,2)][int(lsb,2)]
        ct+=exp
    return ct


if __name__=='__main__':
    main()
