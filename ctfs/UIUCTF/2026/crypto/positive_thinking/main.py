import tenseal as ts
import secrets
import os
import base64


FLAG = os.getenv("FLAG", "uiuctf{test}")


# ============================================================
# CKKS parameters
# ============================================================

POLY_MODULUS_DEGREE = 16384
COEFF_MOD_BIT_SIZES = [60, 40, 40, 40, 40, 40, 40, 60]
GLOBAL_SCALE = 2**40


# ============================================================
# Challenge parameters
# ============================================================

SECRET_BITS = 50
NORMALIZATION1 = 2**24
NORMALIZATION2 = 2**25
MAX_QUERIES = 100


# ============================================================
# Chebyshev polynomial T_8
#
#     T_8(x) = 128x^8 - 256x^6
#              + 160x^4 - 32x^2 + 1
#
# TenSEAL polyval expects coefficients in increasing
# order of degree.
# ============================================================

CHEBYSHEV8 = [
    1,
    0,
    -32,
    0,
    160,
    0,
    -256,
    0,
    128,
]


def chebyshev8(x):
    return x.polyval(CHEBYSHEV8)


# ============================================================
# FHE setup
# ============================================================

context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=POLY_MODULUS_DEGREE,
    coeff_mod_bit_sizes=COEFF_MOD_BIT_SIZES,
)

context.global_scale = GLOBAL_SCALE
context.generate_relin_keys()


# ============================================================
# Secret
# ============================================================

secret = secrets.randbelow(
    2**SECRET_BITS
)

encrypted_secret = ts.ckks_vector(
    context,
    [secret],
)


# ============================================================
# Publish public context
# ============================================================

public_context = context.copy()
public_context.make_context_public()

print("Public context:")
print(
    base64.b64encode(
        public_context.serialize()
    ).decode()
)

print("Encrypted value:")
print(
    base64.b64encode(
        encrypted_secret.serialize()
    ).decode()
)


# ============================================================
# Oracle
# ============================================================

for query in range(MAX_QUERIES):

    print(
        f"Query {query + 1}/{MAX_QUERIES}"
    )

    print("Serialized ciphertext:")

    try:
        blob = base64.b64decode(
            input("> ")
        )

        ciphertext = ts.ckks_vector_from(
            context,
            blob,
        )

        # Evaluate
        #
        #     T8(x / 2^49)
        #
        # on the submitted ciphertext.
        # 2^49 is split into 2^24 and 2^25 to avoid issues with the global scale

        normalized = ciphertext * (1.0 / NORMALIZATION1) * (1.0 / NORMALIZATION2)

        result = (
            chebyshev8(normalized)
            .decrypt()[0]
        )

    except Exception:
        print("Invalid ciphertext")
        continue

    print(
        "Positive"
        if result > 0
        else "Not positive"
    )

    guess = int(
        input("Secret: ")
    )

    if guess == secret:
        print(FLAG)
        raise SystemExit

    print("Keep trying!")


print("Maybe next time?")