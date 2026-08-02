import json
import os
import secrets
import sys
import textwrap


DEFAULT_FLAG = "uctf{dev-bonded-ledger}"
OFFICE_NAME = os.getenv("OFFICE_NAME", "North Quay Bond Office")
DESK_NAME = os.getenv("DESK_NAME", "Wax Counter")
Q = 3329
N = 70


def get_flag() -> str:
    return os.getenv("FLAG", DEFAULT_FLAG).strip()


def sample_noise(width: int) -> list[int]:
    return [secrets.randbits(1) - secrets.randbits(1) for _ in range(width)]


def multiply_matrix_vector(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(row[index] * vector[index] for index in range(len(vector))) for row in matrix]


def dot(left: list[int], right: list[int]) -> int:
    return sum(left[index] * right[index] for index in range(len(left)))


def keygen() -> tuple[list[list[int]], list[int], list[int]]:
    secret = sample_noise(N)
    matrix = [[secrets.randbelow(Q) for _ in range(N)] for _ in range(N)]
    error = sample_noise(N)
    matrix_secret = multiply_matrix_vector(matrix, secret)
    public = [(matrix_secret[index] + error[index]) % Q for index in range(N)]
    return matrix, secret, public


def seal_line_item(note: int, matrix: list[list[int]], public: list[int]) -> tuple[list[int], int]:
    nonce = sample_noise(N)
    vector_error = sample_noise(N)
    scalar_error = sample_noise(1)[0]
    matrix_nonce = multiply_matrix_vector(matrix, nonce)
    wrapped_vector = [(matrix_nonce[index] + vector_error[index]) % Q for index in range(N)]
    wrapped_note = (dot(public, nonce) + scalar_error + note) % Q
    return wrapped_vector, wrapped_note


def encode_public_record(matrix: list[list[int]], public: list[int]) -> str:
    return json.dumps({"q": Q, "n": N, "A": matrix, "t": public}, separators=(",", ":"))


def build_banner(matrix: list[list[int]], public: list[int]) -> str:
    public_record = encode_public_record(matrix, public)
    return textwrap.dedent(
        f"""\
        [{OFFICE_NAME} // {DESK_NAME}]
        Outgoing line items must carry the house seal before they leave the ledger room.
        The public filing copy is posted below for anyone handling intake.

        public = {public_record}

        Commands:
          public   show the filing copy again
          seal     wrap a one-byte line item
          getflag  present the private seal
          help     show this menu
          exit     leave the counter
        """
    )


def parse_secret_guess(raw_guess: str) -> list[int] | None:
    candidate = raw_guess.strip()
    if not candidate:
        return None

    try:
        parsed = json.loads(candidate)
        if not isinstance(parsed, list):
            return None
        values = [int(item) for item in parsed]
    except json.JSONDecodeError:
        pieces = candidate.replace(",", " ").split()
        try:
            values = [int(piece) for piece in pieces]
        except ValueError:
            return None
    except (TypeError, ValueError):
        return None

    if len(values) != N:
        return None
    if any(value not in (-1, 0, 1) for value in values):
        return None
    return values


def write_output(message: str) -> None:
    sys.stdout.write(message)
    sys.stdout.flush()


def main() -> None:
    matrix, secret, public = keygen()
    write_output(build_banner(matrix, public))

    while True:
        write_output("\nledger> ")
        try:
            command = input().strip().lower()
        except EOFError:
            write_output("\nCounter closed.\n")
            return

        if command in {"help", "?"}:
            write_output(build_banner(matrix, public))
            continue

        if command == "public":
            write_output(encode_public_record(matrix, public) + "\n")
            continue

        if command in {"seal"}:
            write_output("Line item (0-255): ")
            try:
                note = int(input().strip())
            except (EOFError, ValueError):
                write_output("Only unsigned byte values fit on this form.\n")
                continue

            if not 0 <= note <= 255:
                write_output("Only unsigned byte values fit on this form.\n")
                continue

            wrapped_vector, wrapped_note = seal_line_item(note, matrix, public)
            write_output(
                "sealed = "
                + json.dumps({"u": wrapped_vector, "v": wrapped_note}, separators=(",", ":"))
                + "\n"
            )
            continue

        if command == "getflag":
            write_output("Private seal (JSON list or space-separated ternary vector): ")
            try:
                guess_input = input()
            except EOFError:
                write_output("\nCounter closed.\n")
                return

            guess = parse_secret_guess(guess_input)
            if guess is None:
                write_output("That is not a valid seal impression.\n")
                continue

            if guess == secret:
                write_output(f"Archive copy released. {get_flag()}\n")
                return

            write_output("Seal mismatch. The ledger stays closed.\n")
            continue

        if command == "exit":
            write_output("Counter closed.\n")
            return

        write_output("Unknown command. Type 'help' for the counter menu.\n")


if __name__ == "__main__":
    main()