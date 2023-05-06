from .lfsr import LFSR
from .mode import Mode


def _should_invert_1(mode: Mode) -> bool:
	return mode in (Mode.Authentication, Mode.Data)

def _should_invert_2(mode: Mode) -> bool:
	return mode in (Mode.DiskKey, Mode.Data)

class Cipher:
	mode: Mode
	carry: int
	lfsr_1: LFSR
	lfsr_2: LFSR

	def __init__(self, key_bytes: bytes, mode: Mode):
		self.mode = mode
		self.carry = 0

		assert len(key_bytes) == 8, "Key must be 8 bytes long"
		key = int.from_bytes(key_bytes, "big")
		key_1 = (key & 0xffffff0000000000) >> 40
		key_2 = (key & 0x000000ffffffffff)
		lfsr_seed_1 = ((key_1 & 0xfffff8) << 1) | 8 | (key_1 & 7)
		lfsr_seed_2 = ((key_2 & 0xfffffffff8) << 1) | 8 | (key_2 & 7)
		self.lfsr_1 = LFSR(25, lfsr_seed_1, 0x19e4001)
		self.lfsr_2 = LFSR(41, lfsr_seed_2, 0xfdc0000001)

	def _get_lfsr_byte(self) -> int:
		byte_1 = self.lfsr_1.next_byte()
		byte_2 = self.lfsr_2.next_byte()

		if _should_invert_1(self.mode):
			byte_1 = ~byte_1 & 0xff

		if _should_invert_2(self.mode):
			byte_2 = ~byte_2 & 0xff

		result = byte_1 + byte_2 + self.carry
		self.carry = (result >> 8) & 1
		return result & 0xff

	def _lfsrify_byte(self, byte: int) -> int:
		return byte ^ self._get_lfsr_byte()

	def encrypt(self, data: bytes) -> bytes:
		return bytes(self._lfsrify_byte(byte) for byte in data)

	def decrypt(self, data: bytes) -> bytes:
		return bytes(self._lfsrify_byte(byte) for byte in data)
