You have been hired by a tech company to assess the security of thier quantum communication system. The system uses the BB84 protocol for key distribution. During your assessment, you've intercepted some qubits and their bases during an exchange between Alice and Bob, but some of Bob's measurements are incorrect at every third qubit due to an eavesdropping scenario. Since this is a new system still in testing, the seed space is restricted to positive integers between 1 and 100.

Qubits = [0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1]

Bases = ['R', 'R', 'D', 'R', 'R', 'R', 'R', 'R', 'D', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'D', 'R', 'D', 'D', 'R', 'R', 'D', 'D', 'D', 'R', 'R', 'D', 'R', 'R', 'D', 'R', 'D', 'D', 'D', 'R', 'D', 'R', 'D', 'R', 'D', 'D', 'R', 'R', 'R', 'R', 'D', 'R', 'R', 'R', 'D', 'D', 'D', 'D', 'R', 'D', 'D', 'R', 'D', 'R', 'R', 'R', 'R', 'D', 'D', 'D', 'R', 'D', 'R', 'R', 'R', 'D', 'D', 'D', 'R', 'R', 'D', 'R', 'D', 'D']

Measurements = [0, 1, ?, 1, 0, ?, 1, 1, ?, 0, 1, ?, 0, 1, ?, 0, 1, ?, 1, 0, ?, 1, 0, ?, 0, 1, ?, 0, 1, ?, 1, 0, ?, 0, 0, ?, 0, 1, ?, 0, 1, ?, 1, 1, ?, 1, 0, ?, 1, 0, ?, 0, 1, ?, 0, 1, ?, 0, 1, ?, 1, 0, ?, 1, 0, ?, 0, 1, ?, 0, 0, ?, 0, 1, ?, 1, 1, ?, 1, 1]

Encrypted Message = [0x23, 0x59, 0x86, 0x1e, 0x60, 0xcf, 0xdc, 0x4e, 0x6a, 0x0b, 0x0c, 0x50, 0xd4, 0x5a, 0x71, 0x87, 0xdb, 0x0c, 0x46, 0x1d, 0x63, 0x44, 0xba, 0x5e, 0x37, 0xd3, 0x9a, 0x4b, 0x77, 0x4b, 0x3d, 0x4b]
