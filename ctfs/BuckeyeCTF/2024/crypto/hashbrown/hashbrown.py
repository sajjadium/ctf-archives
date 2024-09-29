import os

# pip install pycryptodome
from Crypto.Cipher import AES

flag = "bctf{????????????????}"
secret = os.urandom(16)

my_message = "\n".join(
    [
        "Grate the raw potatoes with a cheese grater, place them into a bowl and cover completely with water. Let sit for 10 minutes.",
        "Drain the grated potatoes well; if this is not done thoroughly the potatoes will steam instead of fry.",
        "Mix in chopped onions by hand.",
        "Mix the egg OR flour into the hash brown mixture evenly. This will allow the hash browns to stay together when frying.",
        "Place a large frying pan on medium-high heat and add enough oil to provide a thin coating over the entire bottom of the pan.",
        "When the oil has come up to temperature apply a large handful of potatoes to the pan and reshape into a patty that is about 1/4-1/2 inch (6-12 mm) thick. The thinner the patty, the crispier the hash browns will be throughout.",
        "Flip when they are crisp and brown on the cooking side. They should also stick together nicely before they are flipped. This should take about 5-8 minutes.",
        "The hash browns are done when the new side is brown and crispy. This should take another 3-5 minutes.",
    ]
).encode()


def aes(block: bytes, key: bytes) -> bytes:
    assert len(block) == len(key) == 16
    return AES.new(key, AES.MODE_ECB).encrypt(block)


def pad(data):
    padding_length = 16 - len(data) % 16
    return data + b"_" * padding_length


def hash(data: bytes):
    data = pad(data)
    state = bytes.fromhex("f7c51cbd3ca7fe29277ff750e762eb19")

    for i in range(0, len(data), 16):
        block = data[i : i + 16]
        state = aes(block, state)

    return state


def sign(message, secret):
    return hash(secret + message)


def main():
    print("Recipe for hashbrowns:")
    print(my_message)
    print("Hashbrowns recipe as hex:")
    print(my_message.hex())
    print("Signature:")
    print(sign(my_message, secret).hex())
    print()

    print("Give me recipe for french fry? (as hex)")
    your_message = bytes.fromhex(input("> "))
    print("Give me your signiature?")
    your_signiature = bytes.fromhex(input("> "))
    print()

    print("Your recipe:")
    print(your_message)
    print("Your signiature:")
    print(your_signiature.hex())
    print()

    if b"french fry" not in your_message:
        print("That is not a recipe for french fry!!")
    elif your_signiature != sign(your_message, secret):
        print("That is not a valid signiature!!")
    else:
        print("Thank you very much. Here is your flag:")
        print(flag)


if __name__ == "__main__":
    main()
