import os
import uuid
import zlib
import subprocess

try:
    from flag import FLAG
except:
    FLAG = "test{FLAG}"

BANNED_LIST = ['#', '_', '?', ':']
MAX_LEN = 20000
N = 25

rows = []
row = input("C Code:")
while row:
    rows.append(row)
    row = input()
code = "\n".join(rows) + "\n"

if len(code) > MAX_LEN:
    quit()
for c in BANNED_LIST:
    if c in code:
        quit()
        
# Generate unique filenames using UUID
source_path = "/tmp/" + str(uuid.uuid4()) + "_source.c"
output_path = "/tmp/" + str(uuid.uuid4()) + "_output"

# Write the user-provided code to the source file
with open(source_path, "w") as file:
    file.write(code)

# Compile the code using the unique output name
subprocess.run(["sudo", "-u", "nobody", "gcc", "-o", output_path, source_path], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Clean up the source file immediately after compilation
os.truncate(source_path, 0)
os.remove(source_path)
os.sync()

# Exception handler
def terminate(reason, output_path):
    try:
        print(reason)
        os.remove(output_path)
    finally:
        exit()

# Verify the file can be recovered
for i in range(N):
    otp = os.urandom(len(code))
    try:
        # Important note: the intended solution does not require file system access or networking. 
        # As such the sandbox on the flag server is more nuanced than what is shown.
        # However, since this is a CTF, you can solve the chal any way you like (within the rules) :)
        out = subprocess.check_output(["sudo", "-u", "nobody", output_path], input=otp, stderr=subprocess.STDOUT, timeout=15)
        v = int(out.strip())
    except subprocess.TimeoutExpired:
        terminate("Process Timed Out", output_path)
    except subprocess.CalledProcessError:
        terminate("Subprocess returned non-zero exit status", output_path)
    except ValueError:
        terminate("Output conversion failed", output_path)
    
    if zlib.crc32(bytes(a ^ b for a, b in zip(code.encode(), otp))) != v:
        terminate("Output Checksum Mismatch", output_path)
    else:
        print("Checksum Ok i={}".format(i))

# Print flag and clean up
terminate("Wow! You clearly recovered the file so here is your flag: {}".format(FLAG), output_path)
