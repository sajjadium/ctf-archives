from math import log2
import random
import secrets
import signal


def gen_pbox(s, n):
    """
    Generate a balanced permutation box for an SPN

    :param s: Integer, number of bits per S-box.
    :param n: Integer, number of S-boxes.
    :return: List of integers, representing the generated P-box.
    """
    return [(s * i + j) % (n * s) for j in range(s) for i in range(n)]


def gen_sbox(n):
    """
    Gen SBox for a given non negative integer n using a random permutation.

    Parameters:
    :param n: Integer, the bit size of sbox

    :return: List of integers, representing 2^n elements corresponding to the
            SBox permutation generated for the input.
    """
    a, b = 2**((n + 1) // 2), 2**(n // 2)
    x = list(range(a))
    random.shuffle(x)
    res = x[:]
    for i in range(b - 1):
        for j in range(len(x)):
            res.insert((i + 2) * j - 1, a * (i + 1) + x[j])
        res = [res[i] for i in res]
    return res


def rotate_left(val, shift, mod):
    """
    Rotate the bits of the value to the left by the shift amount.

    The function rotates the bits of the value to the left by the shift amount,
    wrapping the bits that overflow. The result is then masked by (1<<mod)-1
    to only keep the mod number of least significant bits.

    :param val: Integer, the value to be rotated.
    :param shift: Integer, the number of places to shift the value to the left.
    :param mod: Integer, the modulo to be applied on the result.
    :return: Integer, the rotated value.
    """
    shift = shift % mod
    return (val << shift | val >> (mod - shift)) & ((1 << mod) - 1)


class SPN:
    def __init__(self, SBOX, PBOX, key, rounds):
        """
        Initialize the SPN class with the provided parameters.

        :param SBOX: List of integers representing the S-box.
        :param PBOX: List of integers representing the P-box.
        :param key: List of integers, bytes or bytearray representing the key.
                    LSB BLOCK_SIZE bits will be used
        :param rounds: Integer, number of rounds for the SPN.
        """
        self.SBOX = SBOX
        self.PBOX = PBOX
        self.SINV = [SBOX.index(i) for i in range(len(SBOX))]
        self.PINV = [PBOX.index(i) for i in range(len(PBOX))]
        self.BLOCK_SIZE = len(PBOX)
        self.BOX_SIZE = int(log2(len(SBOX)))
        self.NUM_SBOX = len(PBOX) // self.BOX_SIZE
        self.rounds = rounds
        self.round_keys = self.expand_key(key, rounds)

    def perm(self, inp):
        """
        Apply the P-box permutation on the input.

        :param inp: Integer, the input value to apply the P-box permutation on.
        :return: Integer, the permuted value after applying the P-box.
        """
        ct = 0
        for i, v in enumerate(self.PBOX):
            ct |= (inp >> (self.BLOCK_SIZE - 1 - i) & 1) << (self.BLOCK_SIZE - 1 - v)
        return ct

    def inv_perm(self, inp):
        """
        Apply the inverse P-box permutation on the input.

        :param inp: Integer, the input value to apply the inverse P-box
                    permutation on.
        :return: Integer, the permuted value after applying the inverse P-box.
        """
        ct = 0
        for i, v in enumerate(self.PINV):
            ct |= (inp >> (self.BLOCK_SIZE - 1 - i) & 1) << (self.BLOCK_SIZE - 1 - v)
        return ct

    def sbox(self, inp):
        """
        Apply the S-box substitution on the input.

        :param inp: Integer, the input value to apply the S-box substitution on.
        :return: Integer, the substituted value after applying the S-box.
        """
        ct, BS = 0, self.BOX_SIZE
        for i in range(self.NUM_SBOX):
            ct |= self.SBOX[(inp >> (i * BS)) & ((1 << BS) - 1)] << (BS * i)
        return ct

    def inv_sbox(self, inp: int) -> int:
        """
        Apply the inverse S-box substitution on the input.

        :param inp: Integer, the input value to apply the inverse S-box
                    substitution on.
        :return: Integer, the substituted value after applying the inverse S-box.
        """
        ct, BS = 0, self.BOX_SIZE
        for i in range(self.NUM_SBOX):
            ct |= self.SINV[(inp >> (i * BS)) & ((1 << BS) - 1)] << (BS * i)
        return ct

    def int_to_list(self, inp):
        """
        Convert a len(PBOX)-sized integer to a list of S-box sized integers.

        :param inp: Integer, representing a len(PBOX)-sized input.
        :return: List of integers, each representing an S-box sized input.
        """
        BS = self.BOX_SIZE
        return [(inp >> (i * BS)) & ((1 << BS) - 1)
                for i in range(self.NUM_SBOX - 1, -1, -1)]

    def list_to_int(self, lst):
        """
        Convert a list of S-box sized integers to a len(PBOX)-sized integer.

        :param lst: List of integers, each representing an S-box sized input.
        :return: Integer, representing the combined input as a
                len(PBOX)-sized integer.
        """
        res = 0
        for i, v in enumerate(lst[::-1]):
            res |= v << (i * self.BOX_SIZE)
        return res

    def expand_key(self, key, rounds):
        """
        Derive round keys deterministically from the given key.

        :param key: List of integers, bytes, or bytearray representing the key.
        :param rounds: Integer, number of rounds for the SPN.
        :return: List of integers, representing the derived round keys.
        """
        if isinstance(key, list):
            key = self.list_to_int(key)
        elif isinstance(key, (bytes, bytearray)):
            key = int.from_bytes(key, 'big')
        block_mask = (1 << self.BLOCK_SIZE) - 1
        key = key & block_mask
        keys = [key]
        for _ in range(rounds):
            keys.append(self.sbox(rotate_left(
                keys[-1], self.BOX_SIZE + 1, self.BLOCK_SIZE)))
        return keys

    def encrypt(self, pt):
        """
        Encrypt plaintext using the SPN, where the last round doesn't
        contain the permute operation.

        :param pt: Integer, plaintext input to be encrypted.
        :return: Integer, ciphertext after encryption.
        """
        ct = pt ^ self.round_keys[0]
        for round_key in self.round_keys[1:-1]:
            ct = self.sbox(ct)
            ct = self.perm(ct)
            ct ^= round_key
        ct = self.sbox(ct)
        return ct ^ self.round_keys[-1]

    def decrypt(self, ct):
        """
        Decrypt ciphertext using the SPN, where the last round doesn't
        contain the permute operation.

        :param ct: Integer, ciphertext input to be decrypted.
        :return: Integer, plaintext after decryption.
        """
        ct = ct ^ self.round_keys[-1]
        ct = self.inv_sbox(ct)
        for rk in self.round_keys[-2:0:-1]:
            ct ^= rk
            ct = self.inv_perm(ct)
            ct = self.inv_sbox(ct)
        return ct ^ self.round_keys[0]

    def encrypt_bytes(self, pt):
        """
        Encrypt bytes using the SPN, in ECB on encrypt

        :param pt: bytes, should be multiple of BLOCK_SIZE//8
        :return: bytes, ciphertext after block-by-block encryption
        """
        block_len = self.BLOCK_SIZE // 8
        assert len(pt) % block_len == 0

        int_blocks = [int.from_bytes(pt[i:i + block_len], 'big')
                      for i in range(0, len(pt), block_len)]
        return b''.join(self.encrypt(i).to_bytes(block_len, 'big')
                        for i in int_blocks)


class Challenge:
    def __init__(self, box_size, num_box, num_rounds, max_mess):
        pbox = gen_pbox(box_size, num_box)
        sbox = gen_sbox(box_size)
        key = secrets.randbits(box_size * num_box)
        self.spn = SPN(sbox, pbox, key, num_rounds)
        self.quota = max_mess

    def query(self, text_hex):
        block_len = self.spn.BLOCK_SIZE // 8
        if len(text_hex) & 1:
            text_hex += "0"
        text = bytes.fromhex(text_hex)
        text += bytes((block_len - len(text)) % block_len)

        if self.quota <= 0:
            raise Exception(
                "Encryption quota exceeded, buy pro subscription for $69/month")
        self.quota -= len(text) // block_len
        print("Quota remaining:", self.quota)
        return self.spn.encrypt_bytes(text).hex()

    def get_flag(self, key_guess):
        if key_guess == self.spn.round_keys[0]:
            from flag import flag
            print(flag)
        else:
            raise Exception("There is no free lunch")


if __name__ == "__main__":
    BOX_SIZE = 6
    NUM_BOX = 16
    QUOTA = 50000
    ROUNDS = 5
    PROMPT = ("Choose API option\n"
              "1. Test encryption\n"
              "2. Get Flag\n")
    challenge = Challenge(BOX_SIZE, NUM_BOX, ROUNDS, QUOTA)
    print("sbox:", "".join(hex(i)[2:].zfill(2) for i in challenge.spn.SBOX))
    signal.alarm(500)
    while True:
        try:
            option = int(input(PROMPT))
            if option == 1:
                pt = input("(hex) text: ")
                print(challenge.query(pt))
            elif option == 2:
                key = int(input("(int) key: "))
                challenge.get_flag(key)
                exit(0)
        except Exception as e:
            print(e)
            exit(1)
