#!/usr/bin/env python3

import numpy as np
import binascii
import os, sys
from flag import FLAG

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc(): 
	return sys.stdin.buffer.readline()

def pad(inp, length):
	result = inp + os.urandom(length - len(inp))
	return result

def byte_xor(a, b):
	return bytes(_a ^ _b for _a,_b in zip(a,b)) 

def chaffy_mask(salt, LTC, m, n):
	q = n ** 2
	half1_salt = salt[:m // 8]
	half2_salt = salt[m // 8:]
	xor_salts = int.from_bytes(byte_xor(half1_salt, half2_salt), "big")

	if xor_salts == 0:
		half1_salt = byte_xor(half1_salt, os.urandom(m))
	half1_binStr = "{:08b}".format(int(half1_salt.hex(),16))
	if(len(half1_binStr) < m):
		half1_binStr = "0" * (m - len(half1_binStr)%m) + half1_binStr
	half2_binStr = "{:08b}".format(int(half2_salt.hex(),16))
	if(len(half2_binStr) < m):
		half2_binStr = "0" * (m - len(half2_binStr)%m) + half2_binStr
	
	vec_1 = np.array(list(half1_binStr), dtype=int)
	vec_1 = np.reshape(vec_1, (m,1))
	vec_2 = np.array(list(half2_binStr), dtype=int)
	vec_2 = np.reshape(vec_2, (m,1))
	
	out_1 = LTC.dot(vec_1) % q
	out_2 = LTC.dot(vec_2) % q
	
	flag_vector = np.array([ord(i) for i in FLAG])
	flag_vector = np.reshape(flag_vector, (n,1))
	masked_flag = (flag_vector ^ out_1 ^ out_2) % 256
	masked_flag = np.reshape(masked_flag, (n,))
	masked_flag = ''.join([hex(_)[2:].zfill(2) for _ in masked_flag])
	return masked_flag.encode('utf-8')

def main():
	border = "|"
	pr(border*72)
	pr(border, " Welcome to chaffymask combat, we implemented a masking method to   ", border)
	pr(border, " hide our secret. Masking is done by your 1024 bit input salt. Also ", border)
	pr(border, " I noticed that there is a flaw in my method. Can you abuse it and  ", border)
	pr(border, " get the flag? In each step you should send salt and get the mask.  ", border)
	pr(border*72)

	m, n = 512, 64 
	IVK = [
	3826, 476, 3667, 2233, 1239, 1166, 2119, 2559, 2376, 1208, 2165, 2897, 830, 529, 346, 150, 2188, 4025, 
	3667, 1829, 3987, 952, 3860, 2574, 959, 1394, 1481, 2822, 3794, 2950, 1190, 777, 604, 82, 49, 710, 1765, 
	3752, 2970, 952, 803, 873, 2647, 2643, 1096, 1202, 2236, 1492, 3372, 2106, 1868, 535, 161, 3143, 3370, 
	1, 1643, 2147, 2368, 3961, 1339, 552, 2641, 3222, 2505, 3449, 1540, 2024, 618, 1904, 314, 1306, 3173, 
	4040, 1488, 1339, 2545, 2167, 394, 46, 3169, 897, 4085, 4067, 3461, 3444, 118, 3185, 2267, 3239, 3612, 
	2775, 580, 3579, 3623, 1721, 189, 650, 2755, 1434, 35, 3167, 323, 589, 3410, 652, 2746, 2787, 3665, 828, 
	3200, 1450, 3147, 720, 3741, 1055, 505, 2929, 1423, 3629, 3, 1269, 4066, 125, 2432, 3306, 4015, 2350, 
	2154, 2623, 1304, 493, 763, 1765, 2608, 695, 30, 2462, 294, 3656, 3231, 3647, 3776, 3457, 2285, 2992, 
	3997, 603, 2342, 2283, 3029, 3299, 1690, 3281, 3568, 1927, 2909, 1797, 1675, 3245, 2604, 1272, 1146, 
	3301, 13, 3712, 2691, 1097, 1396, 3694, 3866, 2066, 1946, 3476, 1182, 3409, 3510, 2920, 2743, 1126, 2154, 
	3447, 1442, 2021, 1748, 1075, 1439, 3932, 3438, 781, 1478, 1708, 461, 50, 1881, 1353, 2959, 1225, 1923, 
	1414, 4046, 3416, 2845, 1498, 4036, 3899, 3878, 766, 3975, 1355, 2602, 3588, 3508, 3660, 3237, 3018, 
	1619, 2797, 1823, 1185, 3225, 1270, 87, 979, 124, 1239, 1763, 2672, 3951, 984, 869, 3897, 327, 912, 1826, 
	3354, 1485, 2942, 746, 833, 3968, 1437, 3590, 2151, 1523, 98, 164, 3119, 1161, 3804, 1850, 3027, 1715, 
	3847, 2407, 2549, 467, 2029, 2808, 1782, 1134, 1953, 47, 1406, 3828, 1277, 2864, 2392, 3458, 2877, 1851, 
	1033, 798, 2187, 54, 2800, 890, 3759, 4085, 3801, 3128, 3788, 2926, 1983, 55, 2173, 2579, 904, 1019, 
	2108, 3054, 284, 2428, 2371, 2045, 907, 1379, 2367, 351, 3678, 1087, 2821, 152, 1783, 1993, 3183, 1317, 
	2726, 2609, 1255, 144, 2415, 2498, 721, 668, 355, 94, 1997, 2609, 1945, 3011, 2405, 713, 2811, 4076, 
	2367, 3218, 1353, 3957, 2056, 881, 3420, 1994, 1329, 892, 1577, 688, 134, 371, 774, 3855, 1461, 1536, 
	1824, 1164, 1675, 46, 1267, 3652, 67, 3816, 3169, 2116, 3930, 2979, 3166, 3944, 2252, 2988, 34, 873, 
	1643, 1159, 2822, 1235, 2604, 888, 2036, 3053, 971, 1585, 2439, 2599, 1447, 1773, 984, 261, 3233, 2861, 
	618, 465, 3016, 3081, 1230, 1027, 3177, 459, 3041, 513, 1505, 3410, 3167, 177, 958, 2118, 326, 31, 2663, 
	2026, 2549, 3026, 2364, 1540, 3236, 2644, 4050, 735, 280, 798, 169, 3808, 2384, 3497, 1759, 2415, 3444, 
	1562, 3472, 1151, 1984, 2454, 3167, 1538, 941, 1561, 3071, 845, 2824, 58, 1467, 3807, 2191, 1858, 106, 
	3847, 1326, 3868, 2787, 1624, 795, 3214, 1932, 3496, 457, 2595, 3043, 772, 2436, 2160, 3428, 2005, 2597, 
	1932, 101, 3528, 1698, 3663, 900, 3298, 1872, 1179, 3987, 3695, 3561, 1762, 3785, 3005, 2574, 6, 1524, 
	2738, 1753, 2350, 558, 800, 3782, 722, 886, 2176, 3050, 221, 1925, 564, 1271, 2535, 3113, 1310, 2098, 
	3011, 964, 3281, 6, 1326, 741, 189, 2632, 373, 1176, 548, 64, 1445, 2376, 1524, 2690, 1316, 2304, 1336, 
	2257, 3227, 2542, 3911, 3460
	]

	LTC = np.zeros([n, m], dtype=(int))
	LTC[0,:] = IVK

	for i in range(1, n):
		for j in range(m // n + 1):
			LTC[i,j*n:(j+1)*n] = np.roll(IVK[j*n:(j+1)*n], i)

	for _ in range(5):
		pr(border, "Give me your salt: ")
		SALT = sc()[:-1]
		SALT = pad(SALT, m // 4)
		MASKED_FLAG = chaffy_mask(SALT, LTC, m, n)
		pr(border, f'masked_flag = {MASKED_FLAG}')

if __name__ == '__main__':
	main()