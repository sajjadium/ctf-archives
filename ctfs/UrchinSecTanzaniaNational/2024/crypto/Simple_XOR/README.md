cryptography easy author : @tahaafarooq

Right! an XOR challenge a pretty basic one. Below is the source code of the script that was used to encrypt the message containing the flag, Help me get the flag back!

message = 'urchinsec{fake_flag}' # message comes here
key = 'a' # key comes here
encrypted = ''.join([chr(ord(x) ^ ord(key)) for x in message])
with open("enc", "w") as enc:
    enc.write(encrypted)

print("encrypted")
