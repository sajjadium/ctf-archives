tr = eval(open('tr').read())
flagtxt = open('flagtxt.py').read()
exec(flagtxt)
with open('flagtxt', 'w') as f:
    f.write(flagtxt.translate(tr))