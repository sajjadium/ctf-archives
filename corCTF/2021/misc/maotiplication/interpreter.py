def apply_runs(string, rules, max_operations=500000000, max_len=5000000):
    for operations in range(max_operations):
        orig_string = string # There HAS to be a better way than this...
        for rule in rules:
            if len(rule) != 2 and len(rule) != 3: # Length 2 is a standard rule, length 3 is a terminating rule
                return f"Invalid rule: {rule}"
            if rule[0] == '': # An empty pattern indicates start of string
                if len(rule) == 2:
                    string = rule[1] + string
                    break
                else:
                    return rule[2] + string
            elif rule[0] in string:
                if len(rule) == 2:
                    string = string.replace(rule[0], rule[1], 1)
                    break
                else:
                    return string.replace(rule[0], rule[2], 1)
            if len(string) > max_len: # Prevent mistakes from causing infinite expansion
                return 'Maximum string length reached. Last string was \'' + string + '\''
        if orig_string == string:
            return string
    return 'Maximum operations reached. Last string was \'' + string + '\''

if __name__ == '__main__':
    tests = [
                ('Hello,', 'Hello, world!'),
                ('Oh Hell.', 'Oh Heck.'),
                ('101', 'ooooo'),
                ('No rules match.', 'No rules match.'),
            ]
    print('Running basic unit tests.')
    for test, expected in tests:
        result = apply_runs(test, [['Hello,', '', 'Hello, world!'], ['Hell', 'Heck'], ['o0', '0oo'], ['1', '0o'], ['0', '']]) # Sorry if these unit tests are hard to read, they were originally imported through a file but I had to modify that for this challenge
        print(f"\'{test}\' => \'{result}\' ({'Test Passed' if result == expected else 'Test Failed, expected ' + expected})")
