
WELCOME='''
 ____            _       _ _ 
|  _ \ _   _    | | __ _(_) |
| |_) | | | |_  | |/ _` | | |
|  __/| |_| | |_| | (_| | | |
|_|    \__, |\___/ \__,_|_|_|
       |___/                 
'''

def main():
    try:
        print("-"*30)
        print(WELCOME)
        print("-"*30)
        print("Try to escape!!This is a jail")
        print("I increased security!!!")
        a=input("> ")
        if len(a)<15:
            eval(a)
        else:
            print("Don't escape!!")
    except:
        print("error")
        exit()

if __name__ == '__main__':
    main()
