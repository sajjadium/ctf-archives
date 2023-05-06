#include "game.hpp"

#include <cstdio>
#include <cstring>
#include <fstream>
#include <typeinfo>

#include "human.hpp"
#include "bot.hpp"
#include "util.hpp"


Game::Game(Player *player, Player *opponent)
	: player(player), opponent(opponent)
{
	if (util::random.bit())
		this->activePlayer = opponent;
	else
		this->activePlayer = player;
}

void Game::startSingleplayer()
{
	Human human;
	Bot bot;
	human.requestName();
	bot.requestName();

	Game game(&human, &bot);
	game.play();
}

void Game::startMultiplayer()
{
	Human player1, player2;
	printf("Player 1: ");
	player1.requestName();
	printf("Player 2: ");
	player2.requestName();

	Game game(&player1, &player2);
	game.play();
}

void Game::printTurnIndicator() const
{
	char line[47];
	const char *arrow = u8"\u25bc";//\u1f817";
	memset(line, ' ', 46);
	line[46] = 0;
	size_t offset = (strlen(this->activePlayer->name) - 1) / 2;
	if (this->activePlayer == this->player)
		offset = 3 + offset;
	else
		offset = 42 - offset;
	strcpy(&line[offset], arrow);
	printf("\n\n%s\n", line);
}

void Game::printPlayerNames() const
{
	printf("X  %-20s%20s  O\n\n", this->player->name, this->opponent->name);
}

void Game::nextPlayer()
{
	if (this->activePlayer == this->player)
		this->activePlayer = this->opponent;
	else
		this->activePlayer = this->player;
}

void Game::congratulate() const
{
	printf("%s won!\n\n", this->activePlayer->name);

	if (this->activePlayer == this->opponent)
		return;

	std::ifstream code_file("redemption_code.txt");

	// Check if the loosing player is a bot
	if (typeid(*this->opponent) != typeid(Bot))
	{
		return;
	}

	printf("Congratulations for defeating %s.\n\n", this->opponent->name);
	char redemption_code[655360]; // 640k ought to be enough for anyflag
	code_file.getline(redemption_code, 655360);

	// Recheck if the game has actually been won before handing out the redemption_code
	// Just to make sure nobody does anything nasty
	if (this->board.checkWinner() != Field::PLAYER)
	{
		printf("Wait a minute. You didn't win! Did you cheat?\n\n");
	}
	else
	{
		printf("The redemption code for your free dessert is: %s\n\n", redemption_code);
	}
	memset(redemption_code, 0, 655360);
}

void Game::play()
{
	while (board.countFields(Field::EMPTY) > 0)
	{
		this->printTurnIndicator();
		this->printPlayerNames();
		this->board.print();
		Position selectedPosition = this->activePlayer->takeTurn(board);
		Field &selectedField = this->board.fields[selectedPosition.x][selectedPosition.y];
		if (selectedField != Field::EMPTY)
		{
			printf("Invalid field selected. Aborting game...\n\n");
			return;
		}
		if (this->activePlayer == this->player)
			selectedField = Field::PLAYER;
		else
			selectedField = Field::OPPONENT;
		Field winner = this->board.checkWinner();
		if (winner == Field::EMPTY)
		{
			nextPlayer();
		}
		else
		{
			printf("\n\n\n");
			this->printPlayerNames();
			this->board.print();
			this->congratulate();
			return;
		}
	}
	printf("\n\n\n");
	this->printPlayerNames();
	this->board.print();
}
