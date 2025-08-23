import builtins

alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet += alphabet.upper()
digits = "0123456789"
def trade(x,y):
    if x in ['a','e','i','o','u']:
        return "abcdefghijklmnopqrstuvwxyz"[y]
builtins.chr = trade


cod = input(">>> ")
for i in alphabet:
    if cod.count(i) > 1:
        print(">:(")
        exit(0)
for i in digits:
    if cod.count("\\" + i):
        print(">:(")
        exit(0)

del alphabet
del digits
exec(cod.encode().decode("unicode_escape"))
