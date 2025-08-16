import math
import json

def enc(msg, a=0????, b=0????, M=0????):
    p = [ord(c) for c in msg]
    max_p = max(p) if p else 0
    prod = a * b
    s = 0???????
    if prod < 2 * max_p:
        s = math.ceil(math.sqrt((2 * max_p) / prod))
    a_eff = a * s
    b_eff = b * s

    l = [int(round((2 * x / (a_eff * b_eff)) * M)) for x in p]
    return {"l": l}

if __name__ == "__main__":
    msg = "flag_is_here"
    c = enc(msg)
    print(json.dumps(c, ensure_ascii=False, indent=2))