load("/home/sage/common.sage")

# secret import
from flag import FLAG

import random


def sign(msg, privkey):
    (A, a), centralmap, (B, b) = privkey

    msgK = encodeK(msg, m)
    Binv = B**(-1)
    F_Ax = matmul(Binv, vecadd(msgK, vecneg(b)))

    while True:
        Ax = [K.random_element() for _ in range(v1)] + [K(0) for _ in range(v1, n)]

        # lazy implementation
        skiplayer1 = False
        if all([F_Ax[i] == K(0) for i in range(m)]):
            Ax = [K(0) for _ in range(v2)] + [K.random_element() for _ in range(v2, n)]
            break
        elif all([F_Ax[i] == K(0) for i in range(o1)]):
            Ax = [K(0) for _ in range(v1)] + [K.random_element() for _ in range(v1, v2)] + [K(0) for _ in range(v2, n)]
            skiplayer1 = True

        # layer 1
        if not(skiplayer1):
            o1_mat = [K(0) for _ in range(o1**2)]
            o1_vec = [F_Ax[i] for i in range(o1)]
            for k in range(o1):
                for (i, j), Kele in centralmap[k].items():
                    if j < v1:
                        o1_vec[k] -= Kele * Ax[i] * Ax[j]
                    else:
                        o1_mat[o1*k+(j-v1)] += Kele * Ax[i]
            o1_mat = Matrix(K, o1, o1, o1_mat)
            o1_vec = vector(K, o1, o1_vec)
            try:
                o1_sol = o1_mat.solve_right(o1_vec)
                for i in range(o1):
                    Ax[v1+i] = o1_sol[i]
            except:
                continue

        # layer 2
        o2_mat = [K(0) for _ in range(o2**2)]
        o2_vec = [F_Ax[o1+i] for i in range(o2)]
        for k in range(o2):
            for (i, j), Kele in centralmap[o1+k].items():
                if j < v2:
                    o2_vec[k] -= Kele * Ax[i] * Ax[j]
                else:
                    o2_mat[o2*k+(j-v2)] += Kele * Ax[i]
        o2_mat = Matrix(K, o2, o2, o2_mat)
        o2_vec = vector(K, o2, o2_vec)
        try:
            o2_sol = o2_mat.solve_right(o2_vec)
            for i in range(o2):
                Ax[v2+i] = o2_sol[i]
        except:
            continue
        break

    Ainv = A**(-1)
    x = matmul(Ainv, vecadd(Ax, vecneg(a)))

    return decodeK(x, n)


def verify(msg, sig, pubkey):
    x = encodeK(sig, n)
    t = encodeK(msg, m)
    t_ = [pubkeyele(x) for pubkeyele in pubkey]
    if t == t_:
        return True
    else:
        return False


if __name__ == '__main__':
    idx = random.randint(0, 20-1)
    fpriv = open(f'/home/sage/privkey_{idx}', 'r')
    privkeystr = fpriv.read()
    fpriv.close()
    exec(privkeystr)
    
    fpub = open(f'/home/sage/pubkey_{idx}', 'r')
    pubkeystr = fpub.read()
    fpub.close()
    exec(pubkeystr)

    # offer public key to user
    print(pubkeystr)

    print("Wait loading keys...", flush=True)

    privkey_0_0 = Matrix(K, n, n, [strtoK(Kelestr) for Kelestr in privkey_0[0]])
    privkey_0_1 = vector(K, n, [strtoK(Kelestr) for Kelestr in privkey_0[1]])
    privkey_0 = (privkey_0_0, privkey_0_1)

    privkey_1 = [{(i,j):strtoK(Kelestr) for (i,j),Kelestr in privkey_1_ele.items()} for privkey_1_ele in privkey_1]

    privkey_2_0 = Matrix(K, m, m, [strtoK(Kelestr) for Kelestr in privkey_2[0]])
    privkey_2_1 = vector(K, m, [strtoK(Kelestr) for Kelestr in privkey_2[1]])
    privkey_2 = (privkey_2_0, privkey_2_1)

    privkey = (privkey_0, privkey_1, privkey_2)

    pubkey_ = []
    for pubkeyele in pubkey:
        pubkeyele_ = 0
        for e, Kelestr in pubkeyele.items():
            pubkeyele_ += strtoK(Kelestr) * reduce(lambda a,b:a*b, [yi[i]**e[i] for i in range(len(e))], 1)
        pubkey_.append(pubkeyele_)
    pubkey = pubkey_
    
    cnt = 0
    MENU = '1:sign\n2:verify\n3:getflag'
    while True:
        try:
            print("")
            print(MENU)
            userinput = int(input('>> '))
            if userinput == 1:
                if cnt > 3:
                    print('No more give you a signature')
                    continue
                msghex = input('msg(hex): ')
                sig = sign(bytes.fromhex(msghex), privkey)
                print(f'sig: {sig.hex()}')
                cnt += 1
                continue
            elif userinput == 2:
                msghex = input('msg(hex): ')
                sighex = input('sig(hex): ')
                result = verify(bytes.fromhex(msghex), bytes.fromhex(sighex), pubkey)
                if result:
                    print('Verification success.')
                else:
                    print('Verification failed.')
                continue
            elif userinput == 3:
                msg = bytes([random.randint(0, 255) for _ in range((4*m)//8)])
                print(f'sign for msg: {msg.hex()}')
                sighex = input('sig(hex): ')
                result = verify(msg, bytes.fromhex(sighex), pubkey)
                if result:
                    print('Congratulations. Here is FLAG.')
                    print(FLAG)
                    break
                else:
                    print('NG')
                    break
            else:
                continue
        except:
            print('error occured')
            break
