from totally_normal_integers import Int, sum
from string import digits
from secret import FLAG

zero = Int(0)

class Calculator:
    def __init__(self):
        self.ind = 0
        self.vals = [zero]*6
        self.t = [Int(tval) for tval in [1550, 1548, 8073, 5413, 1411]]
    
    def calc(self, a, op, b):
        result = eval(f"Int({a}) {op} Int({b})")
        if op == "+":
            try:
                self.vals[self.ind//2] = result
            except:
                self.vals = [zero]*6
        self.check()
        self.ind += 1
        return result
    
    def check(self):
        if all([t == sum(self.vals[i:i+2]) for i, t in enumerate(self.t)]) and sum(self.vals) == Int(78606):
            print(f"Backdoor activated!!! Spilling secrets: {FLAG}")
            exit()
    
    
calculator = Calculator()
WELCOME = "Welcome to the online calculator service. Enjoy your free trial while it's still in beta!"
INPUT = "What do you want to calculate(enter in format '<num 1> <operator> <num 2>', e.g. '1 * 2'): "

print(WELCOME)
while True:
    inp = input(INPUT).split()
    assert len(inp) == 3, "One operation at a time"
    assert inp[1] in ["+", "-", "*", "/", "//", "%", "**"], "It's still in beta, sorry haven't implemented everything yet"
    assert inp[0].removeprefix("-").isdigit() and inp[2].removeprefix("-").isdigit(), "Only integers please :)"
    
    try:
        print(calculator.calc(*inp))
    except ValueError:
        break
