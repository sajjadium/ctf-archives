def f(t):
    c = list(t)
    for i in range(len(t)):
        for j in range(i, len(t) - 1):
            c[j], c[j+1] = c[j+1], c[j]
    return "".join(c)

if __name__ == "__main__":
    flag = open("flag", "r").read()
    open("ciphertext", "w").write(f(flag))