from OneWayEnigma import *

settings = getSettings()
encryptor = Enigma(settings)

print(Encrypt(input("ENTER_YOUR_SECRETS_HERE >>> "), encryptor))

# No. of rotors = 5, sequence = (5,3,1,2,4), positions = (?, ?, ?, ?, ?)