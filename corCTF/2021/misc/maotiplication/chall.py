import random
from interpreter import apply_runs

FLAG = "REDACTED"

def intro():
    rep = random.randint(1, 10)
    test = "strellic"*rep
    expected = "jsgod"
    return (test, expected)

def xor():
    a = random.randint(0, 255)
    b = random.randint(0, 255)
    c = a^b
    test = bin(a)[2:] + '^' + bin(b)[2:]
    expected = bin(c)[2:]
    return (test, expected)

def mult():
    a = random.randint(0, 255)
    b = random.randint(0, 255)
    c = a*b
    test = bin(a)[2:] + 'x' + bin(b)[2:]
    expected = bin(c)[2:]
    return (test, expected)

def run_round(test_case, max_operations, max_rules, trials=256):
    for i in range(5):
        case = test_case()
        print(f"\'{case[0]}\' => \'{case[1]}\'")

    print(f"\nConstraints: {max_rules} rules, {max_operations} substitutions\n\n")

    rules = []
    while True:
        rule = input('Rule: ')
        if ':' in rule:
            rules.append(rule.split(':'))
        elif 'EOF' in rule:
            break
        
    if len(rules) > max_rules:
        print('Maximum rules exceeded!')
        exit()
   
    for i in range(trials):
        case = test_case()
        result = apply_runs(case[0], rules, max_operations=max_operations)
        if result != case[1]:
            print(f"\'{case[0]}\' => \'{result}\' (Test Failed, expected \'{case[1]}\')")
            exit()
    print("All tests passed!\n\n")

print("""
its time to get funky and maotiply

This interpreter takes a series of string substitutions and executes them on input strings sequentially.
Please enter your substitution rules in sequential order, one per line. Terminate your rules sequence with the string \'EOF\'. DO NOT SEND AN ACTUAL EOF.

The rule format is SEARCH:REPLACE. A double colon (SEARCH::REPLACE) can be used to create a terminating rule. If a terminating substitution rule is executed, the interpreter will not process any further substitutions.
If SEARCH is an empty string, then REPLACE will be inserted at the beginning of the input string instead.

For further clarification of interepter behavior, feel free to read the source.

For each round, a short description of the intended behavior will be provided. Additionally, several examples will be supplied. Your task is to devise a series of substitutions to accomplish this behavior.

Good luck!
""")

print('Round 1:')
print('Replace (possibly repeated) instances of \"strellic\" with a single instance of \"jsgod\".')
run_round(intro, 20, 5, trials=10)

print('Round 2:')
print('Perform XOR on the two supplied numbers.')
run_round(xor, 120, 50)

print('Round 3:')
print('Perform multiplication on the two provided numbers.')
run_round(mult, 2500, 100)

print('Congratulations!')
print(FLAG)
