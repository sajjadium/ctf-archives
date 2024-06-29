from hashlib import sha256

hex_alpha = "0123456789abcdef"

print("== Welcome to the onboard slot machine! ==")
print("If all the slots match, you win!")
print("We believe in skill over luck, so you can choose the number of slots.")
print("We'll even let you pick your lucky number (little endian)!")

lucky_number = input("What's your lucky (hex) number: ").lower().strip()
lucky_number = lucky_number.rjust(len(lucky_number) + len(lucky_number) % 2, "0")
if not all(c in hex_alpha for c in lucky_number):
    print("Hey! That's not a hex number! -999 luck!")
    exit(1)
hash = sha256(bytes.fromhex(lucky_number)[::-1]).digest()[::-1].hex()

length = min(32, int(input("How lucky are you feeling today? Enter the number of slots: ")))

print("=" * (length * 4 + 1))
print("|", end="")
for c in hash[:length]:
    print(f" {hex_alpha[hex_alpha.index(c) - 1]} |", end="")
print("\n|", end="")
for c in hash[:length]:
    print(f" {c} |", end="")
print("\n|", end="")
for c in hash[:length]:
    print(f" {hex_alpha[hex_alpha.index(c) - 15]} |", end="")
print("\n" + "=" * (length * 4 + 1))

if len(set(hash[:length])) == 1:
    print("Congratulations! You've won:")
    flag = open("flag.txt").read()
    print(flag[:min(len(flag), length)])
else:
    print("Better luck next time!")