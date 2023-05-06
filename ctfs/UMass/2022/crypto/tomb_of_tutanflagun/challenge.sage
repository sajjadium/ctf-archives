#!/usr/bin/env python3
#
# Polymero
#

#
# We finally uncovered the Tomb of Tutanflagun! Can you help us excavate the flag?
#
#                                      \_m_/
#                  ~~~~|               /MMM\
#                  ~~~~|                3+E
# _____                |     _____       |
#      \___   __       |____/     \______|__
#  .       \_/ /_ _ __/   .      .          \_____
#      .      /|   |\                          .  \____ 
#            /_|_ _|_\  .                         
#         . /|   |   |\                              .      
#    .     /_|___|___|_\             .               
#         /|   |   |   |\                                                       
#        /_|___|___|___|_\                  .             
# .     /|   |   |   |   |\ .                  .                               
#     ./_|___|___|___|___|_\         .                    
#     /|   |   |   |   |   |\                             
#    /_|___|___|___|___|___|_\      .               .   
#            .              .                  .
#

ALP = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}!?"

FLAG = [ALP.index(i) for i in "flag{___REDACTED___}"]

class Pyramid:
    def __init__(self):
        self.Z = GF(67)
        self.n = [1,2,3,4,5]
        self.layers = { i : Matrix(self.Z, i, i, [FLAG.pop(0) for _ in range(i*i)]) for i in self.n }
        
    def _round(self, layer, msg):
        m = layer.base_ring().cardinality()
        n = layer.ncols()
        assert not msg.nrows() % n
        msgmat = Matrix(GF(m), msg.nrows() // n, n, msg.list()).T
        cipmat = (layer * msgmat).T
        return Matrix(GF(m), cipmat.list()).T
    
    def encrypt(self, msg):
        cip = msg
        for n in self.n:
            cip = self._round(self.layers[n], cip)
        return cip

pyra = Pyramid()

message = (pyra.Z^420).random_element().column()
print('message =', ''.join(ALP[i] for i in message.T.list()))

hierocipher = pyra.encrypt(message)
print('hierocipher =', ''.join(ALP[i] for i in hierocipher.T.list()))

#
# message = zptLKTGlJ2r{6nZlMvaMj8AT1zAzlsGqdORn6JVc14JmB?RnT5IXB6Ce?bJ{B8}ty_nHL{k{wR?bCMTqLnnqA_It}7a8XX3QwBFExeZ3}Y?w1!3LHVcVXQS_OS}crc01cuwFG{czY!FRgarAl{9NhcS3Xsoye7AH!B3q{Seeh578R!h4x7?62pE9TA9x8{oGgdX0Uv_W9wJO9Sh9zPbGog3zYwolBL2zOxzoXrf4ZJ0PF{HUYA{kGkL05W2zZKWny3H?y8i85X8Ib_L08csX5V73s77ptrMEYWI5JSa6Crb!qj!eoZK}CLQyRmNBMCSd2IOwy_zYIBN{h22LEVjSvdS5CU!bA!2LvBxWLpO!_!zmbhCXEadPVmIRVqPsZ!EwuFUZH_oKg5TgRm{A4EhT{e7IJn3H1cZ_Zsu}
# hierocipher = QpFKc9fZ1e0LKFbHjDgMf8CDO7?2p0b5XqZxyFUQ6TRYOc3g8w9Ph7nQCCe3asZXeqoDW9QZXWkAR}qgWXiEVH?d{gurMH1meQ6XPwLi7L!pARz1mJ2wVg5irFxWj{op5tLOI_CN0o857S3dpKi9dJGAu47heF23VBXmRHtEKxk5c_h3WKL33Rklcaxa14!Bf3e8iXW8TX0S7flhmvm0o9gGEZvPP!dp4GNVeuf0k1?rX7nW?2VZWmocQNf}mWGpQisETDyLEK1uYM1NqqW2YqfBOFI2gQK9Mr5uBUlCx2HzB8N!N{3GH{vLZ0S5Jo}17k8yidBibec}OfgSkHXbKQWZaMIU}6XvmDj_TbbdAMP15}YmwwAwZA64P6fHJ1PRSlFBtoTzNFMhe6TiPCwAonDWp_c8l8J}Ay3Y
#