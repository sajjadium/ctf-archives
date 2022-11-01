#ifndef __HUMAN_HPP__
#define __HUMAN_HPP__

#include "player.hpp"

class Human : public Player {
public:
	virtual void requestName();
	virtual Position takeTurn(Board &);
};

#endif
