import os
flag = os.environ.get('FLAG', 'SEE{not_the_real_flag}')

p = 2^8 * 3^15 - 1
F.<i> = GF(p^2, modulus=x^2+1)
j = F(0)

print('''\
 _____                                    __  __      
|_   _|                                  |  \/  |              
  | |  ___  ___   __ _  ___ _ __  _   _  | \  / | __ _ _______ 
  | | / __|/ _ \ / _` |/ _ \ '_ \| | | | | |\/| |/ _` |_  / _ \\
 _| |_\__ \ (_) | (_| |  __/ | | | |_| | | |  | | (_| |/ /  __/
|_____|___/\___/ \__, |\___|_| |_|\__, | |_|  |_|\__,_/___\___|
                  __/ |            __/ |                       
                 |___/            |___/
Welcome to the Isogeny Maze! Substrings of pi contain the flag.''')

for _ in range(100):
    E = EllipticCurve(j = j)
    print('-'*63)
    print(f'You are in Town {j}.')
    if str(j) in '31415926535897932384626433832795':
        print(f'There is a flag in this town: {flag}')
    
    neighbours = [E.isogeny_codomain(m).j_invariant() for m in E(0).division_points(2)]
    neighbours = sorted(set(neighbours) - {j})
    roadmsg = 'is only 1 road' if len(neighbours) == 1 else f'are {len(neighbours)} roads'
    print(f'There {roadmsg} out of here:')
    for i,n in enumerate(neighbours):
        print(f'* Road [{i+1}] leads to Town {n}')
    print('Which road would you like to take?')
    try:
        j = neighbours[int(input())-1]
    except (ValueError, IndexError):
        print('Invalid road.')
        pass
