#!/usr/bin/sage
from sage.all import GF, EllipticCurve, PolynomialRing
import hashlib
import json
import sys
import re

# curve and fields
p = 7691
field_size = 641
Fp = GF(field_size)
Fq = GF(p)
Eq = EllipticCurve(Fq, [0, 1])
Fqr = Fq['r']
r = Fqr.gen()
Fq_2 = GF(p**2, modulus=r**2 + 1, name='v')
v = Fq_2.gen()
ExtEq = EllipticCurve(Fq_2, [0, 1])

# set generators
G1 = ExtEq([2693, 4312])
G2 = ExtEq(633*v + 6145, 7372*v + 109)
assert G1.order() == field_size
assert G2.order() == field_size

# generate toxic values
tau = Fp.random_element(Fp)
alpha = Fp.random_element(Fp)
beta = Fp.random_element(Fp)
gamma = Fp.random_element(Fp)
delta = Fp.random_element(Fp)

# crs
CRS1 = [tau**i * G1 for i in range(7)]
CRS2 = [tau**i * G2 for i in range(4)]
CRSTrap1 = [alpha * G1, beta * G1, delta * G1]
CRSTrap2 = [beta * G2, gamma * G2, delta * G2]

def commit(poly, CRS):
    coeffs = poly.list()
    degree = poly.degree()
    com = ExtEq([0, 1, 0])  # point at infinity
    for i in range(min(degree + 1, len(CRS))):
        com += coeffs[i] * CRS[i]
    return com

def point_to_str(point):
    if point.is_zero():
        return "O"
    return f"({point[0]}, {point[1]})"

# convert string to point with field checks
def str_to_point(point_str):
    if point_str == "O":
        return ExtEq([0, 1, 0])

    coords = point_str.strip("()").split(",")
    if len(coords) != 2:
        raise ValueError("Invalid point format")

    # parse extension field point first (contains 'v')
    x_str = coords[0].strip()
    y_str = coords[1].strip()

    if 'v' in x_str or 'v' in y_str:
        try:
            x_coord = None
            y_coord = None

            if '*v +' in x_str:
                if not re.match(r'^-?\d+\*v \+ -?\d+$', x_str):
                    raise ValueError(f"Invalid extension field format: {x_str}")

                x_parts = x_str.split('*v +')
                try:
                    x_coeff1 = int(x_parts[0].strip())
                    x_coeff2 = int(x_parts[1].strip())
                    if not (0 <= x_coeff1 < p and 0 <= x_coeff2 < p):
                        raise ValueError("Coefficient out of field range")
                    x_coord = x_coeff1*v + x_coeff2
                except ValueError:
                    raise ValueError(f"Invalid integer in extension field: {x_str}")

            elif '*v' in x_str:
                if not re.match(r'^-?\d+\*v$', x_str):
                    raise ValueError(f"Invalid extension field format: {x_str}")

                x_parts = x_str.split('*v')
                try:
                    x_coeff = int(x_parts[0].strip())
                    if not (0 <= x_coeff < p):
                        raise ValueError("Coefficient out of field range")
                    x_coord = x_coeff*v
                except ValueError:
                    raise ValueError(f"Invalid integer in extension field: {x_str}")

            elif re.match(r'^-?\d+$', x_str):
                try:
                    x_int = int(x_str)
                    if not (0 <= x_int < p):
                        raise ValueError("Value out of field range")
                    x_coord = Fq_2(x_int)
                except ValueError:
                    raise ValueError(f"Invalid integer: {x_str}")
            else:
                raise ValueError(f"Unrecognized format for x-coordinate: {x_str}")

            if '*v +' in y_str:
                if not re.match(r'^-?\d+\*v \+ -?\d+$', y_str):
                    raise ValueError(f"Invalid extension field format: {y_str}")

                y_parts = y_str.split('*v +')
                try:
                    y_coeff1 = int(y_parts[0].strip())
                    y_coeff2 = int(y_parts[1].strip())
                    if not (0 <= y_coeff1 < p and 0 <= y_coeff2 < p):
                        raise ValueError("Coefficient out of field range")
                    y_coord = y_coeff1*v + y_coeff2
                except ValueError:
                    raise ValueError(f"Invalid integer in extension field: {y_str}")

            elif '*v' in y_str:
                if not re.match(r'^-?\d+\*v$', y_str):
                    raise ValueError(f"Invalid extension field format: {y_str}")

                y_parts = y_str.split('*v')
                try:
                    y_coeff = int(y_parts[0].strip())
                    if not (0 <= y_coeff < p):
                        raise ValueError("Coefficient out of field range")
                    y_coord = y_coeff*v
                except ValueError:
                    raise ValueError(f"Invalid integer in extension field: {y_str}")

            elif re.match(r'^-?\d+$', y_str):
                try:
                    y_int = int(y_str)
                    if not (0 <= y_int < p):
                        raise ValueError("Value out of field range")
                    y_coord = Fq_2(y_int)
                except ValueError:
                    raise ValueError(f"Invalid integer: {y_str}")
            else:
                raise ValueError(f"Unrecognized format for y-coordinate: {y_str}")

            point = ExtEq([x_coord, y_coord])
            return point

        except Exception as e:
            raise ValueError(f"Invalid extension field point: {point_str}. Error: {str(e)}")
    else:
        if not (re.match(r'^-?\d+$', x_str) and re.match(r'^-?\d+$', y_str)):
            raise ValueError(f"Invalid coordinate format: ({x_str}, {y_str})")

        try:
            x_int = int(x_str)
            y_int = int(y_str)

            if not (0 <= x_int < p and 0 <= y_int < p):
                raise ValueError("Coordinate out of field range")

            x_coord = Fq(x_int)
            y_coord = Fq(y_int)

            point = ExtEq([x_coord, y_coord])
            return point
        except Exception as e:
            raise ValueError(f"Invalid field point: {point_str}. Error: {str(e)}")

