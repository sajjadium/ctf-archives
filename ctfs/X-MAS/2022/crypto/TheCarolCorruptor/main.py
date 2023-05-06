import random
from carol_corrupter import FLAG, corrupt_carol


class Krampto:
    def __init__(self):
        self.__SECRET = ""
        self.__generate_secret()

    def __generate_secret(self):
        # is this enough?! maybe... maybe not.
        for i in range(31):
            print(random.getrandbits(640))
        self.__SECRET = str(random.getrandbits(2048))[:32]

    def stop_machine(self):
        proposed_secret = input("SECRET: ")
        if proposed_secret == self.__SECRET:
            print(FLAG)
            exit()
        print("Nuh uh, carols are now forever corrupted!")
        exit()

    def corrupt_carol(self):
        corrupted_carol = corrupt_carol()
        for part in corrupted_carol:
            print(part)


if __name__ == "__main__":
    krampto = Krampto()
    options = """
    1. Corrupt Carol
    2. Stop Machine
    3. Quit
    """
    while True:
        print(options)
        option = input("> ")
        if option == "1":
            krampto.corrupt_carol()
        elif option == "2":
            krampto.stop_machine()
        else:
            exit()