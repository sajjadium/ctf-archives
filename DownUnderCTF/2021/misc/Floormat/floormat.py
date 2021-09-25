import abc
import string
import random

FLAG = 'REDACTED'

class Design(abc.ABC):
    def __init__(self, design=[]):
        self._design = design 
        self._i = -1
    
    def items(self):
        return "".join(self._design)
    
    def get_next(self):
        self._i = (self._i + 1) % len(self._design)
        return self._design[self._i]

    
    def __str__(self):
        return self.get_next()

class Rotate(Design):
    def __init__(self):
        super().__init__(design=["-", "/", "|", "\\"])

class Circles(Design):
    def __init__(self):
        super().__init__(design=[".", "o", "0", "O", "0", "o"])

class Random(Design):
    def __init__(self):
        super().__init__(design=string.ascii_lowercase)
    
    def get_next(self):
        return random.choice(self._design)

designs = {
    'Flutter': Rotate(),
    'Fragment':  Circles(),
    'Festival': Random()
}

templates = {
    'Fundamental': '\n'.join([
        "+" + "-"*20 + "+",
        "|" + "{f}"*20 + "|",
        "|" + "{f}"*20 + "|",
        "|" + "{f}"*20 + "|",
        "|" + "{f}"*20 + "|",
        "|" + "{f}"*20 + "|",
        "+" + "-"*20 + "+"
    ]),
    'Flabbergasting': '\n'.join([
        "+-----+-----+-----+-----+",
        "|"+"{f}"*5+"|"+"{f}"*5+"|"+"{f}"*5+"|"+"{f}"*5+"|",
        "|"+"{f}"*5+"|"+"{f}"*5+"|"+"{f}"*5+"|"+"{f}"*5+"|",
        "+-----+-----+-----+-----+",
        "|"+"{f}"*5+"|"+"{f}"*5+"|"+"{f}"*5+"|"+"{f}"*5+"|",
        "|"+"{f}"*5+"|"+"{f}"*5+"|"+"{f}"*5+"|"+"{f}"*5+"|",
        "+-----+-----+-----+-----+"
    ])
}

def banner():
    print("Welcome to the Fabulous Floormat Factory (FFF)!")
    print("In our fabled facility we fabricate fantasticly fashionable floormats for free!")
    print("Furthermore, for the foreseeable future FFF will fork-out flags to fastidious followers.")
    print('')

def get_happy_f():
        return random.choice(["Fun", "Foxy", "Fetching"])

def get_sad_f():
    return random.choice(["Fail", "Foolish", "Foul"])

def custom_template():
    print('Fascinating! Forgoing the featured furniture and finding the flexible function.')
    print('Fill in your floormat format. {f} flags fancy fabric, F finalizes')
    print('For example, Fundamental:')
    print(templates['Fundamental'])
    print('F')
    print('')

    print('Format:')
    buffer = ""
    while (l := input()) != 'F':
        buffer += l

    return buffer


def get_template():
    print("FFF features a few foundational floormat forms:")
    for nm, floormat in templates.items():
        print('[{}]:'.format(nm))
        print(floormat.format(f=' '))
        print('')
    
    selection = input("Fill in your favorite: ")
    try:
        template = templates[selection.title()]
    except KeyError:
        print('')
        template = custom_template()
    
    print(get_happy_f() + "!")
    print('')

    return template

def get_pattern():
    print('Finally, find the fairest felt furnishings!')
    for nm, pattern in designs.items():
        print('[{}]:'.format(nm))
        print(pattern.items())
        print('')
    
    while True:
        selection = input('Favorite: ')
        try:
            return designs[selection.title()]
        except KeyError:
            print(get_sad_f() + '!')
            pass

if __name__ == '__main__':
    import sys
    sys.tracebacklimit = 0
    sys.excepthook = lambda t,e,b: print('\n\n' + ('Farewell!' if t is KeyboardInterrupt or t is EOFError else 'F***!'))

    banner()

    template = get_template()
    pattern = get_pattern()

    print('')
    print('Formulating...')
    floormat = template.format(f=pattern)

    print('Finished! Felicitations on your Floormat!')
    print('')
    print(floormat)
    print('')

