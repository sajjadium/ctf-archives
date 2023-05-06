from random import shuffle, randrange


from block_cipher import encrypt, decrypt

def garble_label(key0, key1, key2):
    """
    key0, key1 = two input labels
    key2 = output label
    """
    gl = encrypt(key2, key0, key1)
    validation = encrypt(0, key0, key1)
    return (gl, validation)


def GarbledGate( gate, keys): # init g data
    input               = gate["in"]
    output              = gate["id"] 
    gate_type           = gate["type"]
    labels0 = keys[input[0]]
    labels1 = keys[input[1]]
    labels2 = keys[output]
    if gate_type == "AND":
        garbled_table = AND_gate(labels0, labels1, labels2)
    if gate_type == "XOR":
        garbled_table = XOR_gate(labels0, labels1, labels2)
    return garbled_table
        
        
def AND_gate( labels0, labels1, labels2):
    """
    labels0, labels1 = two input labels
    labels2 = output label
    """
    key0_0, key0_1 = labels0
    key1_0, key1_1 = labels1
    key2_0, key2_1 = labels2
    
    G = []
    G.append(garble_label(key0_0, key1_0, key2_0))
    G.append(garble_label(key0_0, key1_1, key2_0))
    G.append(garble_label(key0_1, key1_0, key2_0))
    G.append(garble_label(key0_1, key1_1, key2_1))
    shuffle(G)
    
    return G

def XOR_gate( labels0, labels1, labels2):
    key0_0, key0_1 = labels0
    key1_0, key1_1 = labels1
    key2_0, key2_1 = labels2
    
    G = []
    G.append(garble_label(key0_0, key1_0, key2_0))
    G.append(garble_label(key0_0, key1_1, key2_1))
    G.append(garble_label(key0_1, key1_0, key2_1))
    G.append(garble_label(key0_1, key1_1, key2_0))
    shuffle(G)
    
    return G


def garble_label(key0, key1, key2):
    """
    key0, key1 = two input labels
    key2 = output label
    """
    gl = encrypt(key2, key0, key1)
    validation = encrypt(0, key0, key1)
    return (gl, validation)

