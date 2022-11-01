#include "board.hpp"
#include "human.hpp"
#include "bot.hpp"
#include "util.hpp"
#include "game.hpp"

#include <cstdio>
#include <cstdlib>

void bot_testbench_player_starts();
void bot_testbench_bot_starts();

int main()
{
	while (true)
	{
		char selection;
		printf("1 Play\n2 Rules\n3 Exit\n");
		auto result = scanf("%c", &selection);
		if (result == EOF)
			return 1;
		util::readUntilNewline();
		printf("\n\n");
		if (selection == '1')
		{
			printf("Do you want to play against a (b)ot or against a (h)uman? ");
			fflush(stdout);
			result = scanf("%c", &selection);
			if (result == EOF)
				return 1;
			util::readUntilNewline();
			selection |= 0x20; // Make lowercase
			if (selection == 'b')
				Game::startSingleplayer();
			else if (selection == 'h')
				Game::startMultiplayer();
		}
		else if (selection == '2')
		{
			printf("The rules are simple. The board is a 3x3 grid.\nYou and your opponent take turns placing their symbol into the grid.\nPlayer 1 has a cross (X), player 2 a ring (O).\nWhoever manages to put three of their symbol in a row (diagonals count) wins.\nYou can either play against a friend or against one of our expert level bots.\nIF YOU MANAGE TO WIN AGAINST ONE OF THE BOTS YOU'LL WIN A FREE DESSERT!\n\nPress Enter to continue...");
			fflush(stdout);
			util::readUntilNewline();
			printf("\n\n");

		}
		else if (selection == '3')
		{
			break;
		}
	}
	return 0;
}
