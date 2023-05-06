import os
import tempfile

print("One Small Byte For Pwn, One Giant Leap For Flag")
print("Leap >>>")
leap = int(input())
print("Byte >>>")
new_byte = int(input())

with open("chal.bin", "rb") as f:
    contents = f.read()

contents = contents[:leap] + bytes([new_byte]) + contents[leap+1:]

with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    temp_file.write(contents)

os.system("chmod +x %s" %temp_file.name)
os.system(temp_file.name)
os.remove(temp_file.name)