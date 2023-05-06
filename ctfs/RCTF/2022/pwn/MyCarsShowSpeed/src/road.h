#ifndef ROAD_H
#define ROAD_H
#include <stdio.h>
#include <ncurses.h>   



typedef struct road road_t;

struct road
{
    int         playerRoad;
    int         botRoad;
    char        *headShape;
    char        *bodyShape;
    void        (*buildRoad)(road_t* _this, int col);
    void        (*printEnd)(road_t* _this);

};

void initRoad(road_t *road);
void buildRoadImpl(road_t* _this, int col);
void printEndImpl(road_t *this);



#endif

