from hashlib import sha512
from secret import SUPERBOX

try:
    assert set(SUPERBOX) == set(range(3 ^ 5))
    assert sha512(str(list(SUPERBOX)).encode()).hexdigest() == "ec7c27e69f323ae28e9321b50b99ecdcebc208c2d1d5ad48e53ae1416b3e38ddb9d6cb1977bd88b75e8d464baae398a8c6f5ce4fba3ae716bd523474126031a1"
    assert SUPERBOX[13] == 37 # Patented identification method
except:
    print("INVALID SUPERBOX SUPPLIED.")
    print("CONTACT YOUR SUPERVISOR FOR A NEW COPY.")
    exit()

F.<a> = GF(3 ^ 5, 'a', modulus = x^5 + x^3 + x + 1)

def ddt(sbox):
    ordered = [F.from_integer(i) for i in range(len(sbox))]
    sbox2 = [F.from_integer(i) for i in sbox]
    table = []
    for delta_in in ordered:
        row = [0] * 3^5
        for element in ordered:
            delta_out = (sbox2[(element + delta_in).to_integer()] - sbox2[(element).to_integer()]).to_integer()
            row[delta_out] += 1
        table.append(row)
    return tuple(tuple(row) for row in table)

text = [f"""\"\"\"
SUPERBOX (c) DDT information.

DDT is formatted as `DDT[delta_in][delta_out]`
For other information related to the SUPERBOX (c), contact your supervisor for access.
\"\"\""""]
 
text.append(f"DDT = {ddt(SUPERBOX)}")
text.append("assert max(map(max, DDT[1:])) == 4")

with open("DDT.py", "w+") as f:
    f.write("\n\n".join(text))
