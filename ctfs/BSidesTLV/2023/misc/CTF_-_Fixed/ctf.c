#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<time.h>
#include<string.h>
#include<fcntl.h>
#include<unistd.h>

#define UNUSED(expr) (void)(expr)

#define NUM_OF_RAND	100
#define S_SIZE		41

char s[S_SIZE] = {0};
double r[NUM_OF_RAND] = {0};
unsigned int num = NUM_OF_RAND;

int main() {
	srand(time(NULL));
	
	FILE *f = fopen("flag.txt", "r");
	if (f == NULL) return 1;
	int is = (int)fgets(s, S_SIZE, f);	// avoid  error: ignoring return value of ‘fgets’
	UNUSED(is);	// avoid error: unused variable ‘is’
	fclose(f);

	int fd = open("/dev/random", O_RDONLY);
	if (fd < 0) return 1;
	
	int rnd = 0;
	for(int i=0; i<num; ++i) {
		ssize_t bytes_read = read(fd, &rnd, sizeof(rnd));
		if (bytes_read < 0) return 1;
		r[i] = (double)(rnd ^ s[i%S_SIZE]);
	}
	close(fd);

	for(int i=0; r[i]!=0 && i<NUM_OF_RAND; ++i)	{
		printf("[%02d] %.f\n", i, r[i]);
	}

	return 0;
}
