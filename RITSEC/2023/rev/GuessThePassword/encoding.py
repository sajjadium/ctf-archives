import hashlib, json

class Encoder():

    def __init__(self, secrets_file):
        with open(secrets_file, "r") as file:
            data = json.load(file)
            self.hashed_key = data["key"]
            self.secret = data["secret"]

    def flag_from_pwd(self, key):

        # This function uses code from Vincent's response to this question on SOverflow: https://stackoverflow.com/questions/29408173/byte-operations-xor-in-python
        byte_secret = self.secret.encode()           # convert key to bytes
        byte_key = key.encode()                     # convert the user input to bytes
        
        return bytes(a ^ b for a, b in zip(byte_secret, byte_key)).decode()


    def hash(self, user_input):
        salt = "RITSEC_Salt"
        return hashlib.sha256(salt.encode() + user_input.encode()).hexdigest()


    def check_input(self, user_input):
        hashed_user_input = self.hash(user_input)
        # print("{0} vs {1}".format(hashed_user_input, self.hashed_key))
        return hashed_user_input == self.hashed_key


if __name__ == "__main__":
    main()
