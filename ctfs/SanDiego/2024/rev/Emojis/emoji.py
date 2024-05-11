def main():
    print("what do you think the key is?")
    encrypted = '🙚🙒🙌🙭😌🙧🙬🙻🙠🙓😣🙯🙖🙺🙠🙖😡🙃🙭🙿🙩🙟😯🙮🙬🙸🙻🙦😨🙩🙽🙉🙻🙑😯🙥🙻🙳🙐🙓😿🙯🙽🙉🙣🙐😡🙹🙖🙤🙪🙞😿🙰🙨🙤🙐🙕😯🙨🙽🙳🙽🙊😷'
    key = input()
    plaintext = ''.join([chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encrypted)])
    print("your decrypted text:", plaintext)

main()

