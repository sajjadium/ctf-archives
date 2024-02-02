
import json

def link(brain, a, b):
    if a[0] in brain:
        brain[a[0]][a[1]] = b
    if b[0] in brain:
        brain[b[0]][b[1]] = a

def unlink(brain, ptr):
    other = brain[ptr[0]][ptr[1]]
    if ptr == brain[other[0]][other[1]]:
        brain[ptr[0]][ptr[1]] = ptr
        brain[other[0]][other[1]] = other
        
def enter(brain, a):
    return brain[a[0]][a[1]]
        
def neuron(brain, t):
    c = brain['_n']
    brain['_n'] += 1
    brain[c] = [(c,0),(c,1),(c,2),t]
    return c
    
def happy(brain, i, i2):
    link(brain, enter(brain, (i,1)), enter(brain, (i2,1)))
    link(brain, enter(brain, (i,2)), enter(brain, (i2,2)))
    
def sad(brain, i, i2):
    p = neuron(brain, brain[i2][3])
    q = neuron(brain, brain[i2][3])
    r = neuron(brain, brain[i][3])
    s = neuron(brain, brain[i][3])
    link(brain, (r,1), (p,1))
    link(brain, (s,1), (p,2))
    link(brain, (r,2), (q,1))
    link(brain, (s,2), (q,2))
    link(brain, (p,0), enter(brain, (i,1)))
    link(brain, (q,0), enter(brain, (i,2)))
    link(brain, (r,0), enter(brain, (i2,1)))
    link(brain, (s,0), enter(brain, (i2,2)))

def process_emotion(brain, i, i2) -> bool:
    if brain[i][3] == brain[i2][3]:
        happy(brain, i, i2)
    else:
        sad(brain, i, i2)

    for s in range(3):
        unlink(brain, (i, s))
        unlink(brain, (i2, s))

    del brain[i]
    if i2 in brain:
        del brain[i2]

    return True

def experience_life(brain):
    brain['_n'] = max([k for k in brain if type(k) is int]) + 1

    z1 = []
    z2 = []
    curr = enter(brain, (0,1))
    prev = None
    back = None
    
    while curr[0] != 0 or len(z1) > 0:
        if curr[0] == 0:
            curr = enter(brain, z1.pop(-1))
        prev = enter(brain, curr)
        if curr[1] == 0 and prev[1] == 0:
            back = enter(brain, (prev[0], z2.pop(-1)))
            process_emotion(brain, prev[0], curr[0])
            curr = enter(brain, back)
        elif curr[1] == 0:
            z1.append((curr[0], 2))
            curr = enter(brain, (curr[0], 1))
        else:
            z2.append(curr[1])
            curr = enter(brain, (curr[0], 0))

def write_val(brain, val, prev):
    a = neuron(brain, 0)
    b = neuron(brain, 0)
    c = neuron(brain, 0)
    d = neuron(brain, 0)
    e = neuron(brain, 0)
    f = neuron(brain, 0)
    g = neuron(brain, 0)
    h = neuron(brain, 0)
    i = neuron(brain, 0)
    link(brain,(a,2),(i,0))
    link(brain,(a,0),(b,0))
    link(brain,(b,2),(c,0))
    link(brain,(b,1),(e,1))
    link(brain,(c,2),(d,0))
    link(brain,(c,1),(f,1))
    link(brain,(d,1),(e,0))
    link(brain,(d,2),(f,2))
    link(brain,(e,2),(f,0))
    link(brain,(a,1),(g,0))
    link(brain,(g,2),(h,0))
    link(brain,(i,2),prev)
    
    p = (g,1)
    q = (h,2)
    
    t = max([brain[x][3] for x in brain if type(x) is int]) + 1
    
    for _ in range(val-1):
        m = neuron(brain, t)
        n = neuron(brain, 0)
        t += 1
        
        link(brain,(m,0),p)
        p = (m,2)
        link(brain,(n,0),(m,1))
        link(brain,(n,2),q)
        q = (n,1)
        
    z = neuron(brain,0)
    link(brain,(z,0),p)
    link(brain,(z,2),q)
    link(brain,(z,1),(h,1))
    
    return (i,1)

def term(brain, prev):
    a = neuron(brain, 0)
    b = neuron(brain, 0)
    c = neuron(brain, 0)
    link(brain,(a,0),prev)
    link(brain,(a,2),(b,0))
    link(brain,(b,2),(c,0))
    link(brain,(c,2),(b,1))

def inject(brain, flag):
    prev = (1,1)
    for i in range(len(flag)):
        prev = write_val(brain, ord(flag[i]), prev)
    term(brain, prev)

def is_satisfied(brain):
    a = brain[0][1]
    b = brain[a[0]][2]
    c = brain[b[0]][2]
    return b[0] != c[0]

# -------------------------------

raw = json.load(open('brain.json'))
brain = {int(k): [tuple(raw[k][0]), tuple(raw[k][1]), tuple(raw[k][2]), raw[k][3]] for k in raw}
brain['_n'] = max([k for k in brain if type(k) is int]) + 1

flag = input('Flag > ')

if len(flag) != 32 or flag[:5] != 'dice{' or flag[-1] != '}':
    print('Invalid format')
    exit()

inject(brain, flag)
experience_life(brain)

if is_satisfied(brain):
    print('Flag accepted')
else:
    print('Flag rejected')

# -------------------------------
