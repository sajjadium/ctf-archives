#include <stdio.h>
#include <stdlib.h>

struct hoop {
	char depth[61];
	int hoop;
	char depth2[19];
};

int main() {
	setvbuf(stdin, 0, _IONBF, 0);
	setvbuf(stdout, 0, _IONBF, 0);
	setvbuf(stderr, 0, _IONBF, 0);
	char name[24];

	printf("Welcome to the narrow end of the pool\n");
	printf("How old are you\n");
	unsigned long ans = 0;
	scanf("%li", &ans);
	if(ans <= 0 || (int)ans > 0) {
		printf("Tough luck... too young and too old\n");
		exit(1);
	}
	printf("Ok sport, take your first dive into the water\n");
	scanf("%lu", &ans);
	if(*((double *)(&ans)) != 1) { 
		printf("Drowned in the depths\n");
		exit(1);
	}
	printf("Swim through the hoop!\n");	
	struct hoop *target = calloc(1, sizeof(struct hoop));
	target->hoop = 1;
	scanf("%lu", &ans);
	if(!*((char *)(target)+ ans)) {
		printf("Ouch!\n");
		exit(1);
	}
	printf("That's pretty good! Now make your own course\n");
	scanf(" %88s", (char *)target);
	if(target->hoop != ((0x12345678)^(0xfedcba98))-0xff) {
		printf("So close!\n");
		exit(1);
	}
	printf("Good Job!\n What should be on the medal?\n");
	scanf("%s", &name);
	printf("We hereby present %s with the flag for adequate swimming proficiency!\n", name);
	FILE *f = fopen("flag.txt", "r");
	fgets(name, 24, f);
	printf("%s\n", name);
}
