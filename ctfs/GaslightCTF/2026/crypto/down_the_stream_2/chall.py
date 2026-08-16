from unknown_funcs import generate_feedback

def next_register(register: int) -> int:
    for _ in range(16):
        feedback = generate_feedback(register)
        register = ((register << 1) | feedback) & 0xffff

    return register

def LFSR(pt_bytes: bytes, IV: int) -> bytes:
    assert len(pt_bytes) % 2 == 0
    register = IV
    ct = bytearray()
    ct.append(pt_bytes[0] ^ (register >> 8))
    ct.append(pt_bytes[1] ^ (register & 0x00ff))

    for i in range(2, len(pt_bytes), 2):
        register = next_register(register)
        ct.append(pt_bytes[i] ^ (register >> 8))
        ct.append(pt_bytes[i+1] ^ (register & 0x00ff))
    
    return bytes(ct)

if __name__ == '__main__':
    with open('gaslight-down-the-stream-2/flag_and_IV.txt', 'r') as file:
        flag = file.readline().strip()
        IV = file.readline().strip()

    flag = flag.encode()
    IV = int(IV, 16)
    print(LFSR(flag, IV).hex())
    