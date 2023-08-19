# Functions copied from "That-crete log" from UIUCTF 2022. Thanks!

def miller_rabin(bases, n):
    # I don't know how to annotate this because it involves of a bunch of
    # mathematics that I could not understand, but I still want to be verbose.
    # Maybe I should link you the wiki page so you could read that...
    # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    if n == 2 or n == 3:
        return True

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for b in bases:
        x = pow(b, s, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n-1:
                break
        else:
            return False
    return True

def is_prime(n):
    # bases = [2, 3, 5, 7, 11, 13, 17, 19, 31337] are used by the challenge from
    # UIUCTF. That isn't good enough...
    # I learned from ICPC that those seven bases blocks every number below 2^64.
    bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    # I will also add a bunch of random bases. Well, I really meant it. This is
    # how I generate those bases:
    #       sorted([random.randint(2, 1000000)*2+1 for _ in range(200)])
    bases += [
          20669,   48929,   57021,   63569,   73307,   86815,   93495,  101303,
         124851,  126617,  164415,  171811,  184653,  219385,  221067,  223499,
         229897,  234477,  251893,  264151,  295599,  299453,  308525,  316135,
         318467,  319081,  326169,  341721,  343699,  351743,  374223,  378375,
         387703,  387807,  390443,  417763,  430031,  438233,  440079,  441259,
         444591,  465613,  475205,  485841,  501341,  509761,  515577,  528775,
         533381,  536401,  558123,  562419,  583397,  606965,  617121,  619821,
         625787,  632805,  650751,  689307,  695181,  695725,  704809,  706557,
         720371,  729335,  737269,  741827,  743969,  745609,  750425,  764843,
         768725,  782945,  789713,  794851,  832829,  849477,  849917,  872481,
         880381,  880601,  882991,  891339,  892581,  897917,  900497,  902791,
         907839,  908069,  910733,  936747,  945849,  952533,  965837,  967739,
        1007573, 1018197, 1022845, 1027277, 1027963, 1044711, 1050091, 1050839,
        1053395, 1060643, 1070551, 1080385, 1087593, 1095565, 1111439, 1141847,
        1146745, 1168487, 1176229, 1180219, 1187279, 1203567, 1204739, 1207205,
        1212905, 1233043, 1252625, 1256889, 1272399, 1298475, 1302085, 1305033,
        1309991, 1325833, 1334399, 1340793, 1355737, 1365593, 1376389, 1381963,
        1390677, 1405539, 1421269, 1426487, 1433469, 1448275, 1458545, 1462879,
        1464553, 1482773, 1486655, 1504839, 1512277, 1517895, 1526807, 1532327,
        1543995, 1545351, 1553127, 1563397, 1572205, 1573891, 1583443, 1595567,
        1603263, 1609551, 1631223, 1633943, 1650589, 1677741, 1681935, 1696649,
        1713355, 1715365, 1730819, 1741045, 1745279, 1751007, 1758715, 1778157,
        1779521, 1785051, 1789451, 1789671, 1790781, 1791763, 1812959, 1823427,
        1824907, 1842549, 1846559, 1847019, 1865431, 1879215, 1895455, 1930981,
        1932295, 1940509, 1957911, 1976957, 1986973, 1992813, 1993333, 1994939
    ]
    # We should be able to find all composite numbers smaller than 65536 with
    # this sieve. Well, we don't do Miller-Rabin for every numbers; or it will
    # be too time-consuming.
    for i in range(2, min(256, n)):
        if n % i == 0:
            return False
    # Although I don't know why they used 256 (instead of 65536) here, I will
    # just stick to that.
    if n < 256:
        return True
    # Now we use Miller-Rabin for the large numbers.
    return miller_rabin(bases, n)
