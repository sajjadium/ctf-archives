#include <stdio.h>
#include <stdint.h>

uint64_t num;

void vuln() {
	char buf[64];
	puts("Give me some text.");
	fgets(buf, sizeof(buf), stdin);
	printf("You typed ");
	printf(buf);
	printf("!\n");
}

/* You don't need to understand how this works
 *
 * In case you're curious, this loads the pointer guard from the TCB. This
 * value was chosen because it is randomized and can be accessed without
 * following any pointer chains in this object's memory. */
#define LOAD_SECRET(x) \
	__asm__ volatile ( \
		"mov %%fs:0x30, %0;" \
		: "=r" (x) \
	)

/* Check that only the lower byte of `num` has been changed to 0x42, and other
 * 7 bytes are unmodified - if so, print the flag. */
void check_num() {
	uint64_t goal;
	LOAD_SECRET(goal);
	__asm__ volatile (
		"mov $0x42, %b0;"
		: "+r" (goal)
	);
	if (num != goal) {
		puts("Nope, try again");
	} else {
		puts("Congrats! here's your flag");
		char flagbuf[64];
		FILE* f = fopen("./flag.txt", "r");
		fgets(flagbuf, sizeof(flagbuf), f);
		fclose(f);
		puts(flagbuf);
	}
}

int main() {
	/* disable stdout buffering */
	setvbuf(stdout, NULL, _IONBF, 0);

	LOAD_SECRET(num);
	/* clear the low byte - that way there is no random chance of
	 * getting the flag without doing anything */
	__asm__ volatile (
		"mov $0, %b0;"
		: "+r" (num)
	);

	vuln();

	check_num();

	return 0;
}
