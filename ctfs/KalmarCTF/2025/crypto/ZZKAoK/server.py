import json

from intarg import Verifier, rel_factor

try:
    FLAG = open('flag.txt', 'r').read().strip()
except:
    FLAG = "kalmar{testflag}"

NUMBER = int('''
2519590847565789349402718324004839857142928212620403202777713783604366202070
7595556264018525880784406918290641249515082189298559149176184502808489120072
8449926873928072877767359714183472702618963750149718246911650776133798590957
0009733045974880842840179742910064245869181719511874612151517265463228221686
9987549182422433637259085141865462043576798423387184774447920739934236584823
8242811981638150106748104516603773060562016196762561338441436038339044149526
3443219011465754445417842402092461651572335077870774981712577246796292638635
6373289912154831438167899885040445364023527381951378636564391212010397122822
120720357'''.replace('\n', ''))

def out(obj):
    print(json.dumps(obj))

def inp():
    try:
        s = input()
        return json.loads(s)
    except Exception as e:
        out({
            'type': 'error',
            'message': 'Invalid JSON: ' + str(e)
        })
        exit(1)

def check_proof(msg):
    N = msg['N']
    pf = msg['pf']
    vf = Verifier(pf, N)

    p = vf.com()
    q = vf.com()

    a1 = vf.com()
    a2 = vf.com()
    a3 = vf.com()
    a4 = vf.com()

    b1 = vf.com()
    b2 = vf.com()
    b3 = vf.com()
    b4 = vf.com()

    rel_factor(
        vf,
        p, a1, a2, a3, a4,
        q, b1, b2, b3, b4,
        N
    )

    vf.finalize()
    return N

if __name__ == '__main__':
    out({
        'type': 'hello',
        'message': 'Welcome to Kalmar consolidated proof systems.'
    })
    try:
        N = check_proof(inp())
        out({
            'type': 'success',
            'flag': FLAG if N == NUMBER else 'great job m8, but not quite'
        })
    except Exception as e:
        out({
            'type': 'error',
            'message': 'Looks like a bad proof to me: ' + str(e)
        })
