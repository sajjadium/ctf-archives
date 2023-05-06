enc = b'\x0cYUV\x02\x13\x16\x1a\x01\x04\x05C\x00\twcx|z(((%.)=K%(>'
enc1 = b'\x0bPPS\r\x0b\x02\x0f\x12\r\x03_G\t\x08yb}v+--*+*8=W,>'
enc2 = b'\x07A[\x06\\\r\x15\t\x04\x07\x18VG]U]@\x02\x08&9&%\' 41".;'

import codecs
import random

class pass_w:
    x = "hjlgyjgyj10hadanvbwdmkw00OUONBADANKHM;IMMBMZCNihaillm"
    def encode(self, text, i = -1):
        

        if i < 0 or i > len(self.x) + 1:
            i = random.randint(0, len(self.x) + 1)

        out = chr(i)
        for c in text:
            out += chr(ord(c) ^ ord(self.x[i]))
            i = (i + 1)%79                 

        return codecs.encode(out)
    

y = pass_w()
print(y.encode("REDACTED"))


#Enclose password within GrabCON{}