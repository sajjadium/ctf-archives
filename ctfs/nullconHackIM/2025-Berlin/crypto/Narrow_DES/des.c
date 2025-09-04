#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define LB32_MASK   0x00000000ffffffff
#define LB24_MASK   0x0000000000ffffff
#define ROUNDS 32

/* Post S-Box permutation */
static char P[] = {
	8, 18, 3, 2, 15, 24, 10, 14, 20, 7, 5, 13, 1, 6, 21, 9, 4, 11, 23, 22, 12, 19, 16, 17
};

/* The S-Box tables */
static char S[8][16] = {{
	5, 3, 0, 2, 7, 1, 4, 6,
	1, 6, 4, 7, 5, 0, 3, 2,
}, {
	4, 1, 0, 5, 3, 7, 6, 2,
	1, 4, 0, 5, 2, 6, 3, 7,
}, {
	3, 4, 2, 0, 7, 6, 1, 5,
	3, 7, 6, 0, 4, 2, 1, 5,
}, {
	5, 6, 4, 2, 7, 0, 3, 1,
	6, 5, 7, 2, 1, 3, 4, 0,
}, {
	5, 6, 7, 3, 1, 0, 4, 2,
	3, 6, 2, 1, 7, 4, 0, 5,
}, {
	0, 3, 1, 4, 6, 5, 2, 7,
	0, 3, 5, 4, 7, 6, 1, 2,
}, {
	6, 0, 4, 2, 3, 5, 1, 7,
	0, 6, 7, 3, 2, 1, 4, 5,
}, {
	0, 5, 6, 2, 3, 7, 4, 1,
	2, 4, 0, 7, 3, 1, 5, 6,
}};

uint64_t des(uint64_t msg, uint64_t key, char mode) {
	
	int i, j;
	
	uint32_t L        = 0;
	uint32_t R        = 0;
	uint32_t expanded = 0;
	uint32_t s_output = 0;
	uint32_t p_output = 0;
	uint32_t temp     = 0;
	
	uint32_t sub_key[2] = {0};
	
	L = (uint32_t)((msg >> 24) & LB24_MASK);
	R = (uint32_t)(msg & LB24_MASK);
	
	/* Calculation of the 16 keys */
	sub_key[0] = (uint32_t)(key >> 32);
	sub_key[1] = (uint32_t)(key & LB32_MASK);
	
	for (i = 0; i < ROUNDS; i++) {
		expanded = 0;
		for (j = 0; j < 7; j++) {
			expanded |= ((R >> (20 - 3*j)) & 0xf) << (28 - 4*j);
		}
		expanded |= (R & 7) << 1 | (R >> 23);
		
		if (mode == 'd') {
			expanded = expanded ^ sub_key[(i+1) % 2];
		} else {
			expanded = expanded ^ sub_key[i % 2];
		}
		
		s_output = 0;
		for (j = 0; j < 8; j++) {
			temp = (expanded >> (4*j)) & 0xf;
			s_output <<= 3;
			s_output |= (uint32_t) (S[j][temp]);
		}
		
		p_output = 0;
		for (j = 0; j < 24; j++) {
			p_output <<= 1;
			p_output |= (s_output >> (24 - P[j])) & 1;
		}
		
		temp = R;
		R = L ^ p_output;
		L = temp;
	}
	return ((uint64_t) L) << 24 | R;
}

int main(int argc, const char * argv[]) {
	char inputStr[769];
	uint64_t key = 0x00000000;
	printf("Give your message in hexadecimal.\n");
	fflush(stdout);
	uint64_t input, result;
	char msg[13];
	msg[12] = 0;
	while(1) {
		scanf("%768s" , inputStr);
		for(int i = 0; i < 64; i++) {
			memcpy(msg, inputStr + 12*i, 12);
			input = (uint64_t)strtoull(msg, NULL, 16);
			result  = des(input,  key, 'e');
			printf("%012lx", result);
		}
		printf("\n");
		fflush(stdout);
	}
	exit(0);
}
