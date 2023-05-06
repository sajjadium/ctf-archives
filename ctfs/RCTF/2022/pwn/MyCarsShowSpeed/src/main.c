#include "game.h"
#include "store.h"
#include "win.h"
#include "car.h"
#include "road.h"
#include <stdlib.h>





int main()
{
    alarm(600);
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    game_t *game = malloc(sizeof(game_t));
    initGame(game);

    while(1)
        game->readInput(game);


}