#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct env {
    char name[0x10];
    char *content;
	struct env *fd;
} env;

uint32_t heap_size;
env* heap;

void init() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void set(char *ptr, int size) {
	if (!ptr)
		return;

	uint32_t idx = 0;
	env *temp = NULL;
	char *w = strchr(ptr, '=');

	if((w - ptr) >= 0x10) {
		puts("name is long");
		return;
	}

	env* e = malloc(sizeof(env));
		
	strncpy(e->name, ptr , w-ptr);
	e->name[w-ptr] = '\0';
	e->content = malloc((ptr+size) - (w+1));
	memcpy(e->content, w + 1, (ptr+size) - (w+1));
	e->fd = NULL;
	
	if(!heap) {
		heap = e;
	}
	else {
		temp = heap;
		while(1) {
			if(!strcmp(temp->name, e->name))
				break;
			
			if(temp->fd == NULL) {
				temp->fd = e;
				break;
			}
			else
				temp = temp->fd;
		}
	}
}

void unset(char *ptr) {
	if (!ptr || !heap) {
		return;
	}

	env *temp = heap;
	env *prev = NULL;

	while(1) {
		if(!strcmp(ptr, temp->name)) {
			free(temp->content);
			free(temp);
			break;	
		}
	
		temp = temp->fd;
		if(temp == NULL)
			break;
	}
}

void echo(char *ptr) {
	if (!ptr || !heap) {
		return;
	}

	env* temp = heap;

	while(1) {
		if(!strcmp(ptr, temp->name)) {
			printf("%s: %s\n", temp->name, temp->content);
			return;
		}
		
		temp = temp->fd;
		if(temp == NULL)
			break;
	}

	puts("not found");
}

int main(void) {
	char buf[0x500];
	uint32_t t = 0;

	init();

	while (1) {
		memset(buf, 0, 0x500);

		printf("$ ");
		t = read(0, buf, 0x500);
		if(buf[t - 1] == '\n') { 
			buf[t - 1] = '\0';
			t -= 1;
		}

		char *ptr = strtok(buf, " ");
		char *ptr2 = strtok(NULL, " ");

		if (!strcmp(ptr, "set"))
			set(ptr2, t-4);
		else if (!strcmp(ptr, "unset")) 
			unset(ptr2);
		else if (!strcmp(ptr, "echo")) 
			echo(ptr2);
		else
			puts("command not found");
	}
}

