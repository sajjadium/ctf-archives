#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUF_SIZE 0x40

static int menu(void);
static void put(char *key);
static void get(char *key);
static int getnline(char *buf, int len);
static int getint(void);

int db_reg(const char *key, const char *data, size_t size);
char *db_get(const char *key, size_t *size);
int db_del(const char *key);

__attribute__((constructor))
static int init(){
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	return 0;
}

int main(void){
	int n;

	printf("Simple Key-Value Database");

	for(;;){
		char key[BUF_SIZE] = {0};
	   
		if(!(n = menu()))
			break;

		printf("Key : ");
		getnline(key, sizeof(key));

		switch(n){
			case 1:
				put(key);
				break;
			case 2:
				get(key);
				break;
			case 3:
				printf(db_del(key) ? "'%s' deleted!\n" : "'%s' not found...\n", key);
				break;
			default:
				puts("Wrong input.");
				continue;
		}
		puts("Done.");
	}
	puts("Bye!");

	return 0;
}

static int menu(void){
	printf(	"\nMENU\n"
			"================\n"
			"1. Put\n"
			"2. Get\n"
			"3. Delete\n"
			"0. Exit\n"
			"================\n"
			"> ");

	return getint();
}

static void put(char *key){
	size_t size;
	char *data;

	printf("Size : ");
	if((size = getint()) > 0x400){
		puts("Too Big!\n");
		return;
	}

	printf("Data : ");
	data = alloca(size);
	memset(data, 0, size);
	read(STDIN_FILENO, data, size);

	db_reg(key, data, size);
}

static void get(char *key){
	size_t size;
	char *data;

	if(!(data = db_get(key, &size))){
		printf("'%s' not found...\n", key);
		return;
	}

	puts("\n---- data ----");
	write(STDOUT_FILENO, data, size);
	puts("\n--------------\n");
}

static int getnline(char *buf, int size){
	char *lf;

	if(size < 0 || !fgets(buf, size, stdin))
		return 0;

	if((lf=strchr(buf,'\n')))
		*lf='\0';

	return 1;
}

static int getint(void){
	char buf[0x10] = {0};

	getnline(buf, sizeof(buf));
	return atoi(buf);
}
