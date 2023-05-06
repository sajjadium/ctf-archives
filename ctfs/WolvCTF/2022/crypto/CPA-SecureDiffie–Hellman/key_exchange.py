from flask import Flask
from flask import request
from Crypto.Util.number import bytes_to_long, long_to_bytes
from hashlib import sha256
from hmac import new

app = Flask(__name__)

# ephemerals live on as seeds!

# wrap flag in wsc{}

# Someone has cracked sha-256 and has started impersonating me to Alice on the internet!
# Here's the oracle they proved sha-256 is forgeable on
# Guess the internet will just have to move on to sha-512 or more likely sha-3

key = {
    '0' : 0 , '1' : 1 , '2' : 2 , '3' : 3 , '4' : 4 , '5' : 5 , '6' : 6 ,
    'a' : 70, 'b' : 71, 'c' : 72, 'd' : 73, 'e' : 74, 'f' : 75, 'g' : 76, 'h' : 77, 'i' : 78, 'j' : 79, 
    'k' : 80, 'l' : 81, 'm' : 82, 'n' : 83, 'o' : 84, 'p' : 85, 'q' : 86, 'r' : 87, 's' : 88, 't' : 89, 
    'u' : 90, 'v' : 91, 'w' : 92, 'x' : 93, 'y' : 94, 'z' : 95, '_' : 96, '#' : 97, '$' : 98, '!' : 99, 
}

def bytes_to_long_flag(bytes_in):
    long_out = ''
    for b in bytes_in:
        long_out += str(key[chr(b)])
    return int(long_out)

def long_to_bytes_flag(long_in):
    new_map = {v: k for k, v in key.items()}
    list_long_in = [int(x) for x in str(long_in)]
    str_out = ''
    i = 0
    while i < len(list_long_in):
        if list_long_in[i] < 7:
            str_out += new_map[list_long_in[i]]
        else:
            str_out += new_map[int(str(list_long_in[i]) + str(list_long_in[i + 1]))]
            i += 1
        i += 1
    return str_out.encode("utf_8")

def diffie_hellman(A):
    p = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
    g = 5016207480195436608185086499540165384974370357935113494710347988666301733433042648065896850128295520758870894508726377746919372737683286439372142539002903041
    B = pow(g,b,p) #unused in our protocal
    s = pow(A,b,p)
    message = b'My totally secure message to Alice'
    password = long_to_bytes(s)
    my_hmac = new(key=password, msg = message, digestmod=sha256)
    return str(bytes_to_long(my_hmac.digest()))

@app.route("/")
def home():
    A = request.args.get('A')
    if not A:
        return "Missing required query string parameter: A"
    else:
        try:
            result = diffie_hellman(int(A))
            return result
        except:
            return "A must be an integer: " + A;


f = open("flag.txt", "r")
flag = f.read()
b = bytes_to_long_flag(flag.encode('utf-8'))

if __name__ == "__main__":
    app.run(port=54321)

# Someone mentioned CPA-Security to me... No idea what that has to do with this

# All the homies hate 521