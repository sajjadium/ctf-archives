from parser import Parser
from interpreter import Interpreter

import sys
import os
import secrets
import xxhash

FLAG = os.getenv('FLAG', 'VuwCTF{ntc_test_flag}')

BANNER = """
 .-----------------. .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. |
| | ____  _____  | || |  _________   | || |     ______   | |
| ||_   \\|_   _| | || | |  _   _  |  | || |   .' ___  |  | |
| |  |   \\ | |   | || | |_/ | | \\_|  | || |  / .'   \\_|  | |
| |  | |\\ \\| |   | || |     | |      | || |  | |         | |
| | _| |_\\   |_  | || |    _| |_     | || |  \\ `.___.'\\  | |
| ||_____|\\____| | || |   |_____|    | || |   `._____.'  | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------' 
"""
print(BANNER)
print("Welcome to the Not Turing-Complete Interpreter!")
print("Here at VuW, we're proud to offer state-of-the-art")
print("virtual machine capabilities for your code.")
print()
print("To celebrate the launch of our new product, we're offering")
print("a flag to anyone who can solve this programming challenge")
print("using our programming language.")
print()
print("In order to streamline the programming experience,")
print("we've simplified our language to include only the following features:")
print("- Three integer variables: a, b, c")
print("- Advanced integer arithmetic operations: +, -, *, /, ^, &, |")
print("- No control flow (if, loops, etc.)")
print("- No function calls or recursion")
print("- No additional memory or I/O")
print("VuW is proud to be pushing the bounds of computer science")
print("by offering Deterministic Finite Automaton-based computation.")
print()


print("Enter your lines of code, ending with an 'EOF' line:")

parser = Parser()
while True:
    try:
        line = input()
        if line.strip() == "EOF":
            break
        parser.parse_line(line)
    except Exception as e:
        print("Error accepting code")
        sys.exit(1)

NUM_TRIALS = 10

print(f"Running {NUM_TRIALS} trials to validate your code...")

interpreter = Interpreter(parser.code)

def run_trial():
    try:
        scramble = secrets.token_bytes(32)  # 256-bit seed!
        input_a = int.from_bytes(scramble, byteorder='little')
        interpreter.initialize(a_value=input_a)
        interpreter.interpret()
        output_a = interpreter.variables['a']
        expected = int.from_bytes(xxhash.xxh32(scramble).digest(), byteorder='big')
        return output_a == expected
    except Exception as e:
        return False


accepted = False
for trial in range(NUM_TRIALS):
    if not run_trial():
        break
else:
    accepted = True

if accepted:
    print("Code accepted")
    print(f"Flag: {FLAG}")
else:
    print("Code rejected")
