import sys

prog = input("enter your program: ").encode("latin-1")
open(f"{sys.argv[1]}", "wb").write(prog[:4000])
