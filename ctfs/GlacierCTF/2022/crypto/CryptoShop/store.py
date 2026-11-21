from typing import Union
from typing import Set

# pip install pycryptodome
import Crypto
from Crypto.PublicKey import RSA

SHOP_ITEMS = {
    "USB Rubber Ducky": 1,
    "Malduino": 2,
    "WIFI Deauther": 3,
    "Bluetooth Jammer": 5,
    "GSM Jammer": 7,
    "Bad USB": 10,
    "CTF-Flag": 1000,
}

FLAG = open("flag.txt", "r").read()


def calc_refund_code(price: int, d: int, n: int):
    return pow(price, d, n)


class ShopTransaction:
    def __init__(
        self,
        name: str,
        price: int,
        priv_key: Crypto.PublicKey.RSA.RsaKey
    ):
        self.name = name
        self.price = price
        self.refund_code = calc_refund_code(self.price, priv_key.d, priv_key.n)

    def __str__(self):
        return f"{self.name}: {self.price}(Refund-Code: {self.refund_code})"


class ShopState:
    def __init__(
        self,
        name: str,
        balance: int = 5,
        priv_key: Crypto.PublicKey.RSA.RsaKey = None
    ):
        self.name = name
        self.balance = balance
        self.prev_refunds: Set[int] = set()
        self.priv_key = priv_key
        self.pub_key = self.priv_key.public_key()

    def refund_item(self, price: int, refund_code: int) -> int:
        if refund_code in self.prev_refunds:
            return -1

        reference_code = calc_refund_code(
            price,
            self.priv_key.d,
            self.priv_key.n
        )

        if refund_code != reference_code:
            print(type(refund_code))
            print(type(reference_code))
            print("Refund-Code\n", reference_code)
            print("Calculated-Code\n", refund_code)
            return -2

        self.balance += price

        return 0

    def buy(self, name: str) -> Union[ShopTransaction, int]:
        price = SHOP_ITEMS[name]

        if self.balance < price:
            return -1

        self.balance -= price

        if name == "CTF-Flag":
            print(f"Take this: {FLAG}")

        return ShopTransaction(name, price, self.priv_key)


def generate_keys() -> Crypto.PublicKey.RSA.RsaKey:
    key = RSA.generate(1024)

    return key


def buy_menu(shop_state: ShopState) -> int:

    print("What item do you want to bye?")

    for i, item in enumerate(SHOP_ITEMS):
        print(f"{i}. {item}")

    print()
    item_name = input("> ").strip()

    if item_name not in SHOP_ITEMS.keys():
        print(f"Error! Item {item_name} could not be found")
        return -1

    shop_transaction = shop_state.buy(item_name)

    if isinstance(shop_transaction, int) and shop_transaction == -1:
        print("Error, not enough money")
        return 0

    print(f"Bought {shop_transaction.name} for {shop_transaction.price}")
    print(f"Refund-Code:\n{shop_transaction.refund_code}")
    return 0


def refund_menu(shop_state: ShopState) -> int:
    print("What do you want to refund?")
    print("Please provide the refundcode")
    refund_code = input("> ").strip()
    print("Please provide the price")
    refund_amount = input("> ").strip()

    try:
        refund_amount = int(refund_amount)
    except ValueError:
        print(f"Value {refund_amount} not a valid price")
        return 0
    try:
        refund_code = int(refund_code)
    except ValueError:
        print(f"Invalid {refund_code}")
        return 0

    ret_val = shop_state.refund_item(refund_amount, refund_code)

    if ret_val == 0:
        print("Successfully refunded")

    if ret_val == -1:
        print("Error, this refund code was already used!!")

    if ret_val == -2:
        print("Error, this refund code does not match the price!")

    return 0


def display_menu():
    key = generate_keys()

    print("Welcome to the PWN-Store. Please authenticate:")
    user = input("Your Name: ")
    print(f"Welcome back {user}!")

    user_shop_state = ShopState(user, priv_key=key)

    print(f"Customernumber: {user_shop_state.pub_key.n}")

    while True:
        print()
        print(f"Accountname: {user} (Balance: {user_shop_state.balance}€)")
        print("1. List Items")
        print("2. Buy Item")
        print("3. Refund Item")
        print("4. Exit")
        print()
        action = input("> ")

        try:
            action = int(action.strip())
        except ValueError:
            print(f"Error, {action} is not a valid number!")
            continue

        if action < 0 or action > 5:
            print(f"Error, {action} is not a valic action")

        if action == 1:
            for i, item in enumerate(SHOP_ITEMS):
                print(f"{i}. {item} (Price: {SHOP_ITEMS[item]})")

        if action == 2:
            ret_val = buy_menu(user_shop_state)
            if ret_val != 0:
                print("An Error occured! Exiting")
                break

        if action == 3:
            refund_menu(user_shop_state)

        if action == 4:
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(display_menu())
