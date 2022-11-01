#ifndef __BOARD_HPP__
#define __BOARD_HPP__

#include <optional>

#include "position.hpp"

enum class Field {
	EMPTY,
	PLAYER,
	OPPONENT
};

char fieldToChar(Field);

class Board
{
public:
	Field fields[3][3];
	Board();
	void print() const;
	bool takePosition(Position, Field player);
	std::optional<Position> findThreatenedField(Field threateningPlayer) const;
	size_t countFields(Field type) const;
	Field checkWinner() const;
};

#endif
