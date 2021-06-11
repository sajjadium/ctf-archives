#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void flag() {
	FILE *file;
	file = fopen("flag.txt", "r");
	int c;
	while ((c = getc(file)) != EOF) {
		putchar(c);
	}
	fclose(file);
}

int main() {
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	char cells[256] = {0};
	char code[144];
	printf("enter some brainf code: ");
	fgets(code, sizeof(code), stdin);
	int balance = 0;
	for (int i=0; i<strlen(code); i++) {
		if (code[i] == '[') {
			balance++;
		} else if (code[i]==']') {
			balance--;
		}
		if (balance < 0) {
			printf("hey get your brackets straight\n");
			return 0;
		}
	}
	if (balance != 0) {
		printf("hey get your brackets straight\n");
		return 0;
	}
	int i = 0;
	int p = 0;
	while (p < strlen(code)) {
		switch (code[p]) {
			case '>':
				i++;
				p++;
				break;
			case '<':
				i--;
				p++;
				break;
			case '+':
				*(cells+i) += 1;
				p++;
				break;
			case '-':
				*(cells+i) -= 1;
				p++;
				break;
			case '.':
				printf("%c", *(cells+i));
				p++;
				break;
			case ',':
				printf("we don't support input sorry\n");
				p++;
				break;
			case '[': {
				if (*(cells+i) != 0) {
					p++;
					break;
				}
				int ball = 0;
				for (int j=p; j<strlen(code); j++) {
					if (code[j] == '[') {
						ball++;
					} else if (code[j] == ']') {
						ball--;
					}
					if (ball == 0) {
						p = j+1;
						break;
					}
				}
				break;
			}
			case ']': {
				if (*(cells+i) == 0) {
					p++;
					break;
				}
				int balr = 0;
				for (int j=p; j>0; j--) {
					if (code[j] == '[') {
						balr++;
					} else if (code[j] == ']') {
						balr--;
					}
					if (balr == 0) {
						p = j+1;
						break;
					}
				}
				break;
			}
			default:
				p++;
		}
	}
	return 0;
}