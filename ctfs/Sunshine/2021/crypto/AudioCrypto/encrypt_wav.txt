import wave
import struct
import random
import math


#Since this is an audio file it is IMPOSSIBLE for you to apply any cryptanlysis techniques!
#Audio files aren't like silly text files with trivial frequency analysis!
#TODO: Verify above claim before releasing encryption to the public.

#This seems like it should be as secure as a one time pad, even though my cryptography professor says it isn't.
#He's just out of touch probably, it generates a unique stream each time for each combination.
class LCGCryptStream:

    #TODO: Find a more secure way to generate the modulus and prevent audio clipping.
    def __init__(self):
        valid = False
        while not valid:
            valid = True
            #For some reason the program runs really slowly if I go above 2**12 for these? Anyway I should have 48 bits of security now.
            #Brute force that skid.
            self.m = random.randint(2**9, 2**12)
            self.a = random.randint(0, 2**12)
            self.b = random.randint(0, 2**12)
            self.state = random.randint(0, 2**12)
            #Just make sure there aren't any cyclical loops, if it doesn't loop in the first 100 we should be good
            seen = []
            for i in range(100):
                next = self.next_byte()
                if next in seen:
                    valid = False
                seen.append(next)
        
    #TODO: Comment code section.
    def next_byte(self):
        while True:
            #I did multiplication originally but apparently multiplier LCGs can be reversed 
            self.state = (self.state * self.a + self.b) % self.m
            if self.state < 2 ** 8:
                return self.state
        
    #TODO: Switch from using bitwise AND to bitwise XOR to prevent loss of data.
    #TODO: Above TODO completed.
    def encryptFrame(self, frame):
        assert len(frame) == 2
        val = struct.unpack("<h", frame)[0]
        #TODO: Figure out how negative numbers work with XOR so I can stop doing this hack.
        val += 2**15
        val = (val ^ (self.next_byte() << 8 | self.next_byte())) % (2 ** 16)
        #TODO: Figure out how negative numbers work with XOR so I can stop doing this hack.
        val -= 2**15
        #print(hex(val))
        return struct.pack("<h", val)
        
    #TODO: Find a way to securely transmit this information.
    def __str__(self):
        return "LCGCryptStream(m = %d, a = %d, b %d, state = %d)"%(self.m, self.a, self.b, self.state)
        
        
#TODO: Standardize function and variable name format.
def encrypt_audio(inp, out):
    inpaudio = wave.open(inp, mode='rb')
    encaudio = wave.open(out, mode='wb')
    encaudio.setframerate(inpaudio.getframerate())
    encaudio.setnframes(inpaudio.getnframes())
    print("Frames:", inpaudio.getnframes())
    encaudio.setsampwidth(inpaudio.getsampwidth())
    encaudio.setnchannels(inpaudio.getnchannels())
    cryptStream = LCGCryptStream()
    print("LCG initial state", cryptStream)
    frames = inpaudio.readframes(inpaudio.getnframes())
    #Pad the frames out so the length doesn't leak. Apparently thats a side channel.
    frames += b"\x42"*1000
    while len(frames) % 1000 != 0:
        frames += b"\x42"
    #we read the wav frame by frame
    for i in range(0, len(frames), 2):
        frame = frames[i:i+2]
        #This way I don't lose my mind waiting
        if i % (len(frames) // 100) == 0:
            print("%d percent done!"%(i / (len(frames) // 100)))
        encaudio.writeframes(cryptStream.encryptFrame(frame))
    inpaudio.close()
    encaudio.close()
    
#TODO: Actually take user input for these file names so I stop leaking my filesystem
encrypt_audio("/home/bigstrongalligatorman/cyberCrime/flag_plain.wav", "/home/bigstrongalligatorman/cyberCrime/flag_encrypted.wav")
    
