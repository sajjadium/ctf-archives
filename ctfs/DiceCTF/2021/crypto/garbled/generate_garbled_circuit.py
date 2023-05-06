from yao import GarbledCircuit
import json


circuit_filename = "circuit.json"
with open(circuit_filename) as json_file:
    circuit = json.load(json_file)

# creates a new garbled circuit each time
gc = GarbledCircuit(circuit)

g_tables = gc.get_garbled_tables()
keys = gc.get_keys()


print("g_tables = {}".format(repr(g_tables)))
print("\nkeys = {}".format(repr(keys)))
