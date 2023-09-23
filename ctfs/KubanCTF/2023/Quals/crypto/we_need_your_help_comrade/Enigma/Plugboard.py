

class Plugboard:

    def __init__(self, connections):
        self.wiring = Plugboard.decodePlugboard(connections)

    def forward(self,c):
        return self.wiring[c]

    @staticmethod
    def identityPlugboard():
        return list(range(26))

    @staticmethod
    def decodePlugboard(plugboard=None):

        mapping = Plugboard.identityPlugboard()
        if plugboard == None or plugboard == "":
            return mapping

        pairs = plugboard.split()

        for p in pairs:
            c1 = ord(p[0])-65
            c2 = ord(p[1])-65
            mapping[c1]=c2
            mapping[c2]=c1

        return mapping





