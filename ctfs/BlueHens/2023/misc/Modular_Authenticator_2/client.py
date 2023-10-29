import random
import asyncio
import json
import itertools
#For local testing
HOST = "localhost"
PORT = 3000

ROUNDS = 128
RANDOM = random.SystemRandom()

async def main():
    coro = asyncio.open_connection(HOST,PORT)
    with open("public_key.json","r") as f:
        public_key = json.loads(f.read())
    with open("private_key.json","r") as f:
        private_key = json.loads(f.read())
    N = public_key["N"]
    secret = private_key["s"]
    e = public_key["e"]
    reader, writer = await coro
    try:
        randoms =  tuple([RANDOM.randint(2,1<<32) for _ in range(ROUNDS)])
        writer.write(json.dumps([pow(r,e,N) for r in randoms]).encode('utf-8') + b'\r\n')
        await writer.drain()

        challenges = json.loads((await reader.readline()).decode('utf-8'))

        if not isinstance(challenges,list):
            raise ValueError(f"The server responded with something other than a list of challenges: {challenges}")

        responses = []
        for challenge, i in zip(challenges,itertools.count()):
            if challenge == 'r':
                responses.append(randoms[i])
            elif challenge == 'rs':
                responses.append((randoms[i]*secret) % N)
            else:
                raise ValueError(f"The server requested unknown challenge {challenge}")
        
        writer.write(json.dumps(responses).encode('utf-8') + b'\r\n')
        await writer.drain()

        print(await reader.read())
    finally:
        #Be a good citizen and close the connection.
        writer.close()
        await writer.wait_closed()    

if __name__ == "__main__":
    asyncio.run(main())

