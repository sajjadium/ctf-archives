#include "board.hpp"

#include <cstdio>

Board::Board()
{
	for (pos_t x = 0;x < 3;x++)
	{
		for (pos_t y = 0;y < 3;y++)
		{
			this->fields[x][y] = Field::EMPTY;
		}
	}
}

void Board::print() const {
	printf("                   A   B   C\n\n");
	for (int y = 0;y < 3;y++)
	{
		printf("               %i  ", y + 1);
		for (int x = 0;x < 3;x++)
		{
			printf(" %c ", fieldToChar(this->fields[x][y]));
			if (x < 2)
				printf(u8"\u2502");
		}
		printf("\n");
		if (y < 2)
			printf(u8"                  \u2500\u2500\u2500\u253c\u2500\u2500\u2500\u253c\u2500\u2500\u2500\n");
	}
	printf("\n\n");
}

bool Board::takePosition(Position pos, Field player)
{
	if (player == Field::EMPTY)
		return false;
	Field &field = this->fields[pos.x][pos.y];
	if (field != Field::EMPTY)
		return false;
	field = player;
	return true;
}

std::optional<Position> Board::findThreatenedField(Field threateningPlayer) const
{
	// TODO Bottom left to top right not working
	for (pos_t startx = 0;startx < 3;startx++)
	{
		for (pos_t starty = 0;starty < 3;starty++)
		{
			for (pos_t xIncrement = 0;xIncrement <= 1;xIncrement++)
			{
				if (startx > 0 && xIncrement == 1)
					continue;
				for (pos_t yIncrement = -1;yIncrement != 2;yIncrement++)
				{
					if (starty != 2 && yIncrement == static_cast<pos_t>(-1))
						continue;
					if (starty > 0 && yIncrement == 1)
						continue;
					if (xIncrement == 0 && yIncrement == 0)
						continue;
					size_t ownedFields = 0;
					std::optional<Position> emptyField;
					for (pos_t i = 0;i < 3;i++)
					{
						pos_t x = startx + xIncrement * i;
						pos_t y = starty + yIncrement * i;
						Field currentField = this->fields[x][y];
						if (currentField == threateningPlayer)
						{
							ownedFields++;
						}
						else if (currentField == Field::EMPTY)
						{
							emptyField = Position(x, y);
						}
					}
					if (ownedFields == 2 && emptyField.has_value())
					{
						return emptyField;
					}
				}
			}
		}
	}
	return {};
}

size_t Board::countFields(Field type) const
{
	size_t amount = 0;
	for (pos_t x = 0;x < 3;x++)
	{
		for (pos_t y = 0;y < 3;y++)
		{
			if (this->fields[x][y] == type)
				amount++;
		}
	}
	return amount;
}

Field Board::checkWinner() const
{
	for (pos_t startx = 0;startx < 3;startx++)
	{
		for (pos_t starty = 0;starty < 3;starty++)
		{
			for (pos_t xIncrement = 0;xIncrement <= 1;xIncrement++)
			{
				if (startx > 0 && xIncrement == 1)
					continue;
				for (pos_t yIncrement = -1;yIncrement != 2;yIncrement++)
				{
					if (starty != 2 && yIncrement == static_cast<pos_t>(-1))
						continue;
					if (starty > 0 && yIncrement == 1)
						continue;
					if (xIncrement == 0 && yIncrement == 0)
						continue;
					size_t playerFields = 0;
					size_t opponentFields = 0;
					for (pos_t i = 0;i < 3;i++)
					{
						pos_t x = startx + xIncrement * i;
						pos_t y = starty + yIncrement * i;
						Field currentField = this->fields[x][y];
						if (currentField == Field::PLAYER)
							playerFields++;
						else if (currentField == Field::OPPONENT)
							opponentFields++;
					}
					if (playerFields == 3)
						return Field::PLAYER;
					if (opponentFields == 3)
						return Field::OPPONENT;
				}
			}
		}
	}
	return Field::EMPTY;
}

char fieldToChar(Field field) {
	switch (field) {
		case Field::PLAYER:
			return 'X';
		case Field::OPPONENT:
			return 'O';
		default:
			return ' ';
	}
}
