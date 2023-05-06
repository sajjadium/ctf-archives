#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/mman.h>

struct profile {
	char name[0x100];
	long long *friends; //some people have a lot of friends
};

struct profile *user;
int uid;

void login() {
	printf("Please enter your user ID: ");
	scanf(" %d", &uid);
	getchar();

	char file[50];
	char c;
	sprintf(file, "users/%d", uid);
	if (access(file, F_OK) != -1) {
		puts("Before you log back in, please complete a brief survey.");
		puts("For each of the following categories, rate us from 1-10.");
		char survey[20];
		int n = 0;
		printf("Content: ");
		n += read(1, survey+n, 3);
		printf("Moderation: ");
		n += read(1, survey+n, 3);
		printf("Interface: ");
		n += read(1, survey+n, 3);
		printf("Support: ");
		n += read(1, survey+n, 3);
		survey[n] = 0;
		if (strchr(survey, 'n') != NULL) {
			//a bug bounty report said something about hacking and the letter n
			puts("ERROR: HACKING DETECTED");
			puts("Exiting...");
			exit(1);
		}
		if (strcmp(survey, "10\n10\n10\n10\n") != 0) {
			puts("Those ratings don't seem quite right. Please review them and try again:");
			printf(survey);
			n = 0;
			printf("Content: ");
			n += read(1, survey+n, 3);
			printf("Moderation: ");
			n += read(1, survey+n, 3);
			printf("Interface: ");
			n += read(1, survey+n, 3);
			printf("Support: ");
			n += read(1, survey+n, 3);
			survey[n] = 0;
		}
		user = mmap(rand()&0xfffffffffffff000, sizeof (struct profile), PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED, -1, 0);
		FILE *f = fopen(file, "rb");
		fread(user, 1, sizeof (struct profile), f);
		fclose(f);
		if (strcmp(survey, "10\n10\n10\n10\n") != 0) {
			puts("Our survey says... you don't seem very nice. I doubt you have any friends!");
			*(user->friends) = 0;
		}
	} else {
		puts("Welcome to bookface!");
		user = mmap(rand()&0xfffffffffffff000, sizeof (struct profile), PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED, -1, 0);
		printf("What's your name? ");
		fgets(user->name, 0x100, stdin);
	}
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	srand(time(NULL));
	
	login();

	char file[50];

	while (1) {
		printf("You have %lld friends. What would you like to do?\n", user->friends);
		puts("[1] Make friends");
		puts("[2] Lose friends");
		puts("[3] Delete account");
		puts("[4] Log out");
		printf("> ");
		switch (getchar()) {
			case '1':
				printf("How many friends would you like to make? ");
				long long new;
				scanf(" %lld", &new);
				user->friends += new;
				break;
			case '2':
				printf("How many friends would you like to lose? ");
				long long lost;
				scanf(" %lld", &lost);
				user->friends -= lost;
				break;
			case '3':
				puts("Deleting account...\n");
				sprintf(file, "users/%d", uid);
				remove(file);
				login();
				continue;
			case '4':
				puts("Logging out...\n");
				sprintf(file, "users/%d", uid);
				FILE *f = fopen(file, "wb");
				fwrite(user, 1, sizeof (struct profile), f);
				fclose(f);
				login();
				continue;
			case '\n':
				continue;
		}
		getchar();
	}
}
