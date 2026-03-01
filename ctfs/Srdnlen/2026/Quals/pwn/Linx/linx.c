#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <regex.h>
#include <sys/mman.h>

int read_int() { char *buf = malloc(16);
	printf(">> ");
	fgets(buf, 16, stdin);
	return atoi(buf);
}

#define LINKS_COUNT 30
#define LINKS_LEN 50

typedef struct {
	size_t src_idx, dst_idx;
} linkT;

char *links[LINKS_COUNT] = {0};
size_t links_cnt = 0;
linkT *linking = NULL;

regex_t re;

__attribute__((constructor))
void initz() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
    if (regcomp(&re, "^\\[(.*)\\]\\((.*)\\)", REG_EXTENDED) != 0) {
        puts("Failed to compile pattern");
        return;
	}
}

__attribute((destructor))
void deinit() {
	regfree(&re);
}

void do_unlink() {
	char text[512] = {0};
	printf("Insert your link to be unlinked\n> ");
    if (fgets(text, sizeof(text), stdin) == NULL) exit(EXIT_FAILURE);
    text[strcspn(text, "\n")] = '\0';

	bool found = false;
	size_t link_idx;
	for (size_t i = 0; i < LINKS_COUNT && !found; i++) {
		if (links[i] && !strcmp(text, links[i]))
			found = true, link_idx = i;
	}
	if (!found) return;
	for (size_t i = 0; i < links_cnt; ) {
		bool is_dst = !strcmp(links[linking[i].dst_idx], text);
		bool is_src = !strcmp(links[linking[i].src_idx], text);
		if (is_src || is_dst) { // need to delete this linking
			memmove(linking+i, linking+i+1, (links_cnt-i-1)*sizeof(linkT));
			linking = realloc(linking, --links_cnt*sizeof(linkT));
		} else i++;
	}
	free(links[link_idx]);
	links[link_idx] = NULL;

}

void do_link() {
	char text[512] = {0};

	printf("Insert your link (format: \"[<your src>](<your dst>)\")\n> ");
    if (fgets(text, sizeof(text), stdin) == NULL) exit(EXIT_FAILURE);
    text[strcspn(text, "\n")] = '\0';

    regmatch_t *m = calloc(re.re_nsub+1, sizeof(regmatch_t));
    if (regexec(&re, text, re.re_nsub+1, m, 0) == 0) {
		char *src = calloc(1, LINKS_LEN);
		char *dst = calloc(1, LINKS_LEN);
		for (size_t i = 1; i < re.re_nsub+1; i++) {
	        size_t len = m[i].rm_eo - m[i].rm_so;
			if (i == 1) // first group - link from
				memcpy(src, text+m[i].rm_so, len);
			else if (i == 2) // second group - link to
				memcpy(dst, text+m[i].rm_so, len);
		}
		bool src_found = false, dst_found = false;
		size_t src_idx, dst_idx;
		for (size_t i = 0; i < LINKS_COUNT && (!src_found || !dst_found); i++) {
			if (links[i]) {
				if (!strcmp(src, links[i]))
					src_found = true, src_idx = i;
				if (!strcmp(dst, links[i]))
					dst_found = true, dst_idx = i;
			}
		}
		// need to occasionally alloc them
		if (!src_found) {
			for (size_t i = 0; i < LINKS_COUNT && !src_found; i++)
				if (!links[i]) {
					src_found = true, src_idx = i, links[src_idx] = src;
					if (!strcmp(src, dst)) // handle adding linking from and to same new string
						dst_found = true, dst_idx = i, links[dst_idx] = src;
				}
		} else {
			free(src);
			src = links[src_idx];
		}
		if (!dst_found) {
			for (size_t i = 0; i < LINKS_COUNT && !dst_found; i++)
				if (!links[i])
					dst_found = true, dst_idx = i, links[dst_idx] = dst;
		} else {
			free(dst);
			dst = links[dst_idx];
		}
		if (!src_found || !dst_found) {
			puts("No space left for new links!");
			free(src);
			free(dst);
			return;
		}
		// now just need to link them
		linking = realloc(linking, ++links_cnt*sizeof(linkT));
		linking[links_cnt-1] = (linkT){.src_idx = src_idx, .dst_idx = dst_idx};
		printf("Good! You have linked \"%s\" and \"%s\"!\n", src, dst);
    } else {
        puts("No match");
    }
	free(m);
}

void show_links() {
	puts("Here are all the links you inserted:");
	for (size_t i = 0; i < links_cnt; i++) {
		char *src = links[linking[i].src_idx];
		char *dst = links[linking[i].dst_idx];
		printf("\t\"%s\" -> \"%s\"\n", src, dst);
	}
	puts("End of links");
}


int menu() {
    puts(" [1] Insert new link");
    puts(" [2] Unlink a link");
    puts(" [3] Show links");
	puts(" [4] Quit");
    return read_int();
}

__attribute__((constructor)) void init() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
}

int main() {
	void *mem = mmap((void*)0x1337000ULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	if (mem == MAP_FAILED) exit(EXIT_FAILURE);
	puts("Welcome, provide me with your linking sauce:");
	if (fgets(mem, 0x20, stdin) == NULL) exit(EXIT_FAILURE);
	printf("Here's where I put your sauce: %p\n", mem);
	while (1) {
		switch (menu()) {
			case 1:
				do_link();
				break;
			case 2:
				do_unlink();
				break;
			case 3:
				show_links();
				break;
			case 4:
				puts("Bye");
				exit(EXIT_SUCCESS);
			default:
				puts("Invalid option!");
				break;
		}
	}
}
