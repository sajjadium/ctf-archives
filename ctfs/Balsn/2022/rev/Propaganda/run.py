import subprocess

flag = b'BALSN{____this__is______not_a_flag_______}'

answer = [9128846476475241493, 7901709191400900973, 9127969212443560833, 8731519357089725617, 4447363623394058601, 616855300804233277]

output = []
for i in range(0, len(flag), 8):
    number = int.from_bytes(flag[i:i+8], 'little')
    output.append(int((subprocess.check_output(['node', 'launcher.js', str(number)]))[:-2]))

print(output == answer)
