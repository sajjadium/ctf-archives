import random
import shutil
import os.path
import tempfile
from consts import *

def read_code():
    print('#############################')
    print('Give me coq proof, ending with `EOF`.')
    inp = ''
    while True:
        line = input('')
        if line == 'EOF': break
        inp += line + '\n'
    for word in disallowed:
        if word in inp.lower():
            raise ValueError('Disallowed command in coq proof: ' + word)
    return inp

def read_proof(theorem_header):
    print(theorem_header)
    inp = ''
    while True:
        line = input('Coq < ')
        if line == 'Qed.': break
        inp += line + '\n'
    for word in disallowed:
        if word in inp.lower():
            raise ValueError('Disallowed command in coq proof: ' + word)
    return inp

def test_baby_proof(theorem_name, theorem_type):
    print('#############################')
    theorem = f'Theorem {theorem_name}:\n  {theorem_type}.\nProof.\n'
    proof = theorem + read_proof(theorem) + "Qed."
    check = f"{check_header}Check SimplChall.{theorem_name}: {theorem_type}.\n"
    while test_proof(proof, check) != True:
        proof = theorem + read_proof(theorem) + "Qed."

def test_proof(chall_data, check_data=None):
    user = random.randint(10000, 30000)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree('/app', tmpdir, dirs_exist_ok=True)
        os.chown(tmpdir, 0, user)
        os.chmod(tmpdir, 0o1770)
        os.chown(tmpdir + '/proofs', 0, user)
        os.chmod(tmpdir + '/proofs', 0o1770)

        with open(tmpdir + '/proofs/SimplChall.v', 'w') as f:
            f.write(chall_data)

        if check_data != None:
            with open(tmpdir + '/proofs/SimplCheck.v', 'w') as f:
                f.write(check_data)

        if os.fork() == 0:
            os.chdir(tmpdir)
            os.setresgid(user, user, user)
            os.setresuid(user, user, user)
            if os.system('make') == 0:
                os._exit(0)
            else:
                os._exit(1)
        else:
            (_, status) = os.wait()
            if os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0:
                print('Congrats!')
                return True
            else:
                print('You failed! Try harder!')
                print('https://softwarefoundations.cis.upenn.edu/lf-current/')
                return False


def main():
    os.setgroups([])

    print(intro_prompt)


    if input('(y/n) ').lower()[0] != 'y':
        print(tut_intro)

        test_baby_proof('conj1', 'forall P Q: Prop, P /\\ Q -> Q')
        test_baby_proof('transitive',
            'forall P Q R: Prop, (P -> Q) -> (Q -> R) -> P -> R')
        test_baby_proof('or_logic', 'forall A B C D: Prop, ' + \
                '(A -> B) -> (C -> D) -> A \\/ C -> B \\/ D')
        test_baby_proof('not_true_is_false', 'forall b: bool, ' + \
                'b <> true -> b = false')

        print(tut_induct)
        while test_proof(chall_header + read_code(), induct_check) != True:
            pass
        print(tut_ind_prop)
        while test_proof(chall_header + read_code(), ind_prop_checks[0]) != True:
            pass
        print(tut_ind_prop2)
        while test_proof(chall_header + read_code(), ind_prop_checks[1]) != True:
            pass
        print(tut_ind_prop3)
        while test_proof(chall_header + read_code(), ind_prop_checks[2]) != True:
            pass

        print(tut_final)

    if test_proof(chall_header + read_code(), None) == True:
        os.system('cat /app/flag')

if __name__ == '__main__':
    main()
