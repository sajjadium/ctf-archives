#!/usr/local/bin/python

from random import SystemRandom
rand = SystemRandom()


def test_substitution(substitutions, string):
    def substitute(s, a, b):
        initial = s
        s = s.replace(a, b)
        return (s, not s == initial)

    # s ^ 2 rounds for string of length s
    for _ in range(len(string) ** 2):
        performed_substitute = False
        for find, replace in substitutions:
            string, performed_substitute = substitute(string, find, replace)
            # once a substitute is performed, go to next round
            if performed_substitute:
                break
        # if no substitute was performed this round, we are done
        if not performed_substitute:
            break
    return string


def read_substitution(string):
    substitution = tuple(s.strip() for s in string.split('=>'))
    return substitution if len(substitution) == 2 else ('', '')


def run_level(case_generator, max_subs, test_cases=32):
    if input('See next level? (y/n) ') == 'n':
        exit()

    print('-' * 80)
    print('Here is this level\'s intended behavior:')
    for _ in range(10):
        initial, target = case_generator()
        print(f'\nInitial string: {initial}')
        print(f'Target string: {target}')

    print('-' * 80)
    substitutions = []
    current = input(
        f'Enter substitution of form "find => replace", {max_subs} max: '
    )
    substitutions.append(read_substitution(current))
    for _ in range(max_subs - 1):
        if input('Add another? (y/n) ') == 'n':
            break
        current = input('Enter substitution of form "find => replace": ')
        substitutions.append(read_substitution(current))

    print('-' * 80)
    print('Testing substitutions...', flush=True)
    for _ in range(test_cases):
        initial, target = case_generator()
        output = test_substitution(substitutions, initial)
        if not output == target:
            print(f'Failed on string: {initial}.')
            print(f'Expected: {target}.')
            print(f'Computed: {output}.')
            exit()
    print('Level passed!')


print('''
Welcome to The Substitution Game!

In each level, you will enter a list of string substitutions.
For example, you may want to change every instance of 'abcd' to 'def'.

The game will provide a series of test cases.
For each case, substitutions will be applied repeatedly in a series of rounds.
In each round, the first possible substitution will be performed.
For test case of length s, there will be s ^ 2 substitution rounds.

In each round, we will show examples of intended substitution behavior.
It is your goal to match our behavior.
''')


randint = rand.randint


def level_1():
    initial = f'{"0" * randint(0, 20)}initial{"0" * randint(0, 20)}'
    target = initial.replace('initial', 'target')
    return (initial, target)


def level_2():
    initial = ''.join(
        rand.choice(['hello', 'ginkoid']) for _ in range(randint(10, 20))
    )
    target = initial.replace('hello', 'goodbye').replace('ginkoid', 'ginky')
    return (initial, target)


def level_3():
    return ('a' * randint(10, 100), 'a')


def level_4():
    return ('g' * randint(10, 100), 'ginkoid')


def level_5():
    random_string = ''.join(
        str(randint(0, 1)) for _ in range(randint(25, 50))
    )
    initial = random_string
    initial += rand.choice(['', '0', '1'])
    initial += random_string[::-1]

    if rand.randint(0, 1):
        return (f'^{initial}$', 'palindrome')
    else:
        shuffled = list(initial)
        rand.shuffle(shuffled)
        return (
            f'^{"".join(shuffled)}$',
            'not_palindrome'
        )


def level_6():
    first_number = randint(0, 255)
    second_number = randint(0, 255)
    answer = first_number + second_number
    result = 'correct'
    # random chance that answer is wrong
    if rand.randint(0, 1):
        answer = randint(0, 511)
        if not answer == first_number + second_number:
            result = 'incorrect'

    # convert all to string representations
    numbers = [
        bin(first_number)[2:], bin(second_number)[2:], bin(answer)[2:]
    ]

    # chance to pad a number or answer
    if randint(0, 1):
        index = randint(0, 2)
        numbers[index] = '0' * randint(1, 3) + numbers[index]
        # chance to make padded number additionally wrong
        if randint(0, 1):
            result = 'incorrect'
            numbers[index] = '1' + numbers[index]

    return (f'^{numbers[0]}+{numbers[1]}={numbers[2]}$', result)


run_level(level_1, 5)
run_level(level_2, 10)
run_level(level_3, 10)
run_level(level_4, 10)
run_level(level_5, 100, test_cases=128)
run_level(level_6, 300, test_cases=128)

print('-' * 80)
print('You win! Here\'s your flag: [REDACTED]')
