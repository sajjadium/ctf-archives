from random import sample, randint 
 
p = random_prime(2^1024) 
R = Zmod(p) 
 
groups = list(randint(2, 6) for i in range(40)) 
thresh = list(randint(i//2, i//2 + 1) for i in groups) 
 
G = list( 
    list(R.random_element() for i in range(c))  
    for c in groups 
) 
 
message = list( 
    sorted(sample(range(g), i))[::-1] 
    for g, i in zip(groups, thresh) 
) 
 
P = sum( 
    sum(g[i] for i in m) 
    for m, g in zip(message, G) 
) 
 
print(f"p = {p}") 
print(f"groups = {groups}") 
print(f"thresh = {thresh}") 
print(f"G = {G}") 
print(f"P = {P}") 
 
def lexorder(x, m): 
    if len(x) == 0: return 1 
    return binomial(x[0], len(x)) + lexorder(x[1:], x[0]) 
 
flag, b = 0, 1 
for m, g in zip(message, groups): 
    flag += lexorder(m, g) * b 
    b *= binomial(g, len(m)) 
 
print(f"flag = {flag}") 
