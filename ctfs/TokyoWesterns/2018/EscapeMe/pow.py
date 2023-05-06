#!/usr/bin/env python2.7
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



from hashcash import check
import random
import string
import sys
import os
import resource

SKIP_SECRET = sys.argv[1] if len(sys.argv) > 1 else None

bits = 25
rand_resource = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
print 'hashcash -mb{} {}'.format(bits, rand_resource)
sys.stdout.flush()

stamp = sys.stdin.readline().strip()

if SKIP_SECRET is None or stamp != SKIP_SECRET:
    if not stamp.startswith('1:'):
        print 'only hashcash v1 supported'
        exit(1)

    if not check(stamp, resource=rand_resource, bits=bits):
        print 'invalid'
        exit(1)

print 'Any other modules? (space split) > ',
sys.stdout.flush()

mods = sys.stdin.readline().strip()
if '/' in mods:
    print 'You can load modules only in this directory'
    exit(1)

args  = ['./kvm.elf', 'kernel.bin', 'memo-static.elf']
args += mods.split()
print '\nexecuting : {}\n'.format(' '.join(args))

dirname = os.path.dirname(__file__)
os.chdir(dirname)

os.close(2)
os.open('/dev/null', os.O_WRONLY)

resource.setrlimit(resource.RLIMIT_NOFILE, (9, 9))
os.execv(args[0], args)
