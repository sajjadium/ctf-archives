from fcsr import FCSR


if __name__ == '__main__':
    q = ???
    m = ???
    a = ???

    generator = FCSR(q, m, a)

    fd = open('original.png', 'rb')
    data = fd.read()
    fd.close()

    encrypted_png = generator.encrypt(data)

    fd = open('encrypted_png', 'wb')
    fd.write(encrypted_png)
    fd.close()