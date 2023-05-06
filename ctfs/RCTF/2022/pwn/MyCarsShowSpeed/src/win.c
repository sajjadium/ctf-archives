

#include "win.h"
#include "road.h"
#include "car.h"

#include "args.h"

int winRow, winCol;

void initBoard()
{

    initscr();			
    start_color();
    use_default_colors();
    init_pair(3, COLOR_RED, -1);
	crmode();					
	keypad(stdscr, TRUE);
    getmaxyx(stdscr, winRow, winCol);		
	noecho();	
    init_pair(1, COLOR_RED, -1); /* red color */
    init_pair(2, COLOR_WHITE, -1); /* for road */
    
}

