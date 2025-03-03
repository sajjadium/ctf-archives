from string import ascii_uppercase, digits

class rotors:

    saved = {
            1:('{K8UMNZBGS20D3IR_5CEFYOQPX4JH1VA}96TW7L',[9]),
            2:('EFXRSBQ1MC3GYW_9{47AVT8JP5ON6U20ZK}HDIL',[23]),
            3:('WUXQGVJHT2YO043MK17LC9ANZBP{_S6D}I5EFR8',[7]),
            4:('W0K2NBVRPJTZY1XHD9478L{QUMG6I_O3FAS5}CE',[30]),
            5:('V3F_1QA}L4WOZIM8SY7P9XG20CDNKJUH5B6ERT{',[13])
            }

    rotorSequence = {}

    def __init__(self, **kwargs):

        # default values
        self.preset = 1
        self.offset = 0
        self.position = 0

        # switching to given values
        if "rotor_num" in kwargs: self.rotor_num = kwargs["rotor_num"]
        if "preset" in kwargs: self.preset = kwargs["preset"] 
        if "offset" in kwargs: self.offset = kwargs["offset"] 
        if "position" in kwargs: self.position = kwargs["position"]
        if "notches" in kwargs: self.notches = kwargs["notches"]
        else: self.notches = rotors.saved[self.preset][1]
        
        # setting up remaining properties
        rotors.rotorSequence[self.rotor_num] = self 
        self.mapper(self.preset) 
        self.notch_found = False

    def mapper(self, preset=1):

        '''takes preset number as an argument and maps the\n
        rotor wiring accordingly'''

        statorKey = ascii_uppercase + digits + "_{}"
        rotorKey = rotors.saved[preset][0]
        map = {}
        rotorMap = {}
        for i,char in enumerate(statorKey):
            map[char]=i
            map[i]=char
        
        for i in range(len(statorKey)):
            rotorMap[i] = [map[rotorKey[i]]]
        for i in range(len(statorKey)):
            temp = rotorMap[map[rotorKey[i]]]
            rotorMap[map[rotorKey[i]]] = (temp[0], i)
        rotorMap["wiring"] = rotorKey
        
        self.wiring = rotorMap    

    def rotate(self):

        '''rotates the rotorset once (for each keypress)'''

        # should this rotor make the next rotor rotate?
        if self.position in self.notches and self.rotor_num < len(rotors.rotorSequence):
                rotors.rotorSequence[self.rotor_num + 1].notch_found = True

        # to rotate or not to rotate
        if self.rotor_num == 1: 
            self.position +=1

        elif self.notch_found:
            self.position += 1
            self.notch_found = False
        
        # Completion of rotation >>> Reset
        self.position %= 39

    def passLeft(self, contact):

        '''takes contact from right and sends to left\n
        meanwhile taking care of rotation in the\n
        FORWARD CYCLE'''

        self.rotate() # Rotation prior to connection

        LSCN = (self.wiring[(self.position-self.offset+contact)%39][0] - (self.position-self.offset))%39

        return LSCN

    def passRight(self, contact):
        pass

class steckerbrett:

    def __init__(self):

        self.mapper()

    def mapper(self):
        statorKey = ascii_uppercase + digits + "_{}"
        self.pairs = {}
        self.map = {}
        for i,char in enumerate(statorKey):
            self.map[char]=i
            self.map[i]=char
            self.pairs[char]= char

    def connect(self, char):
        return self.map[self.pairs[char]]

    def disconnect(self, contact):
        return self.pairs[self.map[contact]]

def getSettings():

    num = int(input('How many rotors do you want? >>>   '))

    settings['rotors']['sequence'] = []
    for i in range(num):
        rotor_num = int(input(f'Enter number of rotor {i+1} from 1-5 >>>   '))
        settings['rotors']['sequence'].append(rotor_num)
    
    settings['rotors']['positions'] = []
    for i in range(num):
        position = int(input(f'Enter position of rotor {i+1} from 0-38 >>>   '))
        settings['rotors']['positions'].append(position)

    return settings

def Enigma(settings):

    plugboard = steckerbrett()
    sequence = settings['rotors']['sequence']
    positions = settings['rotors']['positions']
    rotorSet = {}
    for i in range(len(sequence)):
        rotorSet[i] = rotors(rotor_num=i+1, preset=sequence[i], position=positions[i])

    return plugboard, rotorSet

def Encrypt(message, enigma):

    plugboard, rotorSet = enigma
    encrypted = ''
    for char in message:
        contact = plugboard.connect(char)
        for i in range(1, len(rotors.rotorSequence)+1):
            contact = rotors.rotorSequence[i].passLeft(contact)
        char = plugboard.disconnect(contact)
        encrypted += char
    return encrypted

def Decrypt(message, enigma):
    pass

# Default Settings for The Enigma
settings = {'version':1,
            'phrase':"Anyth1nG RanD0M Go3S HeR=E 69 And HWa+t CtuaLFck39875/",
            'rotors':{'sequence':[1,1,1],
                    'positions':[11,22,33],
                    'offset':[15,2,31]}}