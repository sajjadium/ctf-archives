from curves import WeierstrassCurve
from curves import AffinePoint

p = 0x8b782894f68da899544752baa0beaeec44301074481e8da13115595f588025ef
curveCSR2023 = WeierstrassCurve(0x5b93c3c0c5ac6aeb53be8996bab4db2b32982c73a145589cd6c40c816c35ec9b, 0x2bcf81f069098bb56f2158a9a3138cb3de8c3c50481fabf68bac88506b9f0646, p)

G = AffinePoint(
        curveCSR2023,
        0x27b20692e5533356329961cc5a576795a80c742bb81e62c177d73a37f1dca5d1, 0x5fd8eed995325760a1e443856871f34473509b61ef39e791f8186cb167dc74cd,
        0x8b782894f68da899544752baa0beaeec44301074481e8da13115595f588025ef
)

# If we do a scalar multiplication of the generators
# order with the generator point, we should end up
# at the neutral element, the point at infinity
X = G.order * G
assert(X == curveCSR2023.poif)

# Since the point at infinity is the neutral element,
# with order+1 we should en up at the generator.
X = (G.order + 1) * G
assert(X == G)
