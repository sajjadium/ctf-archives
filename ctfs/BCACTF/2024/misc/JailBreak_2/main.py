def sanitize(letter):
    print("Checking for contraband...")
    return any([i in letter.lower() for i in BANNED_CHARS])

def end():
    print("Contraband letters found!\nMessages Deleted!")
    exit()

BANNED_CHARS = "gdvxfiyundmnet/\\'~`@#$%^&.{}0123456789"
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
        print(f'Error occured: {str(e)}; Message could not be sent.')

    msg = input("\nPlease enter your message: ")