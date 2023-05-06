
import json
from block_cipher import decrypt

from random import randrange
from yao_circuit import GarbledGate as Ggate

flag = b'****************'


circuit_filename = "circuit_map.json"
with open(circuit_filename) as json_file:
    circuit = json.load(json_file)

def init_keys(circuit):
    keys = {}
    gates          = circuit["gates"] 
    wires          = set()
    for gate in gates:
        wires.add(gate["id"])
        wires.update(set(gate["in"]))
    for wireidx in wires:
        # the index of keys[wireidx] 1 and 0 means TRUE and FALSE in garbled circuit
        keys[wireidx] = (randrange(0, 2**24),randrange(0, 2**24))
    return keys
                    
def validate_the_circuit(geta_table, key0, key1):
    for g in geta_table:
        gl, v = g
        label = decrypt(gl, key0, key1)
        validation = decrypt(v, key0, key1)
        
        if validation == 0:
            return label            
            
def init_garbled_tables(circuit,keys):
    gates = circuit["gates"]
    garbled_tables = {}
    for gate in gates:
        garbled_table = Ggate(gate, keys)
        garbled_tables[gate["id"]] = garbled_table
    return garbled_tables


keys = init_keys(circuit)
G_Table = init_garbled_tables(circuit,keys)
# ic(keys)
# ic(G_Table)

# hint
# circuit wiring has only one situation mack ASSERT be true
geta_table = G_Table[9]
key0 = keys[7][1]
key1 = keys[4][0]
msg = validate_the_circuit(geta_table, key0, key1)
assert msg == keys[circuit["out"][0]][1]
# 

with open("public_data.py","r+") as f:
    print("G_Table = {}".format(G_Table),file=f)
    
with open("private_data.py","r+") as f:
    print("keys = {}".format(keys),file=f)
    print("flag = {}".format(str(flag)),file=f)
    
    
