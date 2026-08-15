#!/usr/bin/env python3
import unicodedata
banned = {"print": print, "open": open, "chr": chr}

s = input(">> ")

if len(s) != 6767:
    exit("wrong length :(")
    
if any(c in s for c in "'\"_`\\#"):
    exit("that's not good :(")
    
if any(c.isascii() and c.isalnum() for c in s):
    exit("no no no!!!")
    
if s.count(";") > 1:
    exit("too many semicolons!")

for c in s:
    if c.isidentifier() and unicodedata.normalize("NFKC", c) == c:
        exit("bad:(((")

exec(s, {"__builtins__": banned}, {})
