#ifndef __GAME_HPP__
#define __GAME_HPP__

#include "player.hpp"

class Game
{
private:
	Player *player;
	Player *opponent;
	Player *activePlayer;
	Board board;
public:
	Game(Player *player, Player *opponent);
	void play();
	void printTurnIndicator() const;
	void printPlayerNames() const;
	void nextPlayer();
	void congratulate() const;
	static void startSingleplayer();
	static void startMultiplayer();
};



#endif
