
import json
import subprocess

flag = input('Flag: ').encode('ascii')
assert len(flag) == 32

inp = {
    "flag": list(bytes(flag))
}

open('tmp_input.json', 'w').write(json.dumps(inp))

rcode = subprocess.run('snarkjs wc ./parts/main.wasm tmp_input.json tmp_witness.wtns', shell=True)
if rcode.returncode == 1:
    print('Failed!')
    exit(-1)

print('Generating proof...')
subprocess.run('snarkjs plonk prove parts/circuit_final.zkey tmp_witness.wtns tmp_proof.json tmp_public.json', shell=True)

print('Do you know the flag?')
pub = json.load(open('tmp_public.json', 'r'))
print('Public: ', pub)
if pub == ["1"]:
    print('good :)')
else:
    print('bad :(')
subprocess.run('snarkjs plonk verify parts/verification_key.json tmp_public.json tmp_proof.json', shell=True)
