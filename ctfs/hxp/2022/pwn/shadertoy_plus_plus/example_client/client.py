from pwn import *
from io import BytesIO
import base64
from PIL import Image

file = open("shader.txt", "rb")
shader = file.read()
file.close()
shader = shader.ljust(4095)

io = remote("localhost", 27500)

if True:
    ## If PoW is required...
    io.readuntil(b"please give S such that sha256(unhex(\"")
    prefix = io.readuntil(b"\"")[:-1]
    io.readuntil(b"ends with ")
    bits = io.readuntil(b" ")[:-1]
    print("[+] calculating PoW...")
    result = subprocess.run(["./pow-solver", bits.decode("ascii"), prefix.decode("ascii")], stdout=subprocess.PIPE, text=True)
    print("[+] finished calc hash: " + result.stdout)
    io.send(result.stdout)

io.readuntil("How many")
io.sendline(b"1")

io.send(shader)

io.readuntil("Sending PNG image as base64...\n")
data = io.readline()[:-1]
imgRaw = base64.b64decode(data)
imgAsIo = BytesIO(imgRaw)
img = Image.open(imgAsIo)
img.show()

finalMessage = io.readline()
print(finalMessage)

io.close()
