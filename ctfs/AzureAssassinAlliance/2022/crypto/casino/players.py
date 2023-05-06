from qunetsim.components import Host
from qunetsim.objects import Qubit
from qunetsim.objects import Logger
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from casino import WIN_MSG, LOSE_MSG
from secret import flag
import sys
import math
import base64
import random
import os


# Logger.DISABLED = False

AAA_ID = "aaa"
GAMBLER_ID = "gambler"


class CASINO_REFEREE():
    def __init__(self):
        pass

    @staticmethod
    def get_position():
        pos = [0,1,2]
        random.shuffle(pos)
        return pos[:2]
    
    @staticmethod
    def arbitrate(r1, r2, res1, res2):
        if (r1 == 0 and r2 == 2) or (r1 == 2 and r2 == 0):
            if res1 == res2:
                return -2
            else:
                return 1
        else:
            if res1 == res2:
                return 1
            else:
                return -2
    
    @staticmethod
    def encrypt(key, iv, msg):
        def padding(msg):
            msg = msg + bytes([16 - len(msg) % 16] * (16 - len(msg) % 16))
            return msg
        aes = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
        cipher = aes.encrypt(padding(msg))
        return base64.b64encode(cipher)
    
    @staticmethod
    def decrypt(key, cipher, id):
        def unpad(msg):
            return msg[:-msg[-1]]
        cipher = base64.b64decode(cipher)
        if len(cipher) % 16 != 0:
            return base64.b64encode(b"")
        if id != AAA_ID and len(cipher) > 16*2:
            return base64.b64encode(b"sorry, this function is restricted to AAA.")
        iv = cipher[:16]
        aes = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
        msg = unpad(aes.decrypt(cipher[16:]))
        return base64.b64encode(msg)


class Player(object):
    def __init__(self):
        pass

    def get_input(self, prompt="> "):
        print(prompt, end="")
        sys.stdout.flush()
        return input()

    def get_next_classical_message(self, receiver_id, buffer, count):
        buffer.append(self.host.get_next_classical(receiver_id, wait=-1))
        msg = b"ACK"
        while msg == b"ACK" or type(msg) != bytes or (msg != b"FIN" and (msg.split(b':')[0] != (b"%d" % count))):
            if len(buffer) == 0:
                buffer.append(self.host.get_next_classical(receiver_id, wait=-1))
            ele = buffer.pop(0)
            msg = ele.content
        self.host.empty_classical()
        return msg

    def get_next_classical_message_slow(self, receiver_id, buffer, count):
        buffer = buffer + self.host.get_classical(receiver_id, wait=3)
        msg = b"ACK"
        while msg == b"ACK" or type(msg) != bytes or (msg != b"FIN" and (msg.split(b':')[0] != (b"%d" % count))):
            if len(buffer) == 0:
                buffer = buffer + self.host.get_classical(receiver_id, wait=3)
            ele = buffer.pop(0)
            msg = ele.content
        self.host.empty_classical()
        return msg

    def bits_to_bytes(self, bits, bytes_len):
        if type(bits) == list:
            bits = "".join([str(x) for x in bits])
        return long_to_bytes(int(bits, 2)).rjust(bytes_len, b'\x00')


class GAMBLER(Player):
    def __init__(self):
        self.host = Host(GAMBLER_ID)
        self.host.add_connection(AAA_ID)
        self.host.delay = 1
        self.host.start()
        self.wait_time = 1
        self.secret_key = None
        self.secret_iv = None

    def exchange_key(self, host, aaa_id, qubits_n):
        try:
            msg_buff = []
            self.secret_key = self.get_next_classical_message(aaa_id, msg_buff, -1)
            self.secret_key = self.secret_key[3:]

            q_i = 0
            q_iv = []
            while q_i < qubits_n:
                qubit = self.host.get_data_qubit(aaa_id, wait=self.wait_time)
                basis = int(self.get_input("Please give me your basis: "))
                self.host.send_classical(aaa_id, b"%d:%d" % (q_i, basis), await_ack=True)
                msg = self.get_next_classical_message(aaa_id, msg_buff, q_i)
                print("%s receives from %s: %s" % (host.host_id, aaa_id, msg.decode()))
                sys.stdout.flush()
                op, angle = map(int, self.get_input('How to rotate (op, angle): ').split(","))
                self.rotate(qubit, op, angle)
                res = qubit.measure(non_destructive=True)
                print("Your qubit result: %d" % res)
                sys.stdout.flush()
                q_i += 1
                del qubit

            q_iv = base64.b64decode(self.get_input("Please tell me the q_iv (base64): "))
            self.secret_iv = q_iv

        except Exception as e:
            # print(e)
            # sys.stdout.flush()
            self.host.send_classical(aaa_id, b"FIN", await_ack=True)
            

    def rotate(self, qubit, op, angle=0):
        if op == 0:
            qubit.H()
        if op == 1:
            qubit.I()
        if op == 2:
            qubit.K()
        if op == 3:
            qubit.T()
        if op == 4:
            qubit.X()
        if op == 5:
            qubit.Y()
        if op == 6:
            qubit.Z()
        if op == 7:
            qubit.rx(angle / 180 * math.pi)
        if op == 8:
            qubit.ry(angle / 180 * math.pi)
        if op == 9:
            qubit.rz(angle / 180 * math.pi)    
            
    def bet(self, host, aaa_id, bet_times):
        try:
            msg_buff = []
            for round in range(bet_times):
                qubit = self.host.get_epr(aaa_id, wait=5)
                msg = self.get_next_classical_message_slow(aaa_id, msg_buff, round)
                print("%s receives from %s: %s" % (host.host_id, aaa_id, msg.decode()))
                sys.stdout.flush()

                msg = base64.b64decode(msg.split(b":")[1])
                msg = CASINO_REFEREE.decrypt(self.secret_key, 
                                            base64.b64encode(self.secret_iv + msg), 
                                            aaa_id)
                msg = base64.b64decode(msg)
                random.seed(self.secret_key)
                for _ in range(round):
                    random.getrandbits(128)
                rnd_msg = long_to_bytes(random.getrandbits(128)).rjust(16, b'\x00')
                assert msg[:16] == rnd_msg

                for _ in range(40):
                    inp = self.get_input("What dou you want to decrypt: ")
                    if inp == "exit":
                        break
                    dec_msg = CASINO_REFEREE.decrypt(self.secret_key, 
                                            inp, self.host.host_id)
                    print("Your decrypted msg: %s" % dec_msg.decode())
                    sys.stdout.flush()

                op, angle = map(int, self.get_input('How to rotate (op, angle): ').split(","))
                if qubit == None:
                    self.host.send_classical(aaa_id, b"FIN", await_ack=True)
                    return 
                self.rotate(qubit, op, angle)
                res = qubit.measure()
                send_msg = b"%d:%d" % (round, res)
                ack_arrived = self.host.send_classical(aaa_id, send_msg, await_ack=True)
                while not ack_arrived:
                    ack_arrived = self.host.send_classical(aaa_id, send_msg, await_ack=True)

                msg = self.get_next_classical_message_slow(aaa_id, msg_buff, round+bet_times)
                money = int(msg.split(b":")[1])
                print("%s's current money is: %d" % (self.host.host_id, money))
                sys.stdout.flush()
                
                del qubit
            self.host.reset_data_qubits(host_id=GAMBLER_ID)

        except Exception as e:
            # print(e)
            # sys.stdout.flush()
            self.host.send_classical(aaa_id, b"FIN", await_ack=True)


