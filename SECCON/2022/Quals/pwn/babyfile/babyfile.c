#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static int menu(void);
static int getnline(char *buf, int size);
static int getint(void);

#define write_str(s) write(STDOUT_FILENO, s, sizeof(s)-1)

int main(void){
	FILE *fp;

	alarm(60);

	write_str("Play with FILE structure\n");

	if(!(fp = fopen("/dev/null", "r"))){
		write_str("Open error");
		return -1;
	}
	fp->_wide_data = NULL;

	for(;;){
		switch(menu()){
			case 0:
				goto END;
			case 1:
				fflush(fp);
				break;
			case 2:
				{
					unsigned char ofs;
					write_str("offset: ");
					if((ofs = getint()) & 0x80)
						ofs |= 0x40;
					write_str("value: ");
					((char*)fp)[ofs] = getint();
				}
				break;
		}
		write_str("Done.\n");
	}

END:
	write_str("Bye!");
	_exit(0);
}

static int menu(void){
	write_str("\nMENU\n"
			"1. Flush\n"
			"2. Trick\n"
			"0. Exit\n"
			"> ");

	return getint();
}

static int getnline(char *buf, int size){
	int len;

	if(size <= 0 || (len = read(STDIN_FILENO, buf, size-1)) <= 0)
		return -1;

	if(buf[len-1]=='\n')
		len--;
	buf[len] = '\0';

	return len;
}

static int getint(void){
	char buf[0x10] = {};

	getnline(buf, sizeof(buf));
	return atoi(buf);
}
