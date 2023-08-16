from datetime import datetime

import ed25519

KILOBYTE = 1024
ED25519_PUBKEY_LENGTH = 32


class MemoryChip:
    def __init__(self, size: int):
        self._data = bytearray(size)

    def read(self, address: int) -> int:
        return self._data[address]

    def write(self, address: int, byte: int):
        raise NotImplementedError("write must be implemented by subclass")

    def size(self) -> int:
        return len(self._data)


class Flash(MemoryChip):
    """Readable and writeable memory."""

    def write(self, address: int, byte: int):
        self._data[address] = byte


class PROM(MemoryChip):
    """One time programmable fuse ROM."""

    def write(self, address: int, byte: int):
        self._data[address] |= byte


class MCU:
    """Emulates a microcontroller that can execute Python code!"""

    PROGRAM_INSTRUCTION_SEGMENT = 0
    STATIC_DATA_SEGMENT = 1
    DYNAMIC_DATA_SEGMENT = 2

    PROGRAM_INSTRUCTION_SEGMENT_OFFSET = 0
    STATIC_DATA_SEGMENT_OFFSET = 1 * KILOBYTE
    DYNAMIC_DATA_SEGMENT_OFFSET = 2 * KILOBYTE

    def __init__(self):
        self._memory_chips = (
            Flash(1 * KILOBYTE),  # PROGRAM_INSTRUCTION_SEGMENT
            PROM(1 * KILOBYTE),  # STATIC_DATA_SEGMENT
            Flash(1 * KILOBYTE),  # DYNAMIC_DATA_SEGMENT
        )

    def resolve_address(self, address):
        for chip in self._memory_chips:
            if address < chip.size():
                return chip, address
            address -= chip.size()

        raise Exception("Address out of range.")

    def read(self, address: int) -> int:
        chip, address = self.resolve_address(address)
        return chip.read(address)

    def write(self, address: int, byte: int):
        chip, address = self.resolve_address(address)
        chip.write(address, byte)

    def verify_signature(self, image: bytes, signature: bytes):
        try:
            verifying_key = bytes(
                self.read(address)
                for address in range(
                    self.STATIC_DATA_SEGMENT_OFFSET,
                    self.STATIC_DATA_SEGMENT_OFFSET + ED25519_PUBKEY_LENGTH,
                )
            )
            ed25519.VerifyingKey(verifying_key).verify(signature, image)
        except ed25519.BadSignatureError:
            raise Exception("Signature verification failed.")

    def flash(self, segment: int, image: bytes, signature: bytes = None) -> bool:
        if segment < 0:
            raise Exception("Segment number must not be negative.")

        if segment == self.PROGRAM_INSTRUCTION_SEGMENT:
            self.verify_signature(image, signature)

        for address, byte in enumerate(image):
            self._memory_chips[segment].write(address, byte)

        return True

    def dump(self, segment: int) -> bytes:
        result = b""

        chip = self._memory_chips[segment]
        for address in range(chip.size()):
            result += chip.read(address).to_bytes(1, "big")

        return result

    def run(self):
        program = bytes(
            self.read(address)
            for address in range(
                self.PROGRAM_INSTRUCTION_SEGMENT_OFFSET, self.STATIC_DATA_SEGMENT_OFFSET
            )
        )
        program = program.strip(b"\x00").decode()

        exec(
            program,
            {"__builtins__": None},
            {
                "mcu": self,
                "print": print,
                "now": datetime.now,
                "get_logfile": lambda timestamp: open(f"logs/{timestamp}.txt", "a+"),
            },
        )
