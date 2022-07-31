# **************************************************************#
# 		                 Redacted information:			        #	
# 			                 flag, n, M				            #
# **************************************************************#

def check(M):
  m = (M^n).n() - identity_matrix(2)

  if m[0,0]^2+m[0,1]^2+m[1,0]^2+m[1,1]^2 < 0.00001:
    return

  print("An error has occured. Please contact an admin about this.")
  quit()


def coefficients(m, length):
  seq = [m]

  while len(seq) < length:
    seq.append(seq[-1]*m)

  return seq


def encrypt(M, m, flag):
  m = coefficients(m, len(flag))

  s = identity_matrix(2)

  for c, a in zip(flag, m):
    s *= M^(c*a)

  return s.n()

def main():
  check(M)
  print("Hello! Welcome to Argand-Noether encryption oracle!")
  print(M.n())

  while True:
    m = int(input("\nPlease input a number m: "))
    enc = encrypt(M, m, flag)
    print(f"Under {m}, the flag gets encrypted to")
    print(enc)


if __name__ == "__main__":
  main()
