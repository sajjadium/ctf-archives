# Cube Cipher

The Cube Cipher is my own invention: A modern unbreakable cipher.

The Cube Cipher is a 27-character block cipher that works as follows:

1. The plaintext is padded to a 27-byte boundary with null bytes.

2. Each byte is brocken up into nibbles and each nibble is arranged on a Rubik's Cube in this order:

	 ```
	            18 19 20
	            21 22 23
	            24 25 26

	  27 28 29  00 01 02  09 10 11
	  30 31 32  03 04 05  12 13 14
	  33 34 35  06 07 08  15 16 17

	            36 37 38
	            39 40 41
	            42 43 44

	            45 46 47
	            48 49 50
	            51 52 53
	 ```
 
3. The cube is folded, shuffled according to a pre-selected "algorithm", and unwraveled into a new stream.

Someone who knows the algorithm can then reverse this by applying it in reverse.
