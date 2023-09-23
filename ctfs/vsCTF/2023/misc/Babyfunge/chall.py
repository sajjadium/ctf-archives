from interpreter import befunge


""" Befunge grid:
[Line 1 input here]
[Line 2 input here]
[Line 3 input here]
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
vsctf{??????????????????????????????}
"""

unneeded_commands = "pg&~"  # idk why anyone would need these
FLAG = "vsctf{??????????????????????????????}"  # real flag will be the same length
line_size = len(FLAG)

# get the input code
payload = ""
for i in range(3):
    this_line = input(f"Line {i+1}: ")
    if len(this_line) > line_size:
        print("Jeez, you don't need all that space!")
        quit()
    payload += f'{this_line:<{line_size}}\n'  # fill the line

# make sure your code is optimal!
num_of_commands = len(payload.replace(" ", "").replace("\n", ""))
any_unneeded_commands = any(command in unneeded_commands for command in payload)
if any_unneeded_commands or num_of_commands > 7:
    print("You don't need all that overhead!")
    quit()

try:
    befunge(f'{payload}{"@"*line_size}\n{FLAG}')
except Exception:
    pass
