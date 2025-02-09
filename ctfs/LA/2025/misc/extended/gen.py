flag = "lactf{REDACTED}"
extended_flag = ""

for c in flag:
    o = bin(ord(c))[2:].zfill(8)

    # Replace the first 0 with a 1
    for i in range(8):
        if o[i] == "0":
            o = o[:i] + "1" + o[i + 1 :]
            break

    extended_flag += chr(int(o, 2))

print(extended_flag)

with open("chall.txt", "wb") as f:
    f.write(extended_flag.encode("iso8859-1"))