class AAA(Player):
    def __init__(self):
        self.host = Host(AAA_ID)
        self.host.add_connection(GAMBLER_ID)
        self.host.delay = 1
        self.host.start()
        self.wait_time = 1
        self.secret_key = None
        self.secret_iv = None

    def exchange_key(self, host, gambler_id, qubits_n):
        try:
            self.secret_key = os.urandom(16)
            self.secret_iv = os.urandom(16)
            host.send_classical(gambler_id, b"%d:%s" %(-1, self.secret_key), await_ack=True)

            msg_buff = []
            q_iv = []
            self.qubits = [Qubit(self.host, q_id=id) for id in range(qubits_n)]
            self.basis = [random.randint(0,1) for _ in range(qubits_n)]
            self.keybits = [random.randint(0,1) for _ in range(qubits_n)]

            for q_i, qubit in enumerate(self.qubits):
                if self.keybits[q_i] == 1:
                    qubit.X()
                self.host.send_qubit(gambler_id, qubit, await_ack=True)
                message = self.get_next_classical_message(gambler_id, msg_buff, q_i)
                if message == b"FIN":
                    return
                if message == b"%d:%d" % (q_i, self.basis[q_i]):
                    if self.basis[q_i] == 1:
                        qubit.H()
                        res = qubit.measure(non_destructive=True)
                        qubit.H()
                    else:
                        res = qubit.measure(non_destructive=True)
                    q_iv.append(res)
                    msg = b"%d:0" % q_i
                else:
                    msg = b"%d:1" % q_i
                self.host.send_classical(gambler_id, msg, await_ack=True)
                
                del qubit

            q_iv = self.bits_to_bytes(q_iv[:128], 16)
            self.secret_iv = q_iv
            self.host.reset_data_qubits(host_id=AAA_ID)

        except Exception as e:
            pass

        
    def bet(self, host, gambler_id, bet_times):
        def ry0(qubit):
            qubit.ry(1/3 * math.pi)
        def ry1(qubit):
            pass
        def ry2(qubit):
            qubit.ry(-1/3 * math.pi)
        
        rotate_ops = [ry0, ry1, ry2]
        msg_buff = []
        gambler_money = 0

        for round in range(bet_times):
            random.seed(self.secret_key)
            for _ in range(round):
                random.getrandbits(128)
            rnd_msg = long_to_bytes(random.getrandbits(128)).rjust(16, b'\x00')

            _, ack_arrived = self.host.send_epr(gambler_id, await_ack=True)
            while not ack_arrived:
                _, ack_arrived = self.host.send_epr(gambler_id, await_ack=True)
            qubit = self.host.get_epr(gambler_id, wait=1)

            r1, r2 = CASINO_REFEREE.get_position()
            rotate_ops[r1](qubit)
            res1 = qubit.measure()
            cipher = CASINO_REFEREE.encrypt(self.secret_key, 
                                            self.secret_iv, 
                                            b"%s+%d" % (rnd_msg, r2))
            send_msg = b"%d:%s" % (round, cipher)
            ack_arrived = self.host.send_classical(gambler_id, send_msg, await_ack=True)
            while not ack_arrived:
                ack_arrived = self.host.send_classical(gambler_id, send_msg, await_ack=True)
            
            msg = self.get_next_classical_message_slow(gambler_id, msg_buff, round)
            if msg == b'FIN':
                return
            res2 = int(msg[-1:])
            gambler_money += CASINO_REFEREE.arbitrate(r1,r2,res1,res2)
            send_msg = b"%d:%d" % (round+bet_times, gambler_money)
            ack_arrived = self.host.send_classical(gambler_id, send_msg, await_ack=True)
            while not ack_arrived:
                ack_arrived = self.host.send_classical(gambler_id, send_msg, await_ack=True)
            
            del qubit

        if gambler_money >= bet_times // 2:
            print(WIN_MSG + flag)
        else: print(LOSE_MSG) 
        sys.stdout.flush()

