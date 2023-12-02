###
### 
###
def main():
    while(2>1):
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
                except:
                    print('Error Encrypting! Please try again')
            elif inp=='2' or inp=='Decrypt a message':
                try:
                    decrypt()
                except:
                    print('Error decrypting!  Please try again')
            elif inp=='4' or inp=='Exit':
                return True
            else:
                try:
                    getFlag()
                except:
                    print('Error getting flag! Please try again')

def encrypt(): ##DONE 
    pt = str(input('Enter your plaintext: '))
    try:
        key = input('Enter your 6 byte key (ex. 0011AABBCCDD): ').strip()
        binKey = str(bin(int('1'+key,base=16)))[3:]
    except:
        print('Invalid Key! Please ensure that your input is 6 bytes!')
        return -1
    if(len(binKey)!=48):
        print('Error with key! Please ensure key is 6 characters long!')
        return -1
    binPT=''
    for chr in pt:
        binPT+='{0:08b}'.format(ord(chr)) 
    binCText=''
    binPT=pad(binPT)
    for i in range(0,len(binPT),48):
        binCText+=xor(substitution(binPT[i:i+48]),binKey)
    print('\nYour ciphertext is: \n' + binCText+'\n\n')

def decrypt(): #DONE?
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
    for i in range(0,len(ctext),48):
        binPText+=unscramble(xor(ctext[i:i+48],binKey))
    decodedMessage=''
    for i in range(0,len(binPText),8):
        decodedMessage+=str(chr(int(binPText[i:i+8],2)))
    print('\nHere is your plaintext back: \n ' + decodedMessage+'\n\n')


##Key is <Redacted>
## <Redacted>
##Flag is TUCTF{<Redacted>}
def getFlag():##DONE
    print('''11001010000100010010110100101011111001011100101110010010000101011011111111101000111001111101110110110000000
             11001000010011111111101010100111100110001000000110000100001001111000110010101110101111011111000110101101001101
             00010010000011111100001100100100001100110100100100100110111001001010101''')

def substitution(ptext): ##DONE
    pattern = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Redacted
    scrambled = ''
    for i in pattern:
        scrambled += str(ptext[i])
    return scrambled

def pad(ptext): ##DONE 
    if len(ptext)%48!=0:
        bitsToAdd =  48-(len(ptext)%48)
        add = ('0'*bitsToAdd)
        ptext+=add    
    elif len(ptext)==0:
        ptext=('0'*48)    
    return ptext

def unscramble(scrambled_text): ##DONE
    revPattern=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Redacted
    unscrambled_text=''
    for i in revPattern:
        unscrambled_text+=str(scrambled_text[i])
    return unscrambled_text

def xor(ptext,key): ##DONE 
    text=''
    for i in range(0,48):
        text+=str(int(ptext[i])^int(key[i]))
    return text
    
main()
