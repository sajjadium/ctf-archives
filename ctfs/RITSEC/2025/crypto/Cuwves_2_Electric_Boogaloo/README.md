We've identified that this alien race communicates with futuristic quantum-resistant cryptographic protocols: their messages are encoded using elliptic curve isogeny walks. Our spies have intercepted a partial transmission, revealing a critical piece of their secret communication. We believe this information holds a secret code necessary to unlocking access to their base. Your mission is to reverse-engineer their isogeny walk and extract the hidden message!

The following cryptographic parameters were intercepted from the transmission:

Prime Field Modulus (p): 4049
Starting Supersingular Elliptic Curve: y^2 = x^3 + 3x + 1
Leaked Midpoint Curve: y^2 = x^3 + 243x + 729
Final Isogeny Kernel Generator: (0 : 1 : 0)

(all curves are over the finite field of size p^2)

The encryption process follows an l-isogeny walk across an isogeny volcano, using l=3 and a depth of n=4. By completing the isogeny walk and determining the final curve, you will recover the j-invariant, which serves as the secret key. The flag is RS{shared_j-invariant}
