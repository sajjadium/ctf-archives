#!/usr/bin/python3 -u

import os
import sys
import subprocess
import uuid
import random

def main():
  number = random.randint(10,100)
  dir = '/tmp/' + str(uuid.uuid4())
  os.mkdir(dir)
  with open('./auto-pwn.c', 'r') as auto_pwn_tmpl_file:
    auto_pwn_c_code = auto_pwn_tmpl_file.read()
    auto_pwn_c_code = auto_pwn_c_code.replace('$1', str(number))
    auto_pwn_tmpl_file.close()
  os.chdir(dir)
  with open('./auto-pwn.c', 'w') as auto_pwn_file:
    auto_pwn_file.write(auto_pwn_c_code)
    auto_pwn_file.close()
  subprocess.run(['/usr/bin/gcc', '-O0', '-fno-stack-protector', '-no-pie', './auto-pwn.c', '-o', 'auto-pwn'], env={'PATH': '/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin'})
  os.remove('./auto-pwn.c')
  print('-' * 27 + ' START BINARY ' + '-' * 27 + '\n')
  print(os.popen('cat ./auto-pwn | xxd').read())
  print('-' * 28 + ' END BINARY ' + '-' * 28)
  subprocess.run(['./auto-pwn'], stdin=sys.stdin, timeout=10)
  os.remove('./auto-pwn')

if __name__ == '__main__':
  print('We give you a few binary with a arbitrary offset. Your task is to use your automated\n pwning setup (that you obviously already have) to get the flag.')
  print('Are you ready ? [y/n] ', end='')
  choice = input()
  if ( choice == 'y' or choice == 'Y' ):
    main()