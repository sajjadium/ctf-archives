from unicorn import Uc, UcError, UC_ARCH_X86, UC_ARCH_ARM64, UC_ARCH_RISCV, UC_MODE_64, UC_MODE_ARM, UC_MODE_RISCV64, UC_PROT_READ, UC_PROT_EXEC, UC_SECOND_SCALE, UC_HOOK_BLOCK
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RIP
from unicorn.arm64_const import UC_ARM64_REG_X0, UC_ARM64_REG_PC
from unicorn.riscv_const import UC_RISCV_REG_X1, UC_RISCV_REG_PC

import sys, json, time, hashlib, signal, os, random, dbm
import fastcrc
from filelock import FileLock
from datetime import datetime


def _check_team_token(token):
    try:
        with dbm.open("data/teams", "r") as db:
            return db.get(hashlib.md5(token.encode("utf-8")).hexdigest(), None)
    except dbm.error:
        return b"<missing team name>"

def hmac64(key, msg):  # RFC 2104
    opadk = (int.from_bytes(b"\x5c" * 8)^key).to_bytes(8)
    ipadk = (int.from_bytes(b"\x36" * 8)^key).to_bytes(8)
    return fastcrc.crc64.we(opadk + fastcrc.crc64.we(ipadk + msg).to_bytes(8))

bbcounter = 0
def hook_block(uc, address, size, user_data):
    global bbcounter
    bbcounter += 1

def run(mu, CODE, MAP_ADDR, REG, PC, INPUT):
    try:
        mu.mem_map(MAP_ADDR, 4096+(len(CODE)//4096)*4096, UC_PROT_READ|UC_PROT_EXEC)
        mu.mem_write(MAP_ADDR, CODE)
        mu.reg_write(REG, INPUT)
        mu.hook_add(UC_HOOK_BLOCK, hook_block)
        # RUN CODE
        mu.emu_start(MAP_ADDR, MAP_ADDR + len(CODE), timeout=UC_SECOND_SCALE*60, count=6000000)
        result = mu.reg_read(REG)
    except UcError as e:
        print("ERROR: %s at 0x%x" % (e, mu.reg_read(PC)))
        result = 0

    return result

def try_login(token):
    os.makedirs('/tmp/FF24', mode=0o700, exist_ok=True)
    conn_interval = 5
    with FileLock(os.path.join('/tmp/FF24', hashlib.sha256(token.encode()).hexdigest()+'.lock'), timeout=1):
        fd = os.open(os.path.join('/tmp/FF24', hashlib.sha256(token.encode()).hexdigest()), os.O_CREAT | os.O_RDWR)
        with os.fdopen(fd, "r+") as f:
            data = f.read()
            now = int(time.time())
            if data:
                last_login, balance = data.split()
                last_login = int(last_login)
                balance = int(balance)
                last_login_str = (
                    datetime.fromtimestamp(last_login).isoformat().replace("T", " ")
                )
                balance += now - last_login
                if balance > conn_interval * 3:
                    balance = conn_interval * 3
            else:
                balance = conn_interval * 3
            if conn_interval > balance:
                print(
                    f"Player connection rate limit exceeded, please try again after {conn_interval-balance} seconds. "
                )
                return False
            balance -= conn_interval
            f.seek(0)
            f.truncate()
            f.write(str(now) + " " + str(balance))
        return True

signal.alarm(3)
token = input("Please input your team token: ")
team_name = _check_team_token(token)
if team_name is None:
    print("No such team!")
    exit(1)
team_name = team_name.decode("utf-8")
if not try_login(token):
    exit(-1)
signal.alarm(0)

print("Welcome to FF24. Think fast, code faster")
print("Plz choose options:\n\t1. View leaderboard\n\t2. Run program")
choice = int(input("Your choice [1/2]: "))
if choice == 1:
    with FileLock("/tmp/FF24/scores.json.lock", timeout=1):
        leaderb = json.load(open('data/scores.json','r'))
    print('------------LEADERBOARD------------')
    temp = sorted(leaderb.values())
    for t,s in sorted(leaderb.items(), key=lambda x:x[1]):
        print("{0:2} | {1:15} | {2}".format(temp.index(s)+1, t, s))
    print('-----------------------------------')
elif choice == 2:
    code = bytes.fromhex(input("Give me shellcode in HEX format: "))
    code_map = int(input("Give me code mapping address: "))
    success = 0
    random_input = random.randint(0, 2**64-1)
    expect = hmac64(random_input, code+random_input.to_bytes(8))
    result = run(Uc(UC_ARCH_ARM64, UC_MODE_ARM), code, code_map, UC_ARM64_REG_X0, UC_ARM64_REG_PC, random_input)
    if expect == result:
        print("ARM64: SUCCESS")
        success += 1
    else:
        print(f"ARM64: {random_input:016x}, {expect:016x}, {result:016x}")
    random_input = random.randint(0, 2**64-1)
    expect = hmac64(random_input, code+random_input.to_bytes(8))
    result = run(Uc(UC_ARCH_RISCV, UC_MODE_RISCV64), code, code_map, UC_RISCV_REG_X1, UC_RISCV_REG_PC, random_input)
    if expect == result:
        print("RV64: SUCCESS")
        success += 1
    else:
        print(f"RV64: {random_input:016x}, {expect:016x}, {result:016x}")
    if success == 2:
        random_input = random.randint(0, 2**64-1)
        expect = hmac64(random_input, code+random_input.to_bytes(8))
        result = run(Uc(UC_ARCH_X86, UC_MODE_64), code, code_map, UC_X86_REG_RAX, UC_X86_REG_RIP, random_input)
        if expect == result:
            print("x86-64: SUCCESS")
            success += 1
        else:
            print(f"x86-64: {random_input:016x}, {expect:016x}, {result:016x}")

    if success:
        score = len(code) * 10000**(3-success) + bbcounter
        print("Your score:", score)
        if score <= 283:
            with open("/flag", "rt") as _f:
                print(_f.read(), flush=True)
        with FileLock("/tmp/FF24/scores.json.lock", timeout=1):
            leaderb = json.load(open('data/scores.json','r'))
            if team_name not in leaderb or score < leaderb[team_name]:
                leaderb[team_name] = score
                json.dump(leaderb, open('data/scores.json','w'))
