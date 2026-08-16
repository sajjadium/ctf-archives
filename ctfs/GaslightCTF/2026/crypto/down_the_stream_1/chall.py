def next_register(register: int) -> int:
    for _ in range(8):
        feedback = (((register >> 7) & 1) ^
                    ((register >> 5) & 1) ^
                    ((register >> 4) & 1) ^
                    ((register >> 3) & 1))
        register = ((register << 1) | feedback) & 0xff

    return register

def LFSR(pt_bytes: bytes, IV: int) -> bytes:
    register = IV
    ct = bytearray()
    ct.append(pt_bytes[0] ^ register)

    for i in range(1, len(pt_bytes)):
        register = next_register(register)
        ct.append(pt_bytes[i] ^ register)
    
    return bytes(ct)

if __name__ == '__main__':
    with open('gaslight-down-the-stream-1/flag_and_IV.txt', 'r') as file:
        flag = file.readline().strip()
        IV = file.readline().strip()

    flag = flag.encode()
    IV = int(IV, 16)
    print(LFSR(flag, IV).hex())
    