#include <pthread.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <alloca.h>

void readuntil(char e) {
  char c;
  do {
    c = getchar();
    if (c == EOF) exit(1);
  } while(c != e);
}

void get_ul(unsigned long* num) {
	fflush(stdout);
	scanf("%lu", num);
	readuntil('\n');
}

int get_int() {
	int d;
	fflush(stdout);
	scanf("%d", &d);
	readuntil('\n');
	return d;
}

void init() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);

	srand(time(0));
	alarm(60*4);
}

void win() {
	char buf[0x10];
	puts("> ");
	gets(buf);
}

int max_tries;

unsigned long play_game() {
	static int counter;
	unsigned long r, guess;
	
	r = rand();

	printf("Enter your guess : ");
	get_ul(&guess);

	if(r == guess) {
		printf("win!\n");
		win();
	} 
	
	if(counter == max_tries-1) {
		printf("Sorry, that was the last guess!\n");
		printf("You entered %lu but the right number was %lu\n", guess, r);
		return r;
	}

	counter++;

	return r;
}

void set_number_of_tries() {
	int tries;
	do {
		printf("Enter the number of tries : ");
		tries = get_int();
	} while(tries < 0 || tries > 10);
	
	max_tries = tries;
	return;
}

int get_size() {
	
	int size;	
	
	do {
		printf("Enter the size : ");
		size = get_int();
	} while(size < 0 || size > 100);

	return size;
}


int main() {

	init();
	int size = get_size();
	unsigned long* values = (unsigned long*)alloca(size*sizeof(unsigned long));
	
	set_number_of_tries();		
	
	for(int i=0; i<max_tries; i++) {
		play_game();
	}
	
	fflush(stdout);

	printf("I don't think you won the game if you made it until here ...\n");
	printf("But maybe a threaded win can help?\n");

	pthread_t tid;
	pthread_create(&tid, NULL, (void*)win, NULL);
	pthread_join(tid, NULL);

	return 0;
}
