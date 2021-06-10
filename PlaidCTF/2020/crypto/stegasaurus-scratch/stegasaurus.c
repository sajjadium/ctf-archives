// lua 5.3 has integer division

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>

#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

const int trials = 10000;
const int deck_size = 40000;
const int hand_size = 8;
const int timeout = 10;

FILE* urand;
lua_State *Alice, *Bob;
char fp[0x100] = {0};

bool getfile() {
	puts("send your file");
	unsigned char randchars[17];
	fread(randchars, sizeof(unsigned char), 16, urand);
	for (int i = 0; i < 16; i++) randchars[i] = randchars[i] % 26 + 'a';
	randchars[16] = 0;
	sprintf(fp, "tries/%s.lua", randchars);
	FILE* writefile = fopen(fp, "w");
	if (!writefile) return false;
	char buff[0x100];
	size_t amt;
	while ((amt = fread(buff, sizeof(char), 0x100, stdin)) > 0) {
		fwrite(buff, 1, amt, writefile);
	}
	fclose(writefile);
	return true;
}

bool part1_checkonce() {
	// Deal a hand
	int deck[deck_size];
	for (int i = 0; i < deck_size; i++) deck[i] = i + 1;

	int hand[hand_size];
	for (int i = 0; i < hand_size; i++) {
		unsigned int card;
		fread(&card, sizeof(unsigned int), 1, urand);
		card %= deck_size - i;
		card += i;
		hand[i] = deck[card];
		// Swap cards in deck so no reuse
		deck[card] = deck[i];
		deck[i] = hand[i];
	}

	// Send the hand to Alice
	lua_getglobal(Alice, "Alice1");
	lua_createtable(Alice, hand_size, 0);
	for (int i = 0; i < hand_size; i++) {
		lua_pushinteger(Alice, (lua_Integer)hand[i]);
		lua_rawseti(Alice, -2, i+1);
	}
	lua_call(Alice, 1, 1);
	
	// Get Alice's response
	int alices[hand_size - 1];
	for (int i = 0; i < hand_size - 1; i++) {
		lua_rawgeti(Alice, -1, i+1);
		alices[i] = lua_tointeger(Alice, -1);
		lua_pop(Alice, 1);
	}

	// Check Alice's response
	bool used[hand_size];
	for (int i = 0; i < hand_size; i++) used[i] = false;

	for (int i = 0; i < hand_size - 1; i++) {
		// All returned values need to be unique
		for (int j = i+1; j < hand_size - 1; j++) {
			if (alices[i] == alices[j]) return false;
		}
		// and in what we gave Alice
		bool found = false;
		for (int j = 0; j < hand_size; j++) {
			if (alices[i] == hand[j]) {
				used[j] = true;
				found = true;
				break;
			}
		}
		if (!found) return false;
	}
	lua_pop(Alice, 1);

	int discarded;
	for (int i = 0; i < hand_size; i++) {
		if (!used[i]) {
			discarded = hand[i];
			break;
		}
	}

	// Send the hand to Bob
	lua_getglobal(Bob, "Bob1");
	lua_createtable(Bob, hand_size-1, 0);
	for (int i = 0; i < hand_size - 1; i++) {
		lua_pushinteger(Bob, (lua_Integer)alices[i]);
		lua_rawseti(Bob, -2, i+1);
	}
	lua_call(Bob, 1, 1);

	// Check Bob's response
	int guess = lua_tointeger(Bob, -1);
	lua_pop(Bob, 1);

	return guess == discarded;
}

bool part2_checkonce() {
	// Set up the table
	int table[96];
	for (int i = 0; i < 64; i++) table[i] = 1;
	for (int i = 64; i < 96; i++) table[i] = 2;
	// Shuffle the table
	for (int i = 0; i < 96; i++) {
		unsigned int swap;
		fread(&swap, sizeof swap, 1, urand);
		swap %= 96 - i;
		int tmp = table[i];
		table[i] = table[i+swap];
		table[i+swap] = tmp;
	}

	// Send the table to Alice
	lua_getglobal(Alice, "Alice2");
	lua_createtable(Alice, 96, 0);
	for (int i = 0; i < 96; i++) {
		lua_pushinteger(Alice, (lua_Integer)table[i]);
		lua_rawseti(Alice, -2, i+1);
	}
	lua_call(Alice, 1, 1);

	// Get Alice's response
	for (int i = 0; i < 32; i++) {
		lua_rawgeti(Alice, -1, i+1);
		int rem = lua_tointeger(Alice, -1) - 1;
		if (!(0 <= rem && rem < 96)) return false;
		if (table[rem] != 1) return false;
		table[rem] = 0;
		lua_pop(Alice, 1);
	}
	lua_pop(Alice, 1);

	// Send the table to Bob
	lua_getglobal(Bob, "Bob2");
	lua_createtable(Bob, 96, 0);
	for (int i = 0; i < 96; i++) {
		int present = table[i] == 0 ? 0 : 1;
		lua_pushinteger(Bob, (lua_Integer)present);
		lua_rawseti(Bob, -2, i+1);
	}
	lua_call(Bob, 1, 1);

	// Get Bob's response

	for (int i = 0; i < 32; i++) {
		lua_rawgeti(Bob, -1, i+1);
		int guess = lua_tointeger(Bob, -1) - 1;
		if (!(0 <= guess && guess < 96)) return false;
		if (table[guess] != 2) return false;
		table[guess] = 0;
		lua_pop(Bob, 1);
	}
	lua_pop(Bob, 1);

	return true;
}

bool trial() {
	printf("running part 1... ");
	for (int i = 0; i < trials; i++) {
		if (!part1_checkonce()) return false;
	}
	printf("passed\nrunning part 2... ");
	for (int i = 0; i < trials; i++) {
		if (!part2_checkonce()) return false;
	}
	printf("passed\n");
	return true;
}

bool run() {
	// Create two instances of the code, one for all of Alice's handling
	// and the other for all of Bob's
	Alice = luaL_newstate(); Bob = luaL_newstate();

	// Give them table and math stdlibs
	luaL_requiref(Alice, LUA_TABLIBNAME, luaopen_table, 1); lua_pop(Alice, 1);
	luaL_requiref(Alice, LUA_MATHLIBNAME, luaopen_math, 1); lua_pop(Alice, 1);
	luaL_requiref(Bob, LUA_TABLIBNAME, luaopen_table, 1); lua_pop(Bob, 1);
	luaL_requiref(Bob, LUA_MATHLIBNAME, luaopen_math, 1); lua_pop(Bob, 1);

	if (luaL_dofile(Alice, fp)) return false;
	if (luaL_dofile(Bob, fp)) return false;

	bool won = trial();
	lua_close(Alice); lua_close(Bob);
	return won;
}

int main(void) {
	setvbuf(stdout, NULL, _IONBF, 0);
	urand = fopen("/dev/urandom", "r");
	if (!urand) return 0;
	//alarm(timeout);
	if (getfile()) {
		if (run()) {
			system("cat flag.txt");
		} else {
			puts("failed");
		}
	}
	fclose(urand);
	return 0;
}

