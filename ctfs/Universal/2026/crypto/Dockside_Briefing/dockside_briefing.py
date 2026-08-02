## TEST 2222

import math
import os
import secrets
import select
import sys
import textwrap

from Crypto.Util.number import bytes_to_long, getPrime


DEFAULT_FLAG = "uctf{dev-dockside-briefing}"
STATION_NAME = os.getenv("STATION_NAME", "Hermes Training Station")
BRIEFING_NAME = os.getenv("BRIEFING_NAME", "Dockside Briefing")


def get_flag() -> str:
    return os.getenv("FLAG", DEFAULT_FLAG).strip()


def get_reply_timeout() -> int:
    raw_timeout = os.getenv("REPLY_TIMEOUT", "30")
    try:
        timeout = int(raw_timeout)
    except ValueError:
        return 30
    return max(timeout, 1)


def get_token_bytes() -> int:
    raw_size = os.getenv("TOKEN_BYTES", "12")
    try:
        token_bytes = int(raw_size)
    except ValueError:
        return 12
    return max(token_bytes, 4)


def build_rsa_prompt(message: bytes) -> tuple[int, int, int]:
    exponent = 3
    message_int = bytes_to_long(message)
    message_power = pow(message_int, exponent)
    minimum_modulus_bits = max(1024, message_power.bit_length() + 64)
    prime_bits = max(512, (minimum_modulus_bits + 1) // 2)

    while True:
        prime_p = getPrime(prime_bits)
        prime_q = getPrime(prime_bits)
        if prime_p == prime_q:
            continue
        if math.gcd(exponent, prime_p - 1) != 1:
            continue
        if math.gcd(exponent, prime_q - 1) != 1:
            continue

        modulus = prime_p * prime_q
        if message_power < modulus:
            ciphertext = pow(message_int, exponent, modulus)
            return exponent, modulus, ciphertext


def build_banner(timeout_seconds: int, exponent: int, modulus: int, ciphertext: int) -> str:
    return textwrap.dedent(
        f"""\
        [{STATION_NAME} // {BRIEFING_NAME}]
        Candidate link established.
        Recover the validation token and return it before the uplink window closes.
        Window: {timeout_seconds}s

        e = {exponent}
        n = {modulus}
        c = {ciphertext}

        reply> """
    )


def write_output(message: str) -> None:
    sys.stdout.write(message)
    sys.stdout.flush()


def read_reply(timeout_seconds: int) -> bytes | None:
    ready, _, _ = select.select([sys.stdin.buffer], [], [], timeout_seconds)
    if not ready:
        return None
    return sys.stdin.buffer.readline()


def main() -> None:
    timeout_seconds = get_reply_timeout()
    challenge_token = secrets.token_hex(get_token_bytes())
    exponent, modulus, ciphertext = build_rsa_prompt(challenge_token.encode("utf-8"))

    write_output(build_banner(timeout_seconds, exponent, modulus, ciphertext))

    raw_response = read_reply(timeout_seconds)
    if raw_response is None:
        write_output("\nTransmission window expired.\n")
        return
        
    flag = get_flag()

    response = raw_response.decode("utf-8", errors="ignore").strip()
    if response == challenge_token:
        write_output(f"\nDispatch accepted. {flag}\n")
        return

    write_output("\nDispatch mismatch. Link terminated.\n")


if __name__ == "__main__":
    main()