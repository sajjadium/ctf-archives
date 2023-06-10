# https://github.com/radical-semiconductor/woodpecker#processor-description
class CPU:
    def __init__(self):
        self.mem = bytearray(1 << 29)
        self.addr = 0
        self.store = 0
        
    def execute(self, instr):
        match instr.strip().upper():
            case 'INC':  self.addr += 1
            case 'INV':  self.mem[self.addr // 8] ^= 1 << (self.addr % 8)
            case 'LOAD': self.store = self.mem[self.addr // 8] >> (self.addr % 8) & 1
            case 'CDEC': self.addr -= self.store
            case other:  raise ValueError(f'Unknown instruction "{other}"')

if __name__ == '__main__':
    flag = input('Enter flag: ').encode('ascii')
    assert len(flag) == 20, 'Incorrect length'
    
    cpu = CPU()
    cpu.mem[:len(flag)] = flag
    
    for instr in open('woodchecker.wpk').readlines():
        cpu.execute(instr)
        
    print('Correct!' if cpu.store else 'Better luck next time')
