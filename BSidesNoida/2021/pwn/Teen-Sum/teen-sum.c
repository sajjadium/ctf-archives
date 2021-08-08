//gcc teen-sum.c -f-no-stack-protector -o teen-sum
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char saved_name[0x100];

void welcome()
{
	alarm(0x61);
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
	puts("Welcome to our adder. Again :)");
	puts("Hope you enjoy.");
	return;
}

void intro(long do_change)
{
	unsigned long sz = 0;
	char name[0x30];

	if (do_change)
		printf("%s! New size please.", saved_name);
	else
		puts("We are very generous to people and to show that, we let people have whatever name length they choose."),
		puts("No... really what do you wanna have?");
	printf("> ");
	scanf("%ld", &sz);
	
	if (do_change)
		printf("New ");

	puts("Name please ^.^ : ");
	printf("> ");
	read(0, name, sz);
	name[sz] = 0;
	strcpy(saved_name, name);
	
	if (!do_change)
		printf("Hey %s\n", saved_name),
		puts("Nice to meet you!"),
		puts("Hope you like this beta version of our calculator :)");
	return;
}

void calc()
{
	unsigned long arr[100];
	unsigned long sz = 0, i = 0, sum = 0;
	
	intro(0);

	puts("Now, you can enter your numbers to be added.");
	puts("But with a heavy heart, we have to say that we can't let you have the full liberty of choosing size here, because some haxxors might do bad things to our calculator :(");
	puts("And you don't want that to happen, right?");
	puts("I'm sure you don't.");
	puts("So we'll allow you to have upto 100 numbers this time ^.^");
	puts("How many?");
	printf("> ");
	scanf("%ld", &sz);
	sz = sz % 101;

	puts("Please enter them one by one.");
	i = 0;
	while(1)
	{
		if (i >= sz || i < 0)
			break;
		printf("> ");
		scanf("%ld", &arr[i]);
		sum += arr[i];
		printf("You entered %ld\n", arr[i++]);
	}

	puts("Want to update your name?\n0. No\n1. Yes");
	printf("> ");
	scanf("%ld", &sz);
	if (sz)
		intro(1);

	printf("%s, Your sum is: %ld", saved_name, sum);
	return;
}

int main()
{
	welcome();
	calc();
	return 0;
}