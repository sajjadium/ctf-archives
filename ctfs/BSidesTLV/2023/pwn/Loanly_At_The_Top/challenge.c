#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include "flag.h"

#define EVER (;;)
#define FLAG_COST 1337 / 2 // yeah, this number again
#define MAX_LOAN 0x1000000

struct financial_ctx
{
	float money;
	float loan;
	int got_flag;
};

// show the flag, but you need to buy it first
void show_flag(struct financial_ctx * ctx)
{
	if (!ctx->got_flag)
	{
		printf("you don't own a flag, buy one first\n");
		return;
	}
	if (ctx->loan > 0)
	{
		printf("as long as you are in debt, i cannot trust you to keep the flag\n");
		return;
	}
	printf(FLAG);
	printf("\n");
}

// buy_flag - good example of choosing the right name for a function
void buy_flag(struct financial_ctx * ctx)
{
	if (ctx->money < FLAG_COST)
	{
		printf("you don't have enough money...\n");
		return;
	}
	if (ctx->got_flag)
	{
		printf("you already have a flag\n");
		return;
	}
	ctx->got_flag = 1;
	ctx->money -= FLAG_COST;
}

// leave your bank, get here a loan without an interest
void get_loan(struct financial_ctx * ctx)
{
	uint32_t how_much = 0;

	printf("how much money do you want? (0, 30000]\n");
	if (scanf("%d", &how_much) != 1)
	{
		printf("invalid input\n");
		return;
	}
	if (how_much > 30000)
	{
		printf("invalid amount. abort.\n");
		return;
	}
	if (ctx->loan + how_much > MAX_LOAN)
	{
		printf("maximal amount reached. abort.\n");
		return;
	}
	ctx->loan += how_much;
	ctx->money += how_much;
}

// return the loan
void return_loan(struct financial_ctx * ctx)
{
	uint32_t how_much = 0;

	printf("how much do you want to return?\n");
	if (scanf("%d", &how_much) != 1)
	{
		printf("invalid input\n");
		return;
	}
	if (how_much > ctx->money)
	{
		printf("you don't have enough money dear <:(\n");
		return;
	}
	if (how_much > ctx->loan)
	{
		printf("it's the first time someone returns more than they need...\n");
		printf("thanks, but we can't accept that\n");
		return;
	}
	ctx->money -= how_much;
	ctx->loan -= how_much;
}

// thanks chatGPT - that's probably fine :)
uint32_t get_rand_int() {
	uint32_t random_int;
	int random_fd = open("/dev/random", O_RDONLY);

	if (random_fd < 0) {
		perror("failed to open /dev/random");
		exit(1);
	}

	ssize_t bytes_read = read(random_fd, &random_int, sizeof(random_int));
	if (bytes_read < 0) {
		perror("failed to read /dev/random");
		exit(1);
	}

	close(random_fd);
	return random_int;
}

// invest - more like "gamble"
void invest(struct financial_ctx * ctx)
{
	uint32_t invest = 0;
	uint32_t rand = 0;

	printf("how much do you want to invest?\n");
	if (scanf("%d", &invest) != 1)
	{
		printf("invalid input\n");
		return;
	}
	if (invest > 312)
	{
		printf("risk is too high, try another amount...\n");
		return;
	}
	if (ctx->money < invest)
	{
		printf("you don't have enough money dude\n");
		return;
	}
	ctx->money -= invest;
	rand = get_rand_int();
	if (rand == 0x13371337)
	{
		printf("mazal tov :)\n");
		ctx->money += invest * 3.14;
		return;
	}
}

int main()
{
	int res = 0;
	int cmd = 0;
	struct financial_ctx ctx = {0};

	setbuf(stdout, NULL);
	printf("the flag is only available to the wealthy\n");
	for EVER
	{
		printf("\nyour financial state is: money: %f, loan: %f\n\n", ctx.money, ctx.loan);
		printf("what do you want to do?\n");
		printf("0) exit\n");
		printf("1) print flag\n");
		printf("2) buy flag\n");
		printf("3) get a loan\n");
		printf("4) return a loan\n");
		printf("5) try to get some $$$ in the capital market :)\n");
		printf(">> ");

		if(scanf("%d", &cmd) != 1)
		{
			printf("invalid input\n");
			break;
		}
		if (cmd == 0) //exit
			break;
		if (cmd == 1)
			show_flag(&ctx);
		if (cmd == 2)
			buy_flag(&ctx);
		if (cmd == 3)
			get_loan(&ctx);
		if (cmd == 4)
			return_loan(&ctx);
		if (cmd == 5)
			invest(&ctx);
	}

	printf("bye bye\n");
	return 0;
}
