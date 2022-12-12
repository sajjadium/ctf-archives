#ifndef GAME_H
#define GAME_H

#include <stdio.h>
#include <unistd.h>
#include "store.h" /*declare game_t */
#include "car.h"
#include "road.h"
#include "win.h"
#include "util.h"


#include <ncurses.h>                    
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>





void gameMenu();
void printBannerImpl();
void printRulesImpl();
void initGame(game_t *_this);
void visitStoreImpl(game_t *_this);
void startGameImpl(game_t *_this);
void showInfoImpl(game_t *_this);
int checkCarImpl(game_t *_this);
void competeImpl(game_t *_this);
void finishGameImpl(game_t *_this);
void readGameInputImpl(game_t *_this);
void switchCarsImpl(game_t *_this);
extern int gameover;
extern int winRow, winCol;

#endif