def verify_proof(L_point, R_point, Q_point, A_point, B_point, C_point):
    left_pairing = A_point.weil_pairing(B_point, field_size)
    right_pairing = (CRSTrap1[0].weil_pairing(CRSTrap2[0], field_size) * 
                      C_point.weil_pairing(CRSTrap2[2], field_size))
    return left_pairing == right_pairing

# generate challenge with L, R s.t. L*R != Q
def generate_challenge():
    Rng = PolynomialRing(Fp, 'x')
    
    # create L/R polynomials
    L_poly = Rng.random_element(degree=3)
    R_poly = Rng.random_element(degree=3)
    
    # ensure L*R != Q
    true_Q_poly = L_poly * R_poly
    fake_Q_poly = true_Q_poly + Rng.random_element(degree=1)
    while fake_Q_poly == true_Q_poly:
        fake_Q_poly = true_Q_poly + Rng.random_element(degree=1)
    
    # commitments
    L_commit = commit(L_poly, CRS1)
    R_commit = commit(R_poly, CRS2)
    Q_commit = commit(fake_Q_poly, CRS1)
    
    return {
        "L": point_to_str(L_commit),
        "R": point_to_str(R_commit), 
        "Q": point_to_str(Q_commit)
    }

print(f"delta :o : {int(delta)}")
rounds_passed = 0
total_rounds = 32

while rounds_passed < total_rounds:
    challenge = generate_challenge()
    print(f"\nRound {rounds_passed + 1}/{total_rounds}")
    print(json.dumps(challenge))
    
    try:
        response = json.loads(input())
        
        # parse proof
        A_point = str_to_point(response["proof"]["A"])
        B_point = str_to_point(response["proof"]["B"])
        C_point = str_to_point(response["proof"]["C"])
        
        # get chall commitments
        L_point = str_to_point(challenge["L"])
        R_point = str_to_point(challenge["R"])
        Q_point = str_to_point(challenge["Q"])
        
        if verify_proof(L_point, R_point, Q_point, A_point, B_point, C_point):
            rounds_passed += 1
            print(f"Verified! {rounds_passed}/{total_rounds}")
        else:
            print("Stupid :)")
    except Exception as e:
        print(f"Error: {e}")

if rounds_passed >= total_rounds:
    with open("flag.txt", "r") as f:
        flag = f.read().strip()
    print(f"Flag: {flag}")
