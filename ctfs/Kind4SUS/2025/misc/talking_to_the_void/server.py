from subprocess import run, PIPE
from secrets import token_bytes
from hashlib import sha256
from base64 import b64encode, b64decode
from time import sleep

class RNG:
	def __init__(self):
		secret = token_bytes(16).hex()
		def digest(state):
			state = secret + state
			state = sha256(state.encode()).digest()
			state = b64encode(state).decode()
			return state
		self._digest = digest
		self._memory = set()
		self.reset()
	def reset(self, seed=""):
		if seed in self._memory:
			print("Nope: hard reset...")
			self.__init__()
			return
		self._state = seed
	def step(self):
		state = self._state
		ans = self._digest(state)
		self._memory.add(ans)
		self._state = ans
		return ans
	def run_shell(self, n):
		n = int(n)
		for i in range(3, 0, -1):
			print("Thinking" + "." * i, flush=True)
			sleep(20)
		state = self.step()
		cmd = state[:n]
		print("Running:", cmd, flush=True)
		res = run([cmd], text=True, stdout=PIPE, stderr=PIPE)
		ans = res.stdout.split()
		ans = [token for token in ans if token.startswith("KSUS")]
		ans = "\n".join(map(self._scramble, ans))
		return ans
	def _scramble(self, message):
		secret = self._state
		secret = b64decode(secret)
		message = message.encode()
		ans = bytes(x ^ y for x, y in zip(message, secret))
		ans = b64encode(ans).decode()
		return ans

def main(attempts=256):
	x = RNG()
	print("""
Options:
> exit
> reset {seed}
> step
> shell {n_char}

Your choice?
""")
	while attempts:
		y = input("?\n")
		if not y:
			continue
		y, *args = y.split()
		if y == "exit":
			break
		elif y == "reset":
			x.reset(*args)
		elif y == "step":
			ans = x.step()
			print(ans)
		elif y == "shell":
			ans = x.run_shell(*args)
			print(ans)
			break
		else:
			print("Invalid choice")
		attempts -= 1

from signal import alarm

if __name__ == "__main__":
	alarm(321)
	try:
		main()
	except Exception:
		print("Something went wrong")
	print("bye!")
