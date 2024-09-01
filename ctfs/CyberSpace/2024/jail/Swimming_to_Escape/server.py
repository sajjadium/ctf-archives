from fish import Interpreter, StopExecution

FLAG = open('flag.txt').read().strip()
whitelist = r' +-*,%><^v~:&!?=()01\'/|_#l$@r{};"'

if __name__ == '__main__':

    while True:
        print('Please input your code:')
        code = input()
        assert len(code) <= 26
        assert all([c in whitelist for c in code])

        code = code + 'n;;;\n' + ';' * 30
        interpreter = Interpreter(code)
        interpreter._stack = [ord(c) for c in FLAG]

        count = 0

        while True:
            try:
                instr = interpreter.move()
                count += 1
            except:
                break

            if count >= 5000:
                print('Too many moves!!')
                break
        print()
