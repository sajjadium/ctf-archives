import math, json
from secrets import token_urlsafe
from Crypto.Util.number import isPrime, bytes_to_long, long_to_bytes

def main():
    try:
        # create token
        token = token_urlsafe(8)
        js = json.dumps({'token': token})
        
        # select primes
        print(f'Welcome to the RSA testing service. Your token is "{token}".')
        print('Please give me 128-bit primes p and q:')
        p = int(input('p='))
        assert isPrime(p) and p.bit_length() == 128, 'p must be a 128-bit prime'
        assert str(float(math.pi)) in str(float(p)), 'p does not look like a certain universal constant'
        q = int(input('q='))
        assert isPrime(q) and q.bit_length() == 128, 'q must be a 128-bit prime'
        assert str(float(math.e)) in str(float(q)), 'q does not look like a certain universal constant'

        # encode
        print('We will use e=65537 because it is good practice.')
        e = 65537
        m = bytes_to_long(js.encode())
        c = pow(m, e, p * q)

        # decode
        print('Now what should the corresponding value of d be?')
        d = int(input('d='))
        m = pow(c, d, p * q)
        
        # interpret as json
        js = json.loads(long_to_bytes(m).decode())
        assert js['token'] == token, 'Invalid token!'
        print('RSA test passed!')

        if 'flag' in js:
            from secret import flag
            print(flag)
    
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
