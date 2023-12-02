from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from utils import AEMC, InvalidTagError
import binascii
import secrets
import base64
import random
import signal
import json

TIMEOUT    = 720
FLAG       = open("/flag", "r").read()
INFO       = b"W3llc0m3 t0 W4nn4G4m3 Ch4mpi0nsh1p 2023"
MAX_ROUNDS = 20
ROUND      = 1
MAX_TRIES  = 14

class AmongSUS:
    N_PLAYERS = 512
    TASKS     = [
        "Catch Fish"   , "Clean Vent"         , "Collect Shells" , "Help Critter"     ,
        "Chart Course" , "Clear Asteroids"    , "Divert Power"   , "Hoist Supplies"   ,
        "Clean Toilet" , "Collect Vegetables" , "Empty Chute"    , "Measure Weather"
    ]

    @classmethod
    def generate_password(self, player: str, salt: bytes):
        return HKDF(
            algorithm=hashes.BLAKE2b(digest_size=64),
            salt=salt,
            info=INFO,
            length=32
        ).derive(player.encode())

    @classmethod
    def info_task(self, player):
        task = random.choice(self.TASKS)
        id   = secrets.token_hex(0x10)

        digest = hashes.Hash(hashes.BLAKE2b(digest_size=64))
        digest.update(
             json.dumps({
                "id": id,
                "player": player,
                "task": task
            }).encode()
        )
        return digest.finalize()

    def __init__(self) -> None:
        self.salt      = secrets.token_bytes(0x0C)
        self.crewmates = [
            f"player_{secrets.token_bytes(0x10).hex()}"  for _ in range(self.N_PLAYERS)
        ]
        self.imposter  = random.choice(self.crewmates)

    def info_players(self):
        print("[INFO PLAYERS]")

        for player in self.crewmates:
            print(">", player)

    def generate_task(self):
        print("[GENERATE TASK]")

        token = AEMC(master_key=self.generate_password(self.imposter, self.salt)).encrypt(
            plaintext=self.info_task(random.choice(self.crewmates)),
            nonce=self.salt,
            associated_data=INFO
        )
        print("> Task Token:", base64.b64encode(token).decode())

    def do_task(self):
        print("[DO TASK]")

        try:
            token = base64.b64decode(input("> Enter Task Token (in base64): "))
            task  = AEMC(master_key=self.generate_password(self.imposter, self.salt)).decrypt(
                ciphertext=token,
                nonce=self.salt,
                associated_data=INFO
            )
            # print(task) # Nah
            print("> Doing task...")

        except (binascii.Error, InvalidTagError):
            print(f"> Invalid token: Impostorrrr!!!")
    
    def report_imposter(self):
        print("[REPORT IMPOSTER]")

        return input("> Who? ") == self.imposter 
    
if __name__ == "__main__":
    signal.alarm(TIMEOUT)

    print("""

                    ▄████████   ▄▄▄▄███▄▄▄▄    ▄██████▄  ███▄▄▄▄      ▄██████▄          ▄████████ ███    █▄     ▄████████      
                    ███    ███ ▄██▀▀▀███▀▀▀██▄ ███    ███ ███▀▀▀██▄   ███    ███        ███    ███ ███    ███   ███    ███      
                    ███    ███ ███   ███   ███ ███    ███ ███   ███   ███    █▀         ███    █▀  ███    ███   ███    █▀       
                    ███    ███ ███   ███   ███ ███    ███ ███   ███  ▄███               ███        ███    ███   ███             
                    ▀███████████ ███   ███   ███ ███    ███ ███   ███ ▀▀███ ████▄       ▀███████████ ███    ███ ▀███████████      
                    ███    ███ ███   ███   ███ ███    ███ ███   ███   ███    ███               ███ ███    ███          ███      
                    ███    ███ ███   ███   ███ ███    ███ ███   ███   ███    ███         ▄█    ███ ███    ███    ▄█    ███      
                    ███    █▀   ▀█   ███   █▀   ▀██████▀   ▀█   █▀    ████████▀        ▄████████▀  ████████▀   ▄████████▀       
                                                                                                                                
    """)
    print("[!] Welcome to Among SUS game. You need to find the exact impostor, otherwise everyone will be killed...")
    print(f"[!] There is only one impostor among all {AmongSUS.N_PLAYERS} players")
    print("[!] Press ENTER to continue...")
    input("")

    while True:
        game    = AmongSUS()
        tries   = 0
        success = False

        if ROUND > MAX_ROUNDS:
            print(f"[*] Congratulation: {FLAG}")
            exit(0)

        print(f"\n[*] Round {ROUND}/{MAX_ROUNDS}")
        print(f"[*] This Game's Token: {game.salt.hex()}")

        while True:
            print("\nYour options:")
            print("1) Info players")
            print("2) Generate task")
            print("3) Do task")
            print("4) Report Imposter")
            print("5) Quit")

            choice = input("> ")

            if choice == '1':
                game.info_players()

            elif choice == '2':
                game.generate_task()

            elif choice == '3':
                if tries >= MAX_TRIES:
                    print("[!] Sorry, you've reached your rate limit")
                    continue
                game.do_task()
                tries += 1

            elif choice == '4':
                if game.report_imposter():
                    success = True
                break

            elif choice == '5':
                print("[!] Bye")
                exit(0)

            else:
                print(f"[!] Invalid choice")

        if success:
            print("[!] Good!")
            ROUND += 1
            continue
        else:
            print("[!] Oops!")
            break