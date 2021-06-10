import random, string, subprocess, os, sys
from hashlib import sha256

random_str=''
for i in xrange (0,1000000000):
	if (sha256(random_stra + str(i)).digest().startswith('\0\0\0')):
		print "Index is = ",i,"Result is =", sha256(random_str + str(i)).hexdigest()