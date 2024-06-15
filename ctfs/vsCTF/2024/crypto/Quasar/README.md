Ireland's challenge from dice '22 "learning-without-errors" was pretty cool. Apparently noise-flooding is the countermeasure for Li-Miccancio's attack on the INDCPA-D of CKKS. Kinda winged this fix, surely nothing could go wrong implementing this?

Note: py-fhe has been modified in this challenge. The modifications are as follows:

    Errors are now gaussian (this makes proofs way easier than uniform/triangular random)
    Keys are now generated with error respective to the modulus size, not always a choice of {-1,0,1}.

These patches are meant to make the library more secure/hard to cheese, and easier to work with. The rest should be pretty much the same. Given this information (or even without to be honest), it should not be required to read the modified library to solve this challenge, or diff, however reading this is a great way to learn CKKS. As far as I know, the modified library used here is bug-free, and the intended does not exploit any part of this modified library, but rather it's usage in server.py/processor.py/challenge.py. If you have any further questions as to the modifications of the library, please open a ticket and assuming it doesn't spoil anything, I'll be happy to answer, as reading a whole library is a pain.
