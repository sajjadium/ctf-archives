import time
from random import SystemRandom
from ethsnarks import jubjub, eddsa, field

FLAG = open('flag.txt', 'rb').read()

def serialize(sig: eddsa.Signature):
    return (sig.R.compress() + int(sig.s).to_bytes(32, 'big')).hex()

def deserialize(b):
    b = bytes.fromhex(b)

    R = jubjub.Point.decompress(b[:32])
    s = field.FQ(int.from_bytes(b[32:], 'big'))

    return R, s


TICKET_PRICE = {
    "normal": 10,
    "FLAG": 100,
}

TICKET_VALUE = {
    "normal": 10,
}

ISSUED_TICKETS = {}

REFUNDED_TICKETS = []

class Tempus:
    def __init__(self, username: str):
        self.signer = eddsa.MiMCEdDSA()
        self.sk, self.pk = self.signer.random_keypair()
        self.username = int.from_bytes(username.encode(), 'big')
        self.userid = self.signer.hash_public(self.pk, self.username)
        self.balance = 10
        self.refunded = []
        self.issued_tickets = {}
        self.rand = SystemRandom()

        print(f"Successfully registered with User ID: {self.userid}")

    def buy_ticket(self, ticket_type):
        price = TICKET_PRICE.get(ticket_type)
        if self.balance >= price:
            self.balance -= price
            new_ticket_id = self.rand.getrandbits(128)
            ticket_id = int.to_bytes(new_ticket_id, 16, "big")
            signature = self.signer.sign(new_ticket_id, self.sk)
            ISSUED_TICKETS[self.signer.hash_public(signature.A, self.username, new_ticket_id)] = ticket_type
            signature = serialize(signature.sig)

            if ticket_type == "FLAG":
                print(FLAG)
            else:
                print(f"Your ticket: {ticket_id.hex()+signature}")
        else:
            print("[ERROR] Insufficient balance")

    def refund_ticket(self):
        try:
            ticket = input("Input ticket: ")
            ticket_id, signature = bytes.fromhex(ticket[:32]), deserialize(ticket[32:])
            if self.signer.verify(self.pk, signature, int.from_bytes(ticket_id, 'big')):
                ticket_key = int(input("Input ticket key: "))
                if ticket_key in ISSUED_TICKETS and signature not in REFUNDED_TICKETS:
                    ticket_type = ISSUED_TICKETS.get(ticket_key)
                    value = TICKET_VALUE.get(ticket_type, 0)
                    self.balance += value
                    REFUNDED_TICKETS.append(signature)
                    print("Ticket succesfully refunded!")
                else:
                    print("[ERROR] Invalid ticket")
            else:
                print("[ERROR] Invalid ticket")
        except Exception:
            print("[ERROR] Invalid ticket")

    def menu(self):
        print("[1] Buy ticket      ($10)")
        print("[2] Buy FLAG        ($100)")
        print("[3] Refund ticket")
        print("[4] Exit")
        print("")
        print(f"Your balance: ${self.balance}")

def main():

    username = input("Username: ")
    ticketer = Tempus(username)

    while True:
        time.sleep(0.5)
        ticketer.menu()
        option = input("$> ")
        if option == "1":
            ticketer.buy_ticket("normal")
        elif option == "2":
            ticketer.buy_ticket("FLAG")
        elif option == "3":
            ticketer.refund_ticket()
        else:
            break

if __name__ == "__main__":
    main()