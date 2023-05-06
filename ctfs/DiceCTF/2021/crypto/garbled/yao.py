from block_cipher import encrypt, decrypt
from random import shuffle, randrange


def generate_random_label():
    return randrange(0, 2**24)


def garble_label(key0, key1, key2):
    """
    key0, key1 = two input labels
    key2 = output label
    """
    gl = encrypt(key2, key0, key1)
    validation = encrypt(0, key0, key1)
    return (gl, validation)


def evaluate_gate(garbled_table, key0, key1):
    """
    Return the output label unlocked by the two input labels,
    or raise a ValueError if no entry correctly decoded
    """
    for g in garbled_table:
        gl, v = g
        label = decrypt(gl, key0, key1)
        validation = decrypt(v, key0, key1)
        
        if validation == 0:
            return label
        
    raise ValueError("None of the gates correctly decoded; invalid input labels")


def evaluate_circuit(circuit, g_tables, inputs):
    """
    Evaluate yao circuit with given inputs.
    
    Keyword arguments:
    circuit   -- dict containing circuit spec
    g_tables  -- garbled tables of yao circuit
    inputs  -- dict mapping wires to labels
    
    Returns:
    evaluation -- a dict mapping output wires to the result labels
    """
    gates        = circuit["gates"] # dict containing circuit gates
    wire_outputs = circuit["outputs"]   # list of output wires
    wire_inputs  = {}               # dict containing Alice and Bob inputs
    evaluation   = {}               # dict containing result of evaluation

    wire_inputs.update(inputs)
    
    # Iterate over all gates
    for gate in sorted(gates, key=lambda g: g["id"]):
        gate_id, gate_in = gate["id"], gate["in"]

        key0 = wire_inputs[gate_in[0]]
        key1 = wire_inputs[gate_in[1]]
        
        garbled_table = g_tables[gate_id]
        msg = evaluate_gate(garbled_table, key0, key1)
        
        wire_inputs[gate_id] = msg

    # After all gates have been evaluated, we populate the dict of results
    for out in wire_outputs:
        evaluation[out] = wire_inputs[out]

    return evaluation
    
    
    
    

class GarbledGate:
    """A representation of a garbled gate.
    Keyword arguments:
    gate  -- dict containing gate spec
    keys  -- dict mapping each wire to a pair of keys
    """

    def __init__(self, gate, keys):
        self.keys                = keys          # dict of yao circuit keys
        self.input               = gate["in"]    # list of inputs' ID
        self.output              = gate["id"]    # ID of output
        self.gate_type           = gate["type"]  # Gate type: OR, AND, ...
        self.garbled_table       = {}            # The garbled table of the gate

        labels0 = keys[self.input[0]]
        labels1 = keys[self.input[1]]
        labels2 = keys[self.output]
        
        if self.gate_type == "AND":
            self.garbled_table = self._gen_garbled_AND_gate(labels0, labels1, labels2)
        else:
            raise NotImplementedError("Gate type `{}` is not implemented".format(self.gate_type))


    def _gen_garbled_AND_gate(self, labels0, labels1, labels2):
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
        # randomly shuffle the table so you don't know what the labels correspond to
        shuffle(G)
        
        return G


    def get_garbled_table(self):
        """Return the garbled table of the gate."""
        return self.garbled_table
    
    


class GarbledCircuit:
    """
    A representation of a garbled circuit.
    Keyword arguments:
    circuit -- dict containing circuit spec
    """

    def __init__(self, circuit):
        self.circuit        = circuit
        self.gates          = circuit["gates"]  # list of gates
        self.wires          = set()             # list of circuit wires

        self.keys           = {}  # dict of keys
        self.garbled_tables = {}  # dict of garbled tables

        # Retrieve all wire IDs from the circuit
        for gate in self.gates:
            self.wires.add(gate["id"])
            self.wires.update(set(gate["in"]))
        self.wires = list(self.wires)

        self._gen_keys()
        self._gen_garbled_tables()


    def _gen_keys(self):
        """Create pair of keys for each wire."""
        for wire in self.wires:
            self.keys[wire] = (
                    generate_random_label(),
                    generate_random_label()
                    )

    def _gen_garbled_tables(self):
        """Create the garbled table of each gate."""
        for gate in self.gates:
            garbled_gate = GarbledGate(gate, self.keys)
            self.garbled_tables[gate["id"]] = garbled_gate.get_garbled_table()

    def get_garbled_tables(self):
        """Return dict mapping each gate to its garbled table."""
        return self.garbled_tables

    def get_keys(self):
        """Return dict mapping each wire to its pair of keys."""
        return self.keys