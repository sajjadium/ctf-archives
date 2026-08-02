import os
import secrets
import select
import sys
import textwrap
import time

from Crypto.Util.number import bytes_to_long, getPrime, inverse


DEFAULT_FLAG = "uctf{dev-transit-seal}"
STATION_NAME = os.getenv("STATION_NAME", "North Quay Relay")
SEAL_NAME = os.getenv("SEAL_NAME", "Transit Seal")


def get_flag() -> str:
    return os.getenv("FLAG", DEFAULT_FLAG).strip()


def get_int_env(name: str, default: int, minimum: int) -> int:
    raw_value = os.getenv(name, str(default))
    try:
        value = int(raw_value)
    except ValueError:
        return default
    return max(value, minimum)


def build_rsa_keypair(bits: int) -> tuple[int, int, int]:
    exponent = 65537
    prime_bits = bits // 2

    while True:
        prime_p = getPrime(prime_bits)
        prime_q = getPrime(prime_bits)
        if prime_p == prime_q:
            continue

        phi = (prime_p - 1) * (prime_q - 1)
        if phi % exponent == 0:
            continue

        modulus = prime_p * prime_q
        private_exponent = inverse(exponent, phi)
        return modulus, exponent, private_exponent


def rsa_private_pow(base: int, exponent: int, modulus: int) -> int:
    result = 1
    relay_mask = base
    base = base % modulus
    bit_index = 0
    e = exponent

    while e:
        if e & 1:
            result = (result * base) % modulus
            if (relay_mask >> bit_index) & 1:
                result = pow(result, modulus - 1, modulus) * result % modulus

        base = (base * base) % modulus
        e >>= 1
        bit_index += 1

    return result

def build_banner(modulus: int, exponent: int, target_ciphertext: int, key_bits: int, relay_limit: int) -> str:
    return textwrap.dedent(
        f"""\
        [{STATION_NAME} // {SEAL_NAME}]
        Hermes relay traffic arrives as sealed ciphertext over the quay relay.
        The terminal exposes the public line data and one target shipment that must be released intact.
        Recover the plaintext token for the target ciphertext below.

        Public modulus bits: {key_bits}
        Query limit: {relay_limit}

        e = {exponent}
        n = {modulus}
        ciphertext = {target_ciphertext:064x}

        Commands:
          relay <hex-ciphertext>
          release <hex-plaintext>
          help
          quit

        command> """
    )


def write_output(message: str) -> None:
    sys.stdout.write(message)
    sys.stdout.flush()


def read_command(timeout_seconds: int) -> str | None:
    ready, _, _ = select.select([sys.stdin.buffer], [], [], timeout_seconds)
    if not ready:
        return None
    return sys.stdin.buffer.readline().decode("utf-8", errors="ignore")


def parse_hex_int(raw_value: str) -> int | None:
    candidate = raw_value.strip().lower()
    if candidate.startswith("0x"):
        candidate = candidate[2:]
    if not candidate:
        return None
    try:
        return int(candidate, 16)
    except ValueError:
        return None


def handle_relay(
    raw_ciphertext: str,
    modulus: int,
    private_exponent: int,
) -> bool:
    ciphertext_value = parse_hex_int(raw_ciphertext)
    if ciphertext_value is None or ciphertext_value >= modulus:
        write_output("relay rejected\n")
        return False

    if not rsa_private_pow(ciphertext_value, private_exponent, modulus):
        write_output("relay failed\n")
        return False

    write_output("relay complete\n")
    return True


def handle_release(raw_plaintext: str, target_plaintext: int, flag: str) -> bool:
    plaintext_value = parse_hex_int(raw_plaintext)
    if plaintext_value is None:
        write_output("release rejected\n")
        return False

    if plaintext_value == target_plaintext:
        write_output(f"release accepted {flag}\n")
        return True

    write_output("release rejected\n")
    return False


def main() -> None:
    flag = get_flag()
    key_bits = get_int_env("KEY_BITS", 1024, 512)
    session_timeout = get_int_env("SESSION_TIMEOUT", 180, 30)
    relay_limit = get_int_env("RELAY_LIMIT", 8200, key_bits)

    modulus, exponent, private_exponent = build_rsa_keypair(key_bits)
    target_plaintext = bytes_to_long(secrets.token_bytes(32))
    target_ciphertext = pow(target_plaintext, exponent, modulus)

    write_output(build_banner(modulus, exponent, target_ciphertext, key_bits, relay_limit))

    relays_used = 0
    while True:
        raw_command = read_command(session_timeout)
        if raw_command is None:
            write_output("\nsession expired\n")
            return

        command = raw_command.strip()
        if not command:
            write_output("command> ")
            continue

        if command == "help":
            write_output("relay <hex-ciphertext> | release <hex-plaintext> | quit\n")
            write_output("command> ")
            continue

        if command == "quit":
            write_output("link closed\n")
            return

        if command.startswith("relay "):
            if relays_used >= relay_limit:
                write_output("relay budget exhausted\n")
                write_output("command> ")
                continue

            relays_used += 1
            handle_relay(
                command[6:],
                modulus,
                private_exponent,
            )
            write_output("command> ")
            continue

        if command.startswith("release "):
            if handle_release(command[8:], target_plaintext, flag):
                return
            write_output("command> ")
            continue

        write_output("unknown command\n")
        write_output("command> ")


if __name__ == "__main__":
    main()