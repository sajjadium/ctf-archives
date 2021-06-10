import os
import sys
import subprocess


def main(argv):
    print("Welcome To JavaScript Cleaner")
    js_name = input("Enter Js File Name To Clean: ")
    code = input("Submit valid JavaScript Code: ")

    js_name = os.path.basename(js_name) # No Directory Traversal for you

    if not ".js" in js_name:
        print("No a Js File")
        return

    with open(js_name,'w') as fin:
        fin.write(code)

    p = subprocess.run(['/usr/local/bin/node','index.js','-f',js_name],stdout=subprocess.PIPE);
    print(p.stdout.decode('utf-8'))

main(sys.argv)
