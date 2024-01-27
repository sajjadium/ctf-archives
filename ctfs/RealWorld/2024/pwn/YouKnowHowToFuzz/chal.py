#!/usr/local/bin/python3
from grammar import Grammar

print("define your own rule >> ")
your_rule = ""
while True:
    line = input()
    if line == "<EOF>":
        break
    your_rule += line + "\n"

rwctf_grammar = Grammar()
err = rwctf_grammar.parse_from_string(your_rule)

if err > 0:
    print("Grammer Parse Error")
    exit(-1)

rwctf_result = rwctf_grammar._generate_code(10)
with open("/domato/rwctf/template.html", "r") as f:
    template = f.read()

rwctf_result = template.replace("<rwctf>", rwctf_result)

print("your result >> ")
print(rwctf_result)

