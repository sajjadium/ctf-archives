def f(t):
    c = list(t)
    for i in range(len(t)):
        for j in range(i, len(t) - 1):
            for k in range(j, len(t) - 2):
                c[k], c[k+1] = c[k+1], c[k]
    return "".join(c)

if __name__ == "__main__":
    flag = open("flag.txt", "r").read()
    open("ciphertext.txt", "w").write(f(flag))
