import numpy as np
from Pyfhel import Pyfhel
from tqdm import tqdm
from scipy.stats import special_ortho_group

num_levels = 9
qi_sizes = [60] + [30] * num_levels + [60]

HE = Pyfhel()           # Creating empty Pyfhel object
ckks_params = {
    'scheme': 'CKKS',   # can also be 'ckks'
    'n': 2**14,         # Polynomial modulus degree. For CKKS, n/2 values can be
                        #  encoded in a single ciphertext. 
                        #  Typ. 2^D for D in [10, 16]
    'scale': 2**30,     # All the encodings will use it for float->fixed point
                        #  conversion: x_fix = round(x_float * scale)
                        #  You can use this as default scale or use a different
                        #  scale on each operation (set in HE.encryptFrac)
    'qi_sizes': qi_sizes # Number of bits of each prime in the chain. 
                        # Intermediate values should be  close to log2(scale)
                        # for each operation, to have small rounding errors.
}
HE.contextGen(**ckks_params)  # Generate context for ckks scheme
HE.keyGen()             # Key Generation: generates a pair of public/secret keys
HE.rotateKeyGen()
HE.relinKeyGen()

# ----------------------------------------

def get_random_matrix():
    w = 2.0
    s = special_ortho_group.rvs(m)
    e = np.random.random(m)
    e *= (np.log2(w) - np.log2(1/w))
    e = 1/w * pow(2, e)
    e *= np.random.choice([-1,1], m)
    e = np.diag(e)
    A = s @ e @ s.T
    return A

n = 2**14
slots = n // 2
m = 8
num_mtx = slots // (m*m)

matx = [get_random_matrix() for i in tqdm(range(num_mtx))]
matx = np.array(matx, dtype=np.float64)
ptxt_x = matx.ravel()

ctxt_x = HE.encryptFrac(ptxt_x)

dir_name = "data"
HE.save_context(dir_name + "/context")
HE.save_public_key(dir_name + "/pub.key")
HE.save_secret_key("sec.key")
HE.save_relin_key(dir_name + "/relin.key")
HE.save_rotate_key(dir_name + "/rotate.key")
ctxt_x.save(dir_name + "/c.ctxt")


"""
Note:
the Pyfhel documentation isn't very clear on this, but after each homomorphic multiplication you perform, you'll want to do:
    x = a * b
    x = ~x # relinearize
    x = HE.rescale_to_next(x) # rescale

This prevents the scale factor from increasing, which would otherwise reduce the number of multiplications you can perform
"""

