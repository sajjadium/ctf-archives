from magic import Magic

with open('flag.txt', 'rb') as f:
    flag = f.read()

banner = '''
███╗   ███╗ █████╗  ██████╗ ██╗ ██████╗    ███████╗██╗ ██████╗ ███╗   ██╗
████╗ ████║██╔══██╗██╔════╝ ██║██╔════╝    ██╔════╝██║██╔════╝ ████╗  ██║
██╔████╔██║███████║██║  ███╗██║██║         ███████╗██║██║  ███╗██╔██╗ ██║
██║╚██╔╝██║██╔══██║██║   ██║██║██║         ╚════██║██║██║   ██║██║╚██╗██║
██║ ╚═╝ ██║██║  ██║╚██████╔╝██║╚██████╗    ███████║██║╚██████╔╝██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝    ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝                                                                         
'''
print(banner)
magic = Magic(137)          # most magical number

C, K, Q = magic.random_list(3)
P1, P2 = C*K, K*Q
pk, sk = (C, P1, P2), (C, K, Q)
print('C =',  pk[0])
print('P1 =', pk[1])
print('P2 =', pk[2])

H = magic.shake(b'Gotta make you understand~')
S = H*Q                     # sign
assert P1*S == C*H*P2       # verify
print('S =', S)

H = magic.shake(b'Never gonna give you flag~')
try:
    S_ = magic(input('> ')[:magic.N])
    if P1*S_ == C*H*P2:
        print(flag)
    else:
        print('Ooh~~~give~you~up~')
except:
    print('You know the rules and so~do~I~')
