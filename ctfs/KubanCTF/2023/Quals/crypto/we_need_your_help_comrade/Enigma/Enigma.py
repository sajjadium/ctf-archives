from Enigma_Project.Enigma.Reflector import Reflector
from Enigma_Project.Enigma.Rotor import Rotor
from Enigma_Project.Enigma.Plugboard import Plugboard


class Enigma:



    def __init__(self,rotors,reflector,rotorPositions,ringSettings,plugboardConnections):
        self.leftRotor = Rotor.Create(rotors[0], rotorPositions[0], ringSettings[0])
        self.middleRotor = Rotor.Create(rotors[1], rotorPositions[1], ringSettings[1])
        self.rightRotor = Rotor.Create(rotors[2], rotorPositions[2], ringSettings[2])

        self.reflector = Reflector.Create(reflector)

        self.plugboard = Plugboard(plugboardConnections)


    def rotate(self):

        if self.middleRotor.isAtNotch():
            self.middleRotor.turnover()
            self.leftRotor.turnover()
        elif self.rightRotor.isAtNotch():
            self.middleRotor.turnover()

        self.rightRotor.turnover()

    def _encrypt(self,c):

        c = ord(c)-65

        self.rotate()

        c = self.plugboard.forward(c)

        c = self.rightRotor.forward(c)
        c = self.middleRotor.forward(c)
        c = self.leftRotor.forward(c)

        c = self.reflector.forward(c)

        c = self.leftRotor.backward(c)
        c = self.middleRotor.backward(c)
        c = self.rightRotor.backward(c)

        c = self.plugboard.forward(c)

        return chr(c+65)

    def encrypt(self,s):
        return "".join([self._encrypt(c) for c in s])
