import base64
from dataclasses import dataclass
from enum import Enum
from Crypto.Cipher import AES
import random
from telnetlib import SE
import libscrc


def bytes_xor_16(bytes1, bytes2):
    v1 = int.from_bytes(bytes1, 'big')
    v2 = int.from_bytes(bytes2, 'big')
    v3 = v1 ^ v2
    return (v3).to_bytes(16, 'big')


def secure_encrypt(key, plain):
    aes = AES.new(key=key, mode=AES.MODE_ECB)
    return aes.encrypt(plain)


def secure_encrypt_packet(key, plain, nonce):
    aes = AES.new(key=key, mode=AES.MODE_CCM, nonce=nonce)
    return aes.encrypt(plain)


def secure_decrypt_packet(key, plain, nonce):
    aes = AES.new(key=key, mode=AES.MODE_CCM, nonce=nonce)
    return aes.decrypt(plain)


def secure_confirm(key, r, p1, p2):
    return secure_encrypt(key, bytes_xor_16(secure_encrypt(key, bytes_xor_16(r, p1)), p2))


class PktOpcode(Enum):
    HELLO = 1
    SC_REQ = 2
    SC_RSP = 3
    M_CONFIRM = 4
    S_CONFIRM = 5
    M_RANDOM = 6
    S_RANDOM = 7
    DATA = 8


class connection_handle:
    def __init__(self, type) -> None:
        self.type = type

    def send(self, data) -> None:
        pass

    def recv(self, length) -> bytes:
        return b""


def dump_packet(prefix: str, pkt: bytes, logfile: str):
    log_content = ""
    print(prefix + "\t", end="")
    log_content += prefix + "\t"
    for i in range(len(pkt)):
        d = pkt[i]
        print(hex(d)[2:].rjust(2, '0'), end="")
        log_content += hex(d)[2:].rjust(2, '0')
        if (i + 1) % 16 == 0 and i + 1 != len(pkt):
            print("\n\t", end="")
            log_content += "\n\t"
        else:
            print(" ", end="")
            log_content += " "
    print("")
    log_content += "\n"
    with open(logfile, "a") as f:
        f.write(log_content)


class connection_handle_socket(connection_handle):
    def __init__(self, s, role, dump) -> None:
        super().__init__("socket")
        self.socket = s
        self.role = role
        self.dump = dump
        self.dumpfile = self.role + ".txt"

    def send(self, data) -> None:
        self.socket.send(data)
        if self.dump:
            dump_packet(">", data, self.dumpfile)

    def recv(self, length) -> bytes:
        data = self.socket.recv(length)
        if self.dump:
            dump_packet("<", data, self.dumpfile)
        return data


class connection_handle_request(connection_handle):
    def __init__(self, request, role, dump) -> None:
        super().__init__("request")
        self.request = request
        self.role = role
        self.dump = dump
        self.dumpfile = self.role + ".txt"

    def send(self, data) -> None:
        self.request.sendall(data)
        if self.dump:
            dump_packet(">", data, self.dumpfile)

    def recv(self, length) -> bytes:
        data = self.request.recv(length)
        if self.dump:
            dump_packet("<", data, self.dumpfile)
        return data


