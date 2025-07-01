import numpy as _
__ = 257
___ = 3
def ____(_____, ______): _______ = int(round(_.linalg.det(_____))) % ______; ________ = pow(_______, -1, ______); _________ = _.round(_______ * _.linalg.inv(_____)).astype(int) ;__________ = (________ * _________) % ______; return __________.astype(int)
def ___________(____________: bytes, _____________: int) -> bytes: ______________ = (_____________ - len(____________) % _____________) % _____________; return ____________ + bytes([0] * ______________)
def _______________(_________________: bytes, __________________: _.ndarray) -> _.ndarray: _________________ = ___________(_________________, __________________.shape[0]);____________________ = _.frombuffer(_________________, dtype=_.uint8).reshape(-1, __________________.shape[0]);return (____________________ @ __________________.T) % __
if __name__ == "__main__":
    flag = b"VERYSECRETFLAG"  
    while True:
        A = _.random.randint(1, __, (___, ___))
        try: ______________________ = ____(A, __);break
        except: continue
    encrypted = _______________(flag, A)
    print("A:\n " + repr(A.tolist()) + " \nencrypted:\n" + repr(encrypted.tolist()))