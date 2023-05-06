import json
import subprocess

print('I know the flag:')
pub = json.load(open('parts/public.json', 'r'))
print('Public: ', pub)
if pub == ["1"]:
    print('good :)')
else:
    print('bad :(')
subprocess.run('snarkjs plonk verify parts/verification_key.json parts/public.json parts/proof.json', shell=True)
