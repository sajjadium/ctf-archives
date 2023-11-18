def encrypt():
    message = input("Enter the message you would like to encrypt: ").strip()
    key = input("Enter the key to encrypt with: ").strip()

    key_int = sum(ord(char) for char in key)

    encrypted_message = ""

    for c in message:
        if c in alphabet:
            position = alphabet.find(c)
            new_position = (position + key_int)
            new_character = alphabet[new_position]
            encrypted_message += new_character
        else:
            encrypted_message += c