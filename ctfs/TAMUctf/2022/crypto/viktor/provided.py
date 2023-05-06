import asyncio
import socket
import hashlib

from time import sleep, time

### CONSTANTS ###
PORTNUM = 49204
TIMEDPRINT = 0.08
FLAG = "[REDACTED]"
CONSTHASH = "667a32132baf411ebf34c81a242d9ef4bf72e288"

def timedOutput(writer, msg, delay):
    for c in msg:
        writer.write(bytes(c, "utf-8"))
        sleep(delay)

def XOR(x, y):
    return "".join([str(hex(int(a, 16)^int(b, 16)))[2:] for a,b in zip(x, y)])

### SERVER STUFF ###
async def handle_client(reader, writer):
    timedOutput(writer, "[==== BOOT SEQUENCE INITATED ====]\n", TIMEDPRINT)
    timedOutput(writer, "Waiting for connection", TIMEDPRINT)
    timedOutput(writer, ".....", 8*TIMEDPRINT)
    timedOutput(writer, "\nData transfer complete\n", TIMEDPRINT)
    timedOutput(writer, "Expected Command Sequence Hash = ", TIMEDPRINT)
    timedOutput(writer, CONSTHASH, TIMEDPRINT)
    timedOutput(writer, "\nPlease enter the commands line by line\n", TIMEDPRINT)
    timedOutput(writer, "When finished enter the command \"EXECUTE\" on the final line\n", TIMEDPRINT)


    inputList = []
    usrInput = (await reader.readline()).decode("utf-8").rstrip()
    while(usrInput != "EXECUTE"):
        inputList.append(usrInput)
        usrInput = (await reader.readline()).decode("utf-8").rstrip()

    hashList = [hashlib.sha1(x.encode()).hexdigest() for x in inputList]
    hashVal = hashList[0]
    for i in range(1, len(hashList)):
        hashVal = XOR(hashVal, hashList[i]) 

    timedOutput(writer, "\nVerifying", TIMEDPRINT)
    timedOutput(writer, ".....\n", 8*TIMEDPRINT)
    if(hashVal == CONSTHASH):
        timedOutput(writer, "Command Sequence Verified\n", TIMEDPRINT)
        timedOutput(writer, "[HAL] Authorization Code = ", TIMEDPRINT)
        timedOutput(writer, FLAG, TIMEDPRINT)
        timedOutput(writer, "\n", TIMEDPRINT)
    else:
        timedOutput(writer, "Invalid Command Sequence\n", TIMEDPRINT)

    timedOutput(writer, "[==== SYSTEM SHUTDOWN ====]\n", TIMEDPRINT)
    writer.close()
    return

async def handle_wrap_timed(reader, writer):
    try:
        await asyncio.wait_for(handle_client(reader, writer), timeout=300)
    except asyncio.exceptions.TimeoutError:
        return

async def run_server():
    server = await asyncio.start_server(handle_wrap_timed, '0.0.0.0', PORTNUM)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())
