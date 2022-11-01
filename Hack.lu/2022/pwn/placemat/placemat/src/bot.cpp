#include "bot.hpp"

#include <cstring>
#include <cstdio>
#include <chrono>
#include <thread>

#include "util.hpp"

const char* names[] = {
	"HAL 9000",
	"WALL-E",
	"R2-D2",
	"C-3PO",
	"GLaDOS",
	"Atlas",
	"P-Body",
	"CL4P-TP",
	"Dalek",
	"Marvin",
	"T-800",
	"Gizmoduck",
	"Little Helper",
	"Bender",
	"KVN",
	"Dreadnought",
	"Ultron",
	"ED-209",
	"Data",
	"Agent Smith",
	"NS-5",
	"AWESOM-O",
	"Optimus Prime",
	"Astroboy",
	"Adjutant",
	"Blitzcrank",
	"2B",
	"9S",
	"Big Daddy",
	"Clippy",
	"WOPR",
};

void Bot::requestName()
{
	strcpy(this->name, names[util::random.in_range(0, sizeof(names) / sizeof(char*) - 1)]);
}

Position Bot::takeTurn(Board &board)
{
	printf("%s is thinking...", this->name);
	fflush(stdout);
	std::this_thread::sleep_for(std::chrono::milliseconds(util::random.in_range(300, 800)));
	printf("\n");

	size_t playerTurn = board.countFields(Field::PLAYER);
	size_t botTurn = board.countFields(Field::OPPONENT);
	if (board.fields[1][1] == Field::EMPTY)
	{
		return Position(1, 1);
	}

	std::optional<Position> targetField = board.findThreatenedField(Field::OPPONENT);
	if (targetField.has_value())
	{
		return *targetField;
	}

	targetField = board.findThreatenedField(Field::PLAYER);
	if (targetField.has_value())
	{
		return *targetField;
	}

	if (playerTurn == 1)
	{
		if (board.fields[1][1] == Field::PLAYER && botTurn == 0)
		{
			return Position(2, 2);
		}
		Position playerPos(0, 0);
		for (size_t x = 0;x < 3;x++)
		{
			for (size_t y = 0;y < 3;y++)
			{
				if (board.fields[x][y] == Field::PLAYER)
				{
					playerPos = Position(x, y);
					break;
				}
			}
		}
		if (playerPos.x % 2 == 1)
			return Position(2, 2 - playerPos.y);
		if (playerPos.y % 2 == 1)
			return Position(2 - playerPos.x, 2);
		if (botTurn == 0)
			return Position(2 - playerPos.x, 1);
		return Position(2 - playerPos.x, 1);
	}
	if (playerTurn == 2 && botTurn == 1)
	{
		if ((board.fields[0][0] == Field::PLAYER && board.fields[2][2] == Field::PLAYER)
			||
			(board.fields[2][0] == Field::PLAYER && board.fields[0][2] == Field::PLAYER))
		{
			return Position(1, 2);
		}
	}
	Position corners[] = {Position(0, 0), Position(0, 2), Position(2, 0), Position(2, 2)};
	std::optional<Position> emptyCorner;
	for (size_t i = 0; i < 4; i++)
	{
		if (board.fields[corners[i].x][corners[i].y] == Field::EMPTY)
		{
			emptyCorner = corners[i];
			if (playerTurn > 2 || botTurn > 1)
				return *emptyCorner;
			size_t axisMatches = 0;
			for (size_t x = 0;x < 3;x++)
			{
				for (size_t y = 0;y < 3;y++)
				{
					if (board.fields[x][y] == Field::PLAYER)
					{
						if (x == emptyCorner->x)
							axisMatches++;
						if (y == emptyCorner->y)
							axisMatches++;
					}
				}
			}
			if (axisMatches >= 2)
				return *emptyCorner;
		}
	}
	if (emptyCorner.has_value())
	{
		return *emptyCorner;
	}

	for (size_t x = 0;x < 3;x++)
	{
		for (size_t y = 0;y < 3;y++)
		{
			if (board.fields[x][y] == Field::EMPTY)
				return Position(x, y);
		}
	}

	board.print();
	printf("There's no spot left for me to go\n");
	return Position(0, 0);
}