class connection_state:
    def __init__(self, role, encrypt) -> None:
        self.role = role
        self.local_counter = 0
        self.remote_counter = 0
        self.encrypt = encrypt
        self.initCRC = b""

    def inc_local_counter(self):
        self.local_counter += 1

    def inc_remote_counter(self):
        self.remote_counter += 1

    def calc_crc(self, pdu):
        initvalue = int.from_bytes(self.initCRC, "little")
        crc = libscrc.hacker24(data=pdu, poly=0x00065B, init=initvalue,
                               xorout=0x00000000, refin=True, refout=True)
        return crc.to_bytes(3, "little")

    def prepare_hello_packet(self):
        hello_packet = b""
        hello_packet += int(self.encrypt << 7 |
                            (PktOpcode.HELLO.value & 0x3f)).to_bytes(1, "little")
        hello_packet += int(3).to_bytes(1, "little")
        if not self.initCRC:
            self.initCRC = random.randbytes(3)
        hello_packet += self.initCRC
        hello_packet += self.calc_crc(hello_packet)
        # no encryption for hello
        return hello_packet

    def decrypt_data_packet(self, data):
        if self.encrypt:
            return secure_decrypt_packet(
                self.sessionkey, data, (self.remote_counter).to_bytes(
                    13, "little")
            )
        else:
            return data

    def prepare_data_packet(self, data, moredata):
        data_packet = b""
        data_packet += int(self.encrypt << 7 | moredata << 6 |
                           (PktOpcode.DATA.value & 0x3f)).to_bytes(1, "little")
        data_packet += len(data).to_bytes(1, "little")
        if self.encrypt:
            data_packet += secure_encrypt_packet(
                self.sessionkey, data, (self.local_counter).to_bytes(
                    13, "little")
            )
        else:
            data_packet += data
        data_packet += self.calc_crc(data_packet)
        return data_packet

    def prepare_sc_request_packet(self):
        sc_request_packet = b""
        sc_request_packet += int(self.encrypt << 7 |
                                 (PktOpcode.SC_REQ.value & 0x3f)).to_bytes(1, "little")
        sc_request_packet += int(16).to_bytes(1, "little")
        IV = random.randbytes(8)
        Secret = random.randbytes(8)
        self.IVm = IV
        self.Secretm = Secret
        sc_request_packet += IV
        sc_request_packet += Secret
        sc_request_packet += self.calc_crc(sc_request_packet)
        return sc_request_packet

    def prepare_sc_respond_packet(self):
        sc_request_packet = b""
        sc_request_packet += int(self.encrypt << 7 |
                                 (PktOpcode.SC_RSP.value & 0x3f)).to_bytes(1, "little")
        sc_request_packet += int(16).to_bytes(1, "little")
        IV = random.randbytes(8)
        Secret = random.randbytes(8)
        self.IVs = IV
        self.Secrets = Secret
        sc_request_packet += IV
        sc_request_packet += Secret
        sc_request_packet += self.calc_crc(sc_request_packet)
        return sc_request_packet

    def prepare_master_confirm_packet(self):
        master_confirm_packet = b""
        master_confirm_packet += int(self.encrypt << 7 |
                                     (PktOpcode.M_CONFIRM.value & 0x3f)).to_bytes(1, "little")
        master_confirm_packet += int(16).to_bytes(1, "little")
        master_random = random.randbytes(16)
        master_confirm = secure_confirm(
            self.numeric_key_bytes, master_random, b"\x00" * 16, b"\xff" * 16)
        self.MRandom = master_random
        self.MConfirm = master_confirm
        master_confirm_packet += master_confirm
        master_confirm_packet += self.calc_crc(master_confirm_packet)
        return master_confirm_packet

    def prepare_slave_confirm_packet(self):
        slave_confirm_packet = b""
        slave_confirm_packet += int(self.encrypt << 7 |
                                    (PktOpcode.S_CONFIRM.value & 0x3f)).to_bytes(1, "little")
        slave_confirm_packet += int(16).to_bytes(1, "little")
        slave_random = random.randbytes(16)
        slave_confirm = secure_confirm(
            self.numeric_key_bytes, slave_random, b"\x00" * 16, b"\xff" * 16)
        self.SRandom = slave_random
        self.SConfirm = slave_confirm
        slave_confirm_packet += slave_confirm
        slave_confirm_packet += self.calc_crc(slave_confirm_packet)
        return slave_confirm_packet

    def prepare_master_random_packet(self):
        master_random_packet = b""
        master_random_packet += int(self.encrypt << 7 |
                                    (PktOpcode.M_RANDOM.value & 0x3f)).to_bytes(1, "little")
        master_random_packet += int(16).to_bytes(1, "little")
        master_random_packet += self.MRandom
        master_random_packet += self.calc_crc(master_random_packet)
        return master_random_packet

    def prepare_slave_random_packet(self):
        slave_random_packet = b""
        slave_random_packet += int(self.encrypt << 7 |
                                   (PktOpcode.S_RANDOM.value & 0x3f)).to_bytes(1, "little")
        slave_random_packet += int(16).to_bytes(1, "little")
        slave_random_packet += self.SRandom
        slave_random_packet += self.calc_crc(slave_random_packet)
        return slave_random_packet

    def check_master_confirm(self, recvMrandom):
        should_Mconfirm = secure_confirm(
            self.numeric_key_bytes, recvMrandom, b"\x00" * 16, b"\xff" * 16)
        if should_Mconfirm == self.MConfirm:
            self.MRandom = recvMrandom
            return True
        else:
            return False

    def check_slave_confirm(self, recvSrandom):
        should_Sconfirm = secure_confirm(
            self.numeric_key_bytes, recvSrandom, b"\x00" * 16, b"\xff" * 16)
        if should_Sconfirm == self.SConfirm:
            self.SRandom = recvSrandom
            return True
        else:
            return False

    def setup_session(self):
        self.storekey = secure_encrypt(
            self.numeric_key_bytes, self.MRandom[:8] + self.SRandom[8:])
        self.sessionkey = secure_encrypt(
            self.storekey, self.Secretm + self.Secrets)


