#ifndef __PLAYER_HPP__
#define __PLAYER_HPP__

#include "board.hpp"

class Player {
public:
	char name[20];
	Player();
	virtual ~Player() = default;
	virtual void requestName() = 0;
	virtual Position takeTurn(Board &) = 0;
};

#endif
