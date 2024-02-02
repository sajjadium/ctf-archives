import pyhelayers
import numpy as np

n = 16384
requirement = pyhelayers.HeConfigRequirement(
    num_slots = n, # Number of slots per ciphertext
    multiplication_depth = 12, # Allow x levels of multiplications
    fractional_part_precision = 50, # Set the precision to 1/2^x
    integer_part_precision = 10, # Set the largest number to 2^x
    security_level = 128)

he_context = pyhelayers.HeaanContext()
he_context.init(requirement)

# Create the Encoder using the context.
encoder = pyhelayers.Encoder(he_context)

he_context.save_to_file("public.key")
he_context.save_secret_key_to_file("private.key")

cutoff = 0.02
x = np.random.uniform(-1, 1, n)
x = np.copysign(np.abs(x) + cutoff, x)  / (1 + cutoff)
cx = encoder.encode_encrypt(x)
cx.save_to_file("x_hard.ctxt")
