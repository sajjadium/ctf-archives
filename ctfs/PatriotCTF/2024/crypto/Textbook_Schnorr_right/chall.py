from sage.all import *
import secrets
import hashlib
import sys
import signal
import re

class EllipticCurveCrypto:
    """
    Elliptic Curve Cryptography using the secp256k1 curve.
    """

    def __init__(self):
        self.p = [<REDACTED>]
        self.q = [<REDACTED>]
        self.K = GF(self.p)
        self.a = self.K([<REDACTED>])
        self.b = self.K([<REDACTED>])
        self.curve = EllipticCurve(self.K, [self.a, self.b])
        self.generator = self.curve(
            [<REDACTED>],
            [<REDACTED>],
        )
        # Generate private and public keys
        self.private_key = secrets.randbelow(self.q)
        self.public_key = self.private_key * self.generator
        print(f"Public Key: {self.public_key}")

    @staticmethod
    def bytes_to_int(b):
        return int.from_bytes(b, byteorder='big')

    @staticmethod
    def int_to_bytes(i):
        return i.to_bytes((i.bit_length() + 7) // 8, byteorder='big')

    def compute_hash(self, target):
        hash_int = int(hashlib.sha256(str(target).encode()).hexdigest(), 16)
        return hash_int % self.q

    def sign(self, message):
        r = secrets.randbelow(self.q)
        R = r * self.generator
        R_int = int(R.xy()[0] + R.xy()[1])
        h = self.compute_hash(R_int | message)
        s = (r + self.private_key * h) % self.q
        return s, R

    def verify(self, message, signature):
        s, R = signature
        R_int = int(R.xy()[0] + R.xy()[1])
        h = self.compute_hash(R_int | message)
        left_side = s * self.generator
        right_side = R + h * self.public_key
        return left_side == right_side

class TimeoutInput:

    class TimeoutError(Exception):
        """Custom exception for input timeout."""
        pass

    @staticmethod
    def timeout_handler(signum, frame):
        raise TimeoutInput.TimeoutError("Input timed out!")

    @staticmethod
    def get_input(prompt, timeout=10):
        """
        Get user input with a timeout.
        :param prompt: The prompt to display to the user.
        :param timeout: The time limit for input in seconds.
        :return: The user's input as a string.
        """
        # Set the signal for a timeout
        signal.signal(signal.SIGALRM, TimeoutInput.timeout_handler)
        signal.alarm(timeout)
        try:
            user_input = input(prompt)
            signal.alarm(0)  # Cancel the timer
            return user_input
        except TimeoutInput.TimeoutError:
            print("No input received within the time limit.")
            sys.exit(0)

def display_flag():
    """Read and display the flag from the 'flag.txt' file."""
    try:
        with open('flag.txt', 'r') as f:
            flag = f.read().strip()
            print(f"Congratulations! Your flag is: {flag}")
    except FileNotFoundError:
        print("Flag file not found.")

def verify_message(separator, words, signature, ecc_instance):
    """
    Verify the provided signature for the message constructed from words and separator.
    """
    message_bytes = separator.join(word.encode() for word in words) + separator
    message_int = int.from_bytes(message_bytes, byteorder='big')
    if ecc_instance.verify(message_int, signature):
        display_flag()
        sys.exit(0)
    else:
        print("Verification failed.")
        sys.exit(0)


def main():
    # Initialize the elliptic curve cryptography instance
    ecc = EllipticCurveCrypto()

    # Test the signing and verification process
    test_message = ecc.bytes_to_int("test".encode())
    s_test, R_test = ecc.sign(test_message)
    assert ecc.verify(test_message, (s_test, R_test))

    # Regular expression patterns for input validation
    separator_pattern = re.compile(r'^[0-9a-fA-F]{2}$')
    word_pattern = re.compile(r'^[0-9a-fA-F]{6}$')

    # Get separator input
    separator_hex = TimeoutInput.get_input("Enter separator as a hex value (2 digits): ")
    if not separator_pattern.match(separator_hex):
        print("Invalid separator format.")
        sys.exit(0)
    separator = bytes.fromhex(separator_hex)

    # Get words input
    words_hex = []
    for i in range(8):
        prompt = f"Enter 3-letter word {i + 1} as a hex value (6 digits): "
        word_hex = TimeoutInput.get_input(prompt)
        if not word_pattern.match(word_hex):
            print("Invalid word format.")
            sys.exit(0)
        words_hex.append(word_hex)

    try:
        words = [bytes.fromhex(word_hex).decode('ascii') for word_hex in words_hex]
    except ValueError:
        print("Invalid ASCII encoding in words.")
        sys.exit(0)

    if any(len(word) != 3 for word in words):
        print("Words must be 3-letter ASCII words.")
        sys.exit(0)

    # Get signature components
    try:
        hex_x_R = input("Enter the x-coordinate of signature R (in hex): ")
        x_R = int(hex_x_R, 16)
        hex_y_R = input("Enter the y-coordinate of signature R (in hex): ")
        y_R = int(hex_y_R, 16)
        hex_signature_s = input("Enter signature s (in hex): ")
        signature_s = int(hex_signature_s, 16)
    except ValueError:
        print("Invalid input for signature components.")
        sys.exit(0)

    if not (0 < signature_s < ecc.q):
        print("Illegal value of s.")
        sys.exit(0)

    # Construct the point R
    try:
        R = ecc.curve(x_R, y_R)
    except ValueError:
        print("Point R does not lie on the curve.")
        sys.exit(0)

    # Verify the message and signature
    verify_message(separator, words, (signature_s, R), ecc)

if __name__ == "__main__":
    main()