#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int userToken = 0;
int balance = 0;

int authorize () {
	userToken = 0x1337;
	return 0;
}

int addBalance (int pin) {
	if (userToken == 0x1337 && pin == 0xdeadbeef) {
		balance = 0x4242;
	} else {
		printf("ACCESS DENIED\n");
	}
	return 0;
}

int flag (int pin, int secret) {
	if (userToken == 0x1337 && balance == 0x4242 && pin == 0xba5eba11 && secret == 0xbedabb1e) {
		printf("Authenticated to purchase rope chain, sending free flag along with purchase...\n");
		system("/bin/cat flag.txt");
	} else {
		printf("ACCESS DENIED\n");
	}
	return 0;
}

void getInfo () {
	printf("Token: 0x%x\nBalance: 0x%x\n", userToken, balance);
}

int main() {
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	char name [32];
	printf("--== ROPE CHAIN BLACK MARKET ==--\n");
	printf("LIMITED TIME OFFER: Sending free flag along with any purchase.\n");
	printf("What would you like to do?\n");
	printf("1 - Set name\n");
	printf("2 - Get user info\n");
	printf("3 - Grant access\n");
	int choice;
	scanf("%d\n", &choice);
	if (choice == 1) {
		gets(name);
	} else if (choice == 2) {
		getInfo();
	} else if (choice == 3) {
		printf("lmao no\n");
	} else {
		printf("I don't know what you're saying so get out of my black market\n");
	}
	return 0;
}