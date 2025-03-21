from Enigma.Enigma import Enigma

print('''                                                                                              
────────────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████──██████──────────██████──██████████──██████████████──██████──────────██████──██████████████─
─██░░░░░░░░░░██──██░░██████████──██░░██──██░░░░░░██──██░░░░░░░░░░██──██░░██████████████░░██──██░░░░░░░░░░██─
─██░░██████████──██░░░░░░░░░░██──██░░██──████░░████──██░░██████████──██░░░░░░░░░░░░░░░░░░██──██░░██████░░██─
─██░░██──────────██░░██████░░██──██░░██────██░░██────██░░██──────────██░░██████░░██████░░██──██░░██──██░░██─
─██░░██████████──██░░██──██░░██──██░░██────██░░██────██░░██──────────██░░██──██░░██──██░░██──██░░██████░░██─
─██░░░░░░░░░░██──██░░██──██░░██──██░░██────██░░██────██░░██──██████──██░░██──██░░██──██░░██──██░░░░░░░░░░██─
─██░░██████████──██░░██──██░░██──██░░██────██░░██────██░░██──██░░██──██░░██──██████──██░░██──██░░██████░░██─
─██░░██──────────██░░██──██░░██████░░██────██░░██────██░░██──██░░██──██░░██──────────██░░██──██░░██──██░░██─
─██░░██████████──██░░██──██░░░░░░░░░░██──████░░████──██░░██████░░██──██░░██──────────██░░██──██░░██──██░░██─
─██░░░░░░░░░░██──██░░██──██████████░░██──██░░░░░░██──██░░░░░░░░░░██──██░░██──────────██░░██──██░░██──██░░██─
─██████████████──██████──────────██████──██████████──██████████████──██████──────────██████──██████──██████─
────────────────────────────────────────────────────────────────────────────────────────────────────────────
────────────────────────────────────────────────────────────────────────────────────────────────────────────
─────────────────██████──██████──██████████████──────────██████████████──────────████████───────────────────                                
─────────────────██░░██──██░░██──██░░░░░░░░░░██──────────██░░░░░░░░░░██──────────██░░░░██───────────────────
─────────────────██░░██──██░░██──██░░██████░░██──────────██░░██████░░██──────────████░░██───────────────────
─────────────────██░░██──██░░██──██░░██──██░░██──────────██░░██──██░░██────────────██░░██───────────────────
─────────────────██░░██──██░░██──██░░██──██░░██──────────██░░██──██░░██────────────██░░██───────────────────
─────────────────██░░██──██░░██──██░░██──██░░██──────────██░░██──██░░██────────────██░░██───────────────────
─────────────────██░░██──██░░██──██░░██──██░░██──────────██░░██──██░░██────────────██░░██───────────────────
─────────────────██░░░░██░░░░██──██░░██──██░░██──────────██░░██──██░░██────────────██░░██───────────────────
─────────────────████░░░░░░████──██░░██████░░██──██████──██░░██████░░██──██████──████░░████─────────────────
───────────────────████░░████────██░░░░░░░░░░██──██░░██──██░░░░░░░░░░██──██░░██──██░░░░░░██─────────────────
─────────────────────██████──────██████████████──██████──██████████████──██████──██████████─────────────────
────────────────────────────────────────────────────────────────────────────────────────────────────────────

''')

print("some settings were conveniently set up for you :)")
print("current enigma settings:")
print("MODEL         : |    Enigma M3    |")
print("RING SETTINGS : |  A  |  A  |  A  |")
print("REFLECTOR     : |      UKW B      |")
print("PLUGBOARD     : | [- DISABLED -]  |")

print("input your rotors (ex. I II III) :")
inp_str = input()
rotors = inp_str.split()
print(rotors)

print("input your rotor positions (ex. A A A) :")
inp_str = input()
rotor_pos = [ord(i) - 65 for i in inp_str.split()]
print(rotor_pos)

e = Enigma(rotors, "B", rotor_pos, [0, 0, 0], "")

SECRET = "[REDACTED]"

FLAG = "KUBANCTF" + SECRET

enc = e.encrypt(FLAG)

print(enc)