#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv) {
	char input[24];
	char filename[24] = "\0";
	char buffer[128];
	FILE* f = NULL;
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 2, 0);
	if (argc > 1) {
		strncpy(filename, argv[1], 23);
	}
	while (1) {
		fgets(input, 128, stdin);
		input[strcspn(input, "\n")] = 0;
		if (input[0] == 'Q') {
			return 0;
		} else if (input[0] == 'f') {
			if (strlen(input) >= 3) {
				strcpy(filename, input + 2);
			}

			if (filename[0] == '\0') {
				puts("?");
			} else {
				puts(filename);
			}
		} else if (input[0] == 'l') {
			if (filename[0] == '\0') {
				puts("?");
			} else {
				if (strchr(filename, '/') != NULL) {
					puts("?");
					continue;
				}

				f = fopen(filename, "r");
				if (f == NULL) {
					puts("?");
					continue;
				}

				while (fgets(buffer, 128, f)) {
					printf("%s", buffer);
				}
				fclose(f);
			}
		} else {
			puts("?");
		}
	}
}
