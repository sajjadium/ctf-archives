"""
This file is provided as an example of how to load the garbled circuit
and evaluate it with input key labels.

Note: the ACTUAL `g_tables` for this challenge are in `public_data.py`, and are not used in this example.

It will error if the provided inputs are not valid label keys,
ie do not match either of the `keys` made by `generate_garbled_circuit.py`
"""

import json

from yao import evaluate_circuit
from generate_garbled_circuit import g_tables, keys


circuit_filename = "circuit.json"
with open(circuit_filename) as json_file:
    circuit = json.load(json_file)
        

inputs = {}
for i in circuit["inputs"]:
    v = keys[i][1]
    inputs[i] = v

evaluation = evaluate_circuit(circuit, g_tables, inputs)
print("")
print(evaluation)

