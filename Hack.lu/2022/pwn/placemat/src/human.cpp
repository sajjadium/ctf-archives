#include "human.hpp"

#include <cstdio>
#include <optional>

#include "util.hpp"

void Human::requestName()
{
	printf("What's your name?\n");
	scanf("%s", this->name);
	util::readUntilNewline();
}

Position Human::takeTurn(Board &board)
{
	std::optional<Position> position;
	while (!position.has_value()) {
		printf("%s, enter the position you want to play (e.g. A3): ", this->name);
		fflush(stdout);
		char c1, c2;
		auto result = scanf("%c%c", &c1, &c2);
		if (result == EOF)
			throw 0;
		util::readUntilNewline();
		c1 |= 0x20; // Make lowercase
		if (c1 >= 'a' && c1 <= 'c' && c2 >= '1' && c2 <= '3')
		{
			pos_t x = c1 - 'a';
			pos_t y = c2 - '1';
			if (board.fields[x][y] == Field::EMPTY)
				position = Position(x, y);
		}
	}
	return *position;
}
