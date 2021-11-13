print('Find my number N, and I will give you the flag.')
def f(N,k):
    while min(N,k)>0:
        if k>N: N,k = k,N
        N%=k
    return max(N,k)
import random
N = random.getrandbits(512)
for i in range(600):
    print(f"Try #{i+1}: ")
    k = input(f'Enter k: ')
    l = input(f'Enter l: ')
    try:
        k= int(k)
        assert 0<k<pow(10,500)
        l= int(l)
        assert 0<l<pow(10,500)
    except:
        print('Invalid input. Exiting...')
        quit()
    print(f'f(N+l,k) = {f(int(N+l),k)}\n')
guess = input('What is N?')
if str(N)==guess:
    print(open('flag.txt').read().strip())
else:
    print('Wrong answer. The number was '+str(N))