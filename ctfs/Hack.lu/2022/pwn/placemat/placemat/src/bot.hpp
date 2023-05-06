#ifndef __BOT_HPP__
#define __BOT_HPP__

#include "player.hpp"

class Bot : public Player
{
public:
	virtual void requestName();
	virtual Position takeTurn(Board &);
};

#endif
