import sys
import random
from secret import get_next_seed, store_leaked_data, store_exec_status, get_flag, get_scheduled_cmds


RESEED_AFTER = 1000000


def xor_bytes(a, b):
    return bytes(map(lambda x: x[0] ^ x[1], zip(a,b)))


class Handler:
    def __init__(self) -> None:
        self.handling = True
        self.reseed()

    def randbytes(self, n):
        self.rng_used += n
        b = self.rng.randbytes(n)
        return b

    def reseed(self):
        seed_bytes = get_next_seed()
        if len(seed_bytes) != 12:
            self.send_raw(b'ERROR: No more pre-shared seeds')
            exit()
        self.rng = random.Random()
        self.rng.seed(seed_bytes)
        self.rng_used = 0

    def recv_msg(self, length, default=None):
        received = b''
        while len(received) < length:
            new_input = sys.stdin.buffer.read(length - len(received))
            received += new_input.strip().replace(b' ', b'')

        if len(received) == 0 and default:
            return default
        try:
            return received
        except:
            return b''

    def send_raw(self, msg):
        sys.stdout.buffer.write(msg)
        sys.stdout.buffer.flush()

    def start_encrypted(self):
        return

    def end_encrypted(self):
        if self.rng_used > RESEED_AFTER:
            self.reseed()

    def recv_encrypted(self):
        msg = b''
        try:
            len_otp = self.randbytes(1)
            len_encrypted = self.recv_msg(1, default=len_otp)
            length = int.from_bytes(xor_bytes(len_otp, len_encrypted), 'little')

            if length == 0:
                self.end_encrypted()
                return msg

            otp = self.randbytes(length)
            received = self.recv_msg(length)
            msg = xor_bytes(otp, received)
        except:
            self.handling = False
        finally:
            self.end_encrypted()
        return msg

    def send_encrypted(self, msg):
        try:
            assert len(msg) < 256
            otp = self.randbytes(1) + self.randbytes(len(msg)) # split for receiver
            self.send_raw(xor_bytes(otp, len(msg).to_bytes(1, 'little') + msg))
        except:
            self.handling = False
            self.send_raw(b'ERR: %d' % (len(msg)))
        finally:
            self.end_encrypted()

    def process_commands(self, cmd_msg: bytes):
        response = b''

        while len(cmd_msg) > 0:
            cursor = 4
            current_cmd = cmd_msg[:cursor]
            if current_cmd == b'LEAK':
                length = cmd_msg[cursor]
                cursor += 1
                store_leaked_data(cmd_msg[cursor:cursor+length])
                cursor += length
            elif current_cmd == b'EXEC':
                store_exec_status(cmd_msg[cursor])
                cursor += 1
            elif current_cmd == b'FLAG':
                response += get_flag()
            elif current_cmd == b'EXIT':
                self.handling = False
            else:
                response += b'ERROR'
            cmd_msg = cmd_msg[cursor:]
        response = response[:255] # truncate response to max length

        response += get_scheduled_cmds(255 - len(response))
        return response

    def handle(self):
        self.send_raw(b'RDY')
        while self.handling:
            try:
                cmd_msg = self.recv_encrypted()
                if not self.handling: return

                response = self.process_commands(cmd_msg)
                self.send_encrypted(response)
                if not self.handling: return
            except:
                return


def main():
    srv = Handler()
    srv.handle()

if __name__ == '__main__':
    main()
