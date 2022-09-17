#! /usr/bin/python2

import subprocess
import tempfile
import sys,os
import random,string
from hashlib import sha256

def proof_of_work():
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
    digest = sha256(proof).hexdigest()
    sys.stdout.write("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
    sys.stdout.write('Give me XXXX:')
    sys.stdout.flush()
    x = sys.stdin.readline()
    x = x.strip()
    if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest:
        return False
    sys.stdout.write('OK\n')
    sys.stdout.flush()
    return True

def main():
    try:
        size = int(sys.stdin.readline())
    except:
        return
    if size > 1000000:
        return
    exp = sys.stdin.read(size)
    f = tempfile.NamedTemporaryFile(prefix='',delete=False)
    f.write(exp)
    f.close()

    # hopefully they will not collide
    cname = "a"+str(random.randint(0,0x100000))
    subprocess.check_output(["docker", "run", "--cap-add=NET_ADMIN", "--rm", "--name", cname,  "-itd", "chal", "sleep", "20"])
    subprocess.check_output(["docker", "cp", f.name, cname+":/home/test/test"])
    subprocess.check_output(["timeout", "10", "docker", "exec", cname, "/run.sh"])

    os.unlink(f.name)


if __name__ == '__main__':
    if proof_of_work():
        main()

