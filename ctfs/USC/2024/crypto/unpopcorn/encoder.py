m = 57983
p = int(open("p.txt").read().strip())

def pop(s):
    return map(lambda x: ord(x)^42, s)

def butter(s):
    return map(lambda x: x*p%m, s)

def churn(s):
    l = list(map(lambda x: (x << 3), s))
    return " ".join(map(lambda x: "{:x}".format(x).upper(), l[16:] + l[:16]))

flag = open("flag.txt").read().strip()
message = open("message.txt", "w")
message.write(churn(butter(pop(flag))))
message.close()
