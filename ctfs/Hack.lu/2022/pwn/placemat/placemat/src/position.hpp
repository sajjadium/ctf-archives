#ifndef __POSITION_HPP__
#define __POSITION_HPP__

#include <optional>

typedef size_t pos_t;

class Position {
public:
	pos_t x;
	pos_t y;
	Position(pos_t x, pos_t y);
};

#endif