def showChoice():
    print("================ CHOICE ================")
    print("[0] Receive a message")
    print("[1] Send a message")
    print("[2] Leave")
    print("-----------------======-----------------")


def goodBye():
    print("-----------------======-----------------")
    print("See you next time\n")


def recieve_message(state: connection_state, handler: connection_handle):
    entire_data_payload = b""
    while True:
        dataheader = handler.recv(2)
        more_data = (dataheader[0] >> 6) & 0b1
        opcode = dataheader[0] & 0x3f
        if opcode != PktOpcode.DATA.value:
            print("Weird not data packet receieved")
            return
        datalength = dataheader[1]
        payload = handler.recv(datalength)
        crc = handler.recv(3)
        should_crc = state.calc_crc(dataheader + payload)
        payload = state.decrypt_data_packet(payload)
        state.inc_remote_counter()
        if crc != should_crc:
            print("CRC check failed in receive message")
            return
        entire_data_payload += payload
        if not more_data:
            break
    decoded_data = base64.b64decode(entire_data_payload).decode()
    print("Your recv : " + decoded_data)


def send_message(state: connection_state, handler: connection_handle):
    data = input("Your data > ").strip().encode()
    encoded_data = base64.b64encode(data)
    # split into segements
    encoded_data_len = len(encoded_data)
    for start in range(0, encoded_data_len, 255):
        if start + 255 > encoded_data_len:
            end = encoded_data_len
            moreData = False
        else:
            end = start + 255
            moreData = True
        data_segment = encoded_data[start: end]
        data_packet = state.prepare_data_packet(data_segment, moreData)
        handler.send(data_packet)
        state.inc_local_counter()


def master_hello_procedure(handler: connection_handle, state: connection_state):
    handler.send(state.prepare_hello_packet())
    state.inc_local_counter()
    hello_pkt = handler.recv(2 + 255 + 3)
    state.inc_remote_counter()
    if hello_pkt[0] & 0x3f != PktOpcode.HELLO.value:
        return False
    encrypt_or_not = (hello_pkt[0] >> 7) & 0b1
    if not encrypt_or_not:
        return True
    handler.send(state.prepare_sc_request_packet())
    state.inc_local_counter()
    numeric_key = int(input("Shared numeric key > "))
    numeric_key = numeric_key % 0x1000000
    state.numeric_key = numeric_key
    state.numeric_key_bytes = (numeric_key).to_bytes(16, "little")
    sc_respond_pkt = handler.recv(2 + 255 + 3)
    state.inc_remote_counter()
    if sc_respond_pkt[0] & 0x3f != int(PktOpcode.SC_RSP.value):
        return False
    recvIVs = sc_respond_pkt[2: 10]
    recvSecrets = sc_respond_pkt[10: 18]
    crc = sc_respond_pkt[18: 18 + 3]
    should_crc = state.calc_crc(sc_respond_pkt[:18])
    if crc != should_crc:
        print("CRC check failed in hello procedure")
        return False
    state.IVs = recvIVs
    state.Secrets = recvSecrets
    handler.send(state.prepare_master_confirm_packet())
    state.inc_local_counter()
    sconfirm_pkt = handler.recv(2 + 255 + 3)
    state.inc_remote_counter()
    if sconfirm_pkt[0] & 0x3f != int(PktOpcode.S_CONFIRM.value):
        return False
    recvSConfirm = sconfirm_pkt[2: 18]
    crc = sconfirm_pkt[18: 18 + 3]
    should_crc = state.calc_crc(sconfirm_pkt[:18])
    if crc != should_crc:
        print("CRC check failed in hello procedure")
        return False
    state.SConfirm = recvSConfirm
    handler.send(state.prepare_master_random_packet())
    state.inc_local_counter()
    srandom_pkt = handler.recv(2 + 255 + 3)
    state.inc_remote_counter()
    if srandom_pkt[0] & 0x3f != int(PktOpcode.S_RANDOM.value):
        return False
    recvSRandom = srandom_pkt[2: 18]
    crc = srandom_pkt[18: 18 + 3]
    should_crc = state.calc_crc(srandom_pkt[:18])
    if crc != should_crc:
        print("CRC check failed in hello procedure")
        return False
    if not state.check_slave_confirm(recvSRandom):
        return False
    state.setup_session()
    return True


