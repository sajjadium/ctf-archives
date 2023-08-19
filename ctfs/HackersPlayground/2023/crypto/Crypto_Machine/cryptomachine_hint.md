Practical RSA implementation can be vulnerable to cache leaks of memory access pattern to d_p and d_q because of a common Power-By-Modulo optimization -- Fixed-Window Exponentiation.
You have gained an insight for a part of algorithm's implementation, which can leak memory access.

```
def get_exponent_digit_value(i: int):

    value = digits_i_to_value[E[i]]
    return value


def pow_mod(B, E, M):

    global omega

    # split exponent into digits
    init_exponent(E, omega)

    # pre-computations 
    b = []
    b.append(1)
    for j in range(1, 2 ** omega):
        b.append(b[j-1] * B % M)

    # exponentiation
    r = 1
    digits_count = (E.bit_length() + omega - 1) // omega
    for i in reversed(range(0, digits_count)):
        for j in range(0, omega):
            r = r * r % M
        r = r * b[get_exponent_digit_value(i)] % M
    
    return r


def rsaChineseReminderTheorem(text: int, p: int, q: int, d_p: int, d_q: int, q_inv: int):

    m_p = pow_mod(text, d_p, p)
    m_q = pow_mod(text, d_q, q)
    h   = q_inv * (m_p - m_q) % p
    return m_q + h * q
```