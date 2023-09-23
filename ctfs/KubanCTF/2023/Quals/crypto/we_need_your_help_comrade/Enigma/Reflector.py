

class Reflector:
    def __init__(self,encoding):
        self.forwardWiring = Reflector.decodeWiring(encoding)

    @staticmethod
    def Create(name):
        if name == "B":
            return Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        elif name == "C":
            return Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")
        else:
            return Reflector("ZYXWVUTSRQPONMLKJIHGFEDCBA")

    @staticmethod
    def decodeWiring(encoding):
        wiring = [ord(i) - 65 for i in encoding]
        return wiring

    def forward(self,c):
        return self.forwardWiring[c]