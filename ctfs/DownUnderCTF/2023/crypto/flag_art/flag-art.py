message = open('./message.txt', 'rb').read() + open('./flag.txt', 'rb').read()

palette = '.=w-o^*'
template = list(open('./mask.txt', 'r').read())

canvas = ''
for c in message:
    for m in [2, 3, 5, 7]:
        while True:
            t = template.pop(0)
            if t == 'X':
                canvas += palette[c % m]
                break
            else:
                canvas += t

print(canvas)
