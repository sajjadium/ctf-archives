def sanitize(letter):
    print("Checking for contraband...")
    return any([(i in letter.lower()) for i in BANNED_CHARS]) or any([ord(l)>120 for l in letter])

def end():
    print("Contraband letters found!\nMessages Deleted!")
    exit()

BANNED_CHARS = "gdvxfiyundmpnetkb/\\'\"~`!@#$%^&*.{},:;=0123456789#-_|? \t\n\r\x0b\x0c"
flag = open('flag.txt').read().strip()

print("Welcome to the prison's mail center")

msg = input("\nPlease enter your message: ")

while msg != "":
    if sanitize(msg): 
        end()

    try:
        x = eval(msg)
        if len(x) != len(flag): end()
        print(x)
    except Exception as e:
        print(f'Error.')

    msg = input("\nPlease enter your message: ")