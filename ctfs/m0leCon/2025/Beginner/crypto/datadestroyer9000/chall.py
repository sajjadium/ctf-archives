import os
from random import shuffle

FLAG = os.getenv("SECRET", "This is some veeeeeeeeeeeeeeeeeeeeeeeeery looooooooooooooooooong sample text :D ptm{fakeflag}").encode()
CHUNK_SIZE = 128
BLOCK_SIZE = 32

def gen_otp(): 
    #generate otp for a chunk of data, 128 bytes
    key = os.urandom(CHUNK_SIZE)
    return key

def gen_permutations():
    #generate permutation for every block of 32 bytes in a chunk
    permutations = []
    for _ in range(CHUNK_SIZE//BLOCK_SIZE):
        perm = list(range(BLOCK_SIZE))
        shuffle(perm)
        permutations.append(perm)
    
    return permutations



# generating otp and permutations
otp = gen_otp()
permutations = gen_permutations()



def xor(x: bytes, y: bytes):
    #xor 2 messages with each other
    return bytes(a ^ b for a, b in zip(x, y))

def scramble(block: bytes, perm: list):
    #scramble 32 bytes of a message given the permutation
    result = []
    for i in range(BLOCK_SIZE):
        result.append(block[perm[i]])
    return bytes(result)

def pad(msg: bytes):
    #pad message so that len is multiple of 128
    if len(msg) % CHUNK_SIZE != 0:
        msg += b'\x00'*(CHUNK_SIZE - (len(msg) % CHUNK_SIZE))
    
    return msg

def scramble_chunk(chunk: bytes):
    #apply otp and then scramble bytes in message
    xored = xor(chunk, otp)
    result = b''
    for i in range(CHUNK_SIZE//BLOCK_SIZE):
        current_perm = permutations[i]
        current_block = xored[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE]
        result += scramble(current_block, current_perm)
    
    return result

def destroy_data(data: bytes):
    #put everything together and destroy every chunk of data
    data = pad(data)
    result = b''
    for i in range(len(data)//CHUNK_SIZE):
        curr_chunk = data[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE]
        result += scramble_chunk(curr_chunk)
    
    return result.hex()

def main():
    print("This program allows you to make your data completely unrecognizable!")
    print("I bet you will not be able to recover my secret hehe")
    print(destroy_data(FLAG))
    print()
    print("You can now try this service however you want!")
    while True:
        data = input("> ")
        if len(data) == 0:
            break
        print(destroy_data(bytes.fromhex(data)))

    print("Goodbye!")


if __name__ == "__main__":
    main()