def slave_hello_procedure(handler: connection_handle, state: connection_state):
    hello_pkt = handler.recv(2 + 255 + 3)
    state.inc_remote_counter()
    if hello_pkt[0] & 0x3f != int(PktOpcode.HELLO.value):
        return False
    encrypt_or_not = (hello_pkt[0] >> 7) & 0b1
    state.encrypt = encrypt_or_not
    hello_pkt_len = hello_pkt[1]
    hello_pkt_payload = hello_pkt[2: 2 + hello_pkt_len]
    state.initCRC = hello_pkt_payload
    handler.send(state.prepare_hello_packet())
    state.inc_local_counter()
    if not encrypt_or_not:
        return True
    else:
        sc_request_pkt = handler.recv(2 + 255 + 3)
        state.inc_remote_counter()
        if sc_request_pkt[0] & 0x3f != int(PktOpcode.SC_REQ.value):
            return False
        recvIVm = sc_request_pkt[2: 10]
        recvSecretm = sc_request_pkt[10: 18]
        crc = sc_request_pkt[18: 18 + 3]
        should_crc = state.calc_crc(sc_request_pkt[:18])
        if crc != should_crc:
            print("CRC check failed in hello procedure")
            return False
        state.IVm = recvIVm
        state.Secretm = recvSecretm
        handler.send(state.prepare_sc_respond_packet())
        state.inc_local_counter()
        numeric_key = int(input("Shared numeric key > "))
        numeric_key = numeric_key % 0x1000000
        state.numeric_key = numeric_key
        state.numeric_key_bytes = (numeric_key).to_bytes(16, "little")
        mconfirm_packet = handler.recv(2 + 255 + 3)
        state.inc_remote_counter()
        if mconfirm_packet[0] & 0x3f != int(PktOpcode.M_CONFIRM.value):
            return False
        recvMConfirm = mconfirm_packet[2: 18]
        crc = mconfirm_packet[18: 18 + 3]
        should_crc = state.calc_crc(mconfirm_packet[:18])
        if crc != should_crc:
            print("CRC check failed in hello procedure")
            return False
        state.MConfirm = recvMConfirm
        handler.send(state.prepare_slave_confirm_packet())
        state.inc_local_counter()
        mrandom_packet = handler.recv(2 + 255 + 3)
        state.inc_remote_counter()
        if mrandom_packet[0] & 0x3f != int(PktOpcode.M_RANDOM.value):
            return False
        recvMRandom = mrandom_packet[2: 18]
        crc = mrandom_packet[18: 18 + 3]
        should_crc = state.calc_crc(mrandom_packet[:18])
        if crc != should_crc:
            print("CRC check failed in hello procedure")
            return False
        if not state.check_master_confirm(recvMRandom):
            return False
        handler.send(state.prepare_slave_random_packet())
        state.inc_local_counter()
        state.setup_session()
        return True


def connection_engine(handler: connection_handle, role: str, encrypt: bool):
    state = connection_state(role, encrypt)
    if role == "master":
        if not master_hello_procedure(handler, state):
            print("hello fail")
            exit(1)
    if role == "slave":
        if not slave_hello_procedure(handler, state):
            print("hello fail")
            exit(1)

    while True:
        try:
            showChoice()
            choice = int(input("Your choice > "))
            if choice < 0 or choice > 2:
                raise ValueError
            if choice == 0:
                recieve_message(state, handler)
            elif choice == 1:
                send_message(state, handler)
            elif choice == 2:
                goodBye()
                return

        except ValueError as err:
            print("Bad Input T.T")
            continue
        except KeyboardInterrupt as err:
            goodBye()
            return
        # except Exception as err:
        #     print("Bad thing happens")
        #     print(err)
        #     return
