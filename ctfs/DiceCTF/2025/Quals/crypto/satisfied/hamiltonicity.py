# this file is identical to the one found at https://github.com/cryptohack/ctf_archive/blob/main/ch2024-sigma-hamiltonicity/server_files/hamiltonicity.py
# apart from the parameters (P, q, h1, h2) used for the commitment scheme
import random
from hashlib import sha256

P = 0x1a91c7e50ef774ab758fa1a8aebfaa9f5fcc3cf22e3b419e5197c5268b1c883f01fbba85de35f1ae1d2544a977dc858a846e6c86f7ff0653881d1e43dbfc535fa3f606cf8f95fb0a53d75dc96de29af01c6967b947b0bf2c1232257d1d9d066036acf3648a54248904f3fdb360debbedab5e58ba7a19308c2a25ad63376044677
q = 0xd48e3f2877bba55bac7d0d4575fd54fafe61e79171da0cf28cbe293458e441f80fddd42ef1af8d70e92a254bbee42c5423736437bff8329c40e8f21edfe29afd1fb0367c7cafd8529ebaee4b6f14d780e34b3dca3d85f96091912be8ece83301b5679b2452a12448279fed9b06f5df6d5af2c5d3d0c98461512d6b19bb02233b


# Generate `h1,h2` to be a random element Z_P of order q
# Unknown dlog relation is mask for the Pedersen Commitment

# Hardcoded a random `h1,h2` value for ease of use
# h1 = pow(random.randint(2,P-1),2,P)
# h2 = pow(random.randint(2,P-1),2,P)
h1 = 78777458529900494490614837925133899234033382878031882472334088956271190982992006579121996363436837622269937515963969631350196078518833552064350879178135378664181885312653105871452865514975911372301003349338291198633437687325826425425608673730990839066457483305538373645745058807876087476862601690892691176886
h2 = 79543261289463851669680579732622963629972939196770858598613223074429180846489223401875297929962046462819170352455602650818571522306298694684743021001523247847054210636909249854011863258940228182916282685739437065475409404546810221793296109200612655318070086567712704167633234254449463709961905778271868952583
comm_params = P,q,h1,h2



# Information theoretically hiding commitment scheme
def pedersen_commit(message, pedersen_params = comm_params):
    P,q,h1,h2 = pedersen_params
    r = random.randint(0,q)
    commitment = (pow(h1,message,P) * pow(h2,r,P)) % P
    return commitment, r

def pedersen_open(commitment,message,r, pedersen_params = comm_params):
    P,q,h1,h2 = pedersen_params
    if (commitment * pow(h1,-message,P) * pow(h2,-r,P) ) % P == 1:
        return True
    else:
        return False

# Given a graph, return an element-wise commitment to the graph
def commit_to_graph(G,N):
    G2 = [[0 for _ in range(N)] for _ in range(N)]
    openings = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            v = G[i][j]
            comm, r = pedersen_commit(v)
            assert pedersen_open(comm,v,r)
            G2[i][j] = comm
            openings[i][j] = [v,r]
    return G2, openings

def check_graph(G,N):
    assert len(G) == N, "G has wrong size"
    for r in G:
        assert len(r) == N, "G has wrong size"
    return True

# Takes a commitment to a graph, and opens all the commitments to reveal the graph
def open_graph(G2,N, openings):
    G = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            v = G2[i][j]
            m,r = openings[i][j]
            assert pedersen_open(v, m, r)
            G[i][j] = m
    return G


# Takes a commitment to a graph, and a claimed set of entries which should open a hamiltonian cycle
# Returns True if the opened nodes form a hamiltonian cycle
def testcycle(graph, N, nodes, openings):
    assert len(nodes) == N
    from_list = [n[0] for n in nodes]
    to_list = [n[1] for n in nodes]
    for i in range(N):
        assert i in from_list
        assert i in to_list
        assert nodes[i][1] == nodes[(i+1)%N][0]

    for i in range(N):
        src,dst = nodes[i]
        r = openings[i]
        # print(f'trying to open {src}->{dst} {r} {graph[src][dst]}')
        assert pedersen_open(graph[src][dst], 1, r)
    return True

# Given a graph, and a permutation, shuffle the graph using the permutation
def permute_graph(G, N, permutation):
    G_permuted = [[G[permutation[i]][permutation[j]] for j in range(N)] for i in range(N)]
    return G_permuted

# given a set of commitment private values, and a subset of these indexes
# return a vector of the randomness needed to open the commitments.
def get_r_vals(openings,N, cycle):
    rvals = []
    for x in cycle:
        m,r = openings[x[0]][x[1]]
        rvals.append(r)
    return rvals


# Iterated Fiat Shamir, take previous state and current graph
def hash_committed_graph(G, state, comm_params):
    fs_state = sha256(str(comm_params).encode())
    fs_state.update(state)
    first_message = "".join([str(x) for xs in G for x in xs])
    fs_state.update(first_message.encode())
    iterated_state = fs_state.digest()
    return iterated_state 
