import os
import time


class mersenne_rng(object):
    def __init__(self, seed=5489):
        self.state = [0] * 624
        self.f = 1812433253
        self.m = 397
        self.u = 11
        self.s = 7
        self.b = 0x9D2C5680
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.index = 624
        self.lower_mask = (1 << 31)-1
        self.upper_mask = 1 << 31

        # update state
        self.state[0] = seed
        for i in range(1, 624):
            self.state[i] = self.int_32(self.f * (self.state[i-1] ^ (self.state[i-1] >> 30)) + i)

    def twist(self):
        for i in range(624):
            temp = self.int_32((self.state[i] & self.upper_mask) + (self.state[(i+1) % 624] & self.lower_mask))
            temp_shift = temp >> 1
            if temp % 2 != 0:
                temp_shift = temp_shift ^ 0x9908b0df
            self.state[i] = self.state[(i+self.m) % 624] ^ temp_shift
        self.index = 0

    def get_random_number(self):
        if self.index >= 624:
            self.twist()
        y = self.state[self.index]
        y = y ^ (y >> self.u)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index += 1
        return self.int_32(y)

    def int_32(self, number):
        return int(0xFFFFFFFF & number)


def main():
    rng = mersenne_rng(???)
    for i in range(625):
        number = rng.get_random_number()
        port1 = (number & (2 ** 32 - 2 ** 16)) >> 16
        port2 = number & (2 ** 16 - 1)

        fd = open('/etc/knockd.conf', 'w')
        fd.write('[options]\n')
        fd.write('    UseSyslog\n')
        fd.write('    interface = enp0s3\n')
        fd.write('[openSSH]\n')
        fd.write('    sequence = {0}, {1}\n'.format(port1, port2))
        fd.write('    seq_timeout = 5\n')
        fd.write('    command = /sbin/iptables -A INPUT -s %IP% -p tcp --dport 2222 -j ACCEPT\n')
        fd.write('    tcpflags = syn\n')
        fd.write('[closeSSH]\n')
        fd.write('    sequence = {1}, {0}\n'.format(port1, port2))
        fd.write('    seq_timeout = 5\n')
        fd.write('    command = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 2222 -j ACCEPT\n')
        fd.write('    tcpflags = syn\n')
        fd.close()
        os.system('systemctl restart knockd')
        assert 'Active: active (running)' in os.popen('systemctl status knockd').read()

        time.sleep(5)

if __name__ == "__main__":
    main()