#!/usr/local/bin/python
import subprocess

code = """
def isPalindrome(s):
    result = True
    for i in range(len(s) // 2):
        characterOne = s[i]
        characterTwo = s[len(s) - 1 - i]
        if characterOne != characterTwo:
            result = False
    return result
wordToCheck = input("Enter a word to check if it's a palindrome: ")
if isPalindrome(wordToCheck):
    print("Yes, it's a palindrome!")
else:
    print("No, it's not a palindrome.")
""".strip().split('\n')

print('-' * 10)
print('\n'.join(code))
print('-' * 10)
while True:
    lno = int(input('line number: '))
    comment = input('comment: ')
    code.insert(lno, f'# {comment}')
    print('-' * 10)
    print('\n'.join(code))
    print('-' * 10)
    if input('add more? [y/N]: ') not in ['y', 'Y']:
        break

name = '/tmp/my_awesome_assignment1.py'
with open(name, 'w') as f:
    f.write('\n'.join(code))
subprocess.run(['python', name])
