import subprocess

print('''\
################################
## DICE TAXATION SYSTEMS 4000 ##
################################''')
flag = input('Enter flag > ')

addendum = '''
### [Flag Addendum]

```catala
declaration flag content list of C equals [{}]
```
'''.format(';'.join(['C{{--index:{} --val:{}}}'.format(i, ord(flag[i])) for i in range(len(flag))]))

prog = open('./DiceTax.catala_en', 'r').read()
open('./DiceTaxInstance.catala_en', 'w').write(prog + addendum)

try:
    p = subprocess.run([
        '/usr/local/bin/catala', 'interpret', 
        '-s', 'Main',
        'DiceTaxInstance.catala_en'
    ], check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    print('You broke the tax machine :(')
    exit(0)

out = p.stdout.decode('utf-8')
tax = out.split('tax = ')[1].split('\n')[0]

print('Tax:', tax)

if tax == '$0.00':
    print('Nice flag!')
