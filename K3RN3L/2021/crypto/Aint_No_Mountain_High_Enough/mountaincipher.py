#!/usr/bin/env python3
#
# Polymero
#

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import os
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse

#-------------------------------------------------------------------------------
# LINEAR ALGEBRA FUNCTIONS (no numpy.linalg, no sage :3)
#-------------------------------------------------------------------------------
# Matrix determinant
def det(m):
    if len(m) == 2:
        return m[0][0]*m[1][1] - m[0][1]*m[1][0]
    else:
        return sum( (-1)**(i) * m[0][i] * det( [list(mi[:i]) + list(mi[i+1:]) for mi in m[1:]] ) for i in range(len(m)) )

# Matrix transpose
def trans(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m))]

# Matrix adjoint (to calculate the inverse)
def adjoint(m):
    adj = [[0 for _ in range(len(m))] for _ in range(len(m))]
    for i in range(len(m)):
        for j in range(len(m)): 
            adj[i][j] = (-1)**(i+j) * det( [ list(mi[:j])+list(mi[j+1:]) for mi in list(m[:i])+list(m[i+1:]) ] )
    return trans(adj)

# Simple matrix multiplication (mod p)
def matmult(A, B, p):
    assert len(A) == len(B)
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for ri in range(n):
        for ci in range(n):
            C[ri][ci] = sum( [A[ri][i]*B[i][ci] for i in range(n)] ) % p
    # Return
    return C

#-------------------------------------------------------------------------------
# CIPHER HELPER FUNCTIONS
#-------------------------------------------------------------------------------
# (u)Random key gen
def keygen(n, p):
    i = 0
    while i < 1000:
        try:
            keycube = [[[int(bytes_to_long(os.urandom(p//256 + 1))/256*p) % p for _ in range(n)] for _ in range(n)] for _ in range(n)]
            keyDINV = [int(inverse(det(k),p)) for k in keycube]
            keyCINV = [[[c*keyDINV[i] % p for c in r] for r in adjoint(k)] for i,k in enumerate(keycube)]
            return keycube, keyCINV[::-1]
        except:
            i += 1
            continue    
    raise ValueError('Key generation failed, try again or try with a different p...')

# Padding and msg matrixfier
def pad(msg, n):
    # Bytestrings only pls
    if type(msg) == str:
        msg = msg.encode()
    # Apply random padding
    while (len(msg) % (n*n) != 0):
        msg += os.urandom(1)
    # Matrixfy and return
    return [[list(i[j:j+n]) for j in range(0,n*n,n)] for i in [msg[k:k+n*n] for k in range(0,len(msg),n*n)]]

#-------------------------------------------------------------------------------
# MOUNTAIN CIPHER
#-------------------------------------------------------------------------------
# Mountain Cipher Encryption Function
def encMC(msg, n, p, key=None, verbose=False):
    # Create key if none given
    if key is None:
        key, _ = keygen(n, p)   
    # Convert msg to matrix
    if type(msg) != list:
        msg = pad(msg, n)
    # For all nxn msg matrices
    ct = []
    for mi in msg:
        # Hill-cipher encrypt with every key matrix
        for i in range(n):
            mi = matmult(key[i], mi, p)
        # Add result to ciphertext
        ct += [mi]
    # Debug
    if verbose:
        print('Key Cube\n',key, '\n')
        print('Message Cube\n',msg, '\n')
        print('Cipher Cube\n',ct, '\n')
        if p < 256:
            print('Msg\n',bytes([i for j in [i for j in msg for i in j] for i in j]), '\n')
            print('Cip\n',bytes([i for j in [i for j in ct for i in j] for i in j]), '\n')
    # Return ciphertext in hex
    if False and all(i < 256 for i in [i for j in [i for j in ct for i in j] for i in j]):
        return bytes([i for j in [i for j in ct for i in j] for i in j]).hex()
    else:
        return ct

# Mountain Cipher Decryption Function
def decMC(cip, n, p, key):
    # Transform cipher text
    if type(cip) == str:
        cip = bytes.fromhex(cip)
    if type(cip) != list:
        cip = pad(cip, n)
    # Decryption key from key
    detinvs = [int(inverse(det(k),p)) for k in key[::-1]]
    deckey = [[[c*detinvs[i] % p for c in r] for r in adjoint(k)] for i,k in enumerate(key[::-1])]
    # Get decryption through encryption with decryption key
    return encMC(cip, n, p, key=deckey, verbose=False)

#-------------------------------------------------------------------------------
# PROOF OF CONCEPT
#-------------------------------------------------------------------------------
def __main__():

	# (key) Cube length
	n = 8
	# Prime modulo
	p = 10001
	# Generate random key set
	kpub, kpriv = keygen(n, p)
	# Encrypt :)
	print(encMC('Hello there! Can I find a flag somewhere around here?', n, p, key=kpub, verbose=True))

#__main__()