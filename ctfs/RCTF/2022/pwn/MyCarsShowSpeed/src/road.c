#include "road.h"
#include <stdlib.h>
#include "args.h"


char *end[] = {"E","N","D",NULL};
char *user[] = {"Y","O","U",NULL};
char *bot[] = {"B","O","T",NULL};

void initRoad(road_t *road)
{
    road->playerRoad = 10;
    road->botRoad = 18;
    road->headShape = "+==============";
    road->bodyShape = "               ";

    road->buildRoad = &buildRoadImpl;
    road->printEnd = &printEndImpl;

}

void buildRoadImpl(road_t* this, int col)
{
    int startRows[2] = {this->playerRoad, this->botRoad};
    int startCol = 0;
    attron(COLOR_PAIR(1));
    for (int k = 0; k < 2; k++)
    {
        int startRow = startRows[k];
        for (int j = 1; j <= 6; ++j)
        {
            if(j % 6 == 0 || j % 6 == 1)
            {
                for (int i = 0; i < col; ++i)
                {
                    mvprintw(startRow, startCol, "%s", this->headShape);
                    startCol += 15;
                }
                mvprintw(startRow, startCol, "%s", "+");
                
            }
            else
            {
                for (int i = 0; i < col; ++i)
                {
                    mvprintw(startRow, startCol, "%s", this->bodyShape);
                    startCol += 15;
                }
                mvprintw(startRow, startCol, "%s", "|");
            }
            startRow++;
            startCol = 0;
        }
    }

    attroff(COLOR_PAIR(1));
}

void printEndImpl(road_t *_this)
{
    int endCol = END_COL + 2;
    int userRow = USER_ROW + 2, botRow = BOT_ROW + 2;
    int i = 0;
    while(end[i])
    {
        mvprintw(userRow, endCol, "%s", end[i]);
        mvprintw(userRow, endCol + 5, "%s", user[i]);
        mvprintw(botRow, endCol, "%s", end[i]);
        mvprintw(botRow, endCol + 5, "%s", bot[i]);
        userRow++;
        botRow++;
        i++;
    }

}


