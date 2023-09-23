class Rotor:
    def __init__(self, name,encoding, rotorPos, notchPosition, ringSetting):
        self.name = name
        self.forwardWiring = Rotor.decodeWiring(encoding)
        self.backwardWiring = Rotor.inverseWiring(self.forwardWiring)
        self.rotorPosition = rotorPos
        self.notchPosition = notchPosition
        self.ringSetting = ringSetting

    @staticmethod
    def Create(name, rotorPosition, ringSetting):

        if name == "I":
            return Rotor("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", rotorPosition, 16, ringSetting)
        elif name == "II":
            return Rotor("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", rotorPosition, 4, ringSetting)
        elif name == "III":
            return  Rotor("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", rotorPosition, 21, ringSetting)
        elif name == "IV":
            return Rotor("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", rotorPosition, 9, ringSetting)
        elif name == "V":
            return Rotor("V", "VZBRGITYUPSDNHLXAWMJQOFECK", rotorPosition, 25, ringSetting)
        else:
            return Rotor("{1}", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", rotorPosition, 0, ringSetting)


    def getName(self):
        return self.name

    def getPosition(self):
        return self.name

    @staticmethod
    def decodeWiring(encoding):
        wiring = [ord(i)-65 for i in encoding]
        return wiring

    @staticmethod
    def inverseWiring(wiring):
        inverse = [0]*len(wiring)
        for i in range(len(wiring)):
            inverse[wiring[i]]=i
        return inverse

    @staticmethod
    def cipher(k,pos,ring,mapping):
        shift = pos - ring
        return (mapping[(k+shift+26)%26] - shift + 26) % 26

    def forward(self,c):
        return Rotor.cipher(c, self.rotorPosition, self.ringSetting, self.forwardWiring)

    def backward(self, c):
        return Rotor.cipher(c, self.rotorPosition, self.ringSetting, self.backwardWiring)

    def isAtNotch(self):
        return self.notchPosition == self.rotorPosition

    def turnover(self):
        self.rotorPosition = (self.rotorPosition+1) % 26

