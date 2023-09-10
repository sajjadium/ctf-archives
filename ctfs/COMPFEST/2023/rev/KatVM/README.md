I made my own language! It's very simple, yet effective in comparing things. It has turing machine like properties as well.

Here are the instructions available, write in just like how you write assembly or script, its top to down:

    left <N>, right <N>: Move the tape head to left or right by N
    store <STRING>: Store string to from current head, the head will move right after the string
    print: Print from head to next empty
    input: Input from stdin and store it in current head, the head will move right after the string
    push: Push current head to stack
    popeq <CHAR>: Pop current stack, and compare the character with given char. If true, it will skip next instruction
    quit: Exit

Example for Hello World:

store Hello World!
left 12
print

You may write it the code in a .kat file, and you can compile it with the website. Then execute it with python run_katvm.py output.kb.

NOTE: You need to run it on Python 3.10
