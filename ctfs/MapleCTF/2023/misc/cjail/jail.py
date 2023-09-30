import os, re

lines = input("input c: ")
while True:
    line = input()
    lines += "\n"
    lines += line
    if line == "": break

if re.search(r'[{][^}]', lines) or re.search(r'[^{][}]', lines):
    quit() # disallow function declarations
elif re.search(r';', lines):
    quit() # disallow function calls
elif re.search(r'#', lines):
    quit() # disallow includes
elif re.search(r'%', lines) or re.search(r'\?', lines) or re.search(r'<', lines):
    quit() # disallow digraphs and trigraphs
elif re.search(r'_', lines):
    quit()
elif re.search(r'system', lines):
    quit() # a little more pain
else:
    with open("safe.c", "w") as file:
        file.write(lines)
    os.system("cc safe.c")
    os.system("./a.out")
