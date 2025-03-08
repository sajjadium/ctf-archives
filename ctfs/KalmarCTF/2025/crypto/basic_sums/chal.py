
with open("flag.txt", "rb") as f:
    flag = f.read()

# I found this super cool function on stack overflow \o/ https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

assert len(flag) <= 45

flag = int.from_bytes(flag, 'big')

base = int(input("Give me a base! "))

if base < 2:
    print("Base is too small")
    quit()
if base > 256:
    print("Base is too big")
    quit()

print(f'Here you go! {sum(numberToBase(flag, base))}')
