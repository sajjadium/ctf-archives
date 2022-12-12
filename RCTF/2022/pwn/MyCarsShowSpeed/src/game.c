#include "game.h"
#include "car.h"
#include <pthread.h>
#include "args.h"

pthread_t userThread, botThread;

void initGame(game_t *_this)
{
    road_t      *road;
    carList_t   *carList;
    car_t       *botCar;
    store_t     *store;

    _this->money = 120;
    _this->winTimes = 0;

    road = malloc(sizeof(road_t));
    carList = malloc(sizeof(carList_t));
    botCar = malloc(sizeof(car_t));
    store = malloc(sizeof(store_t));
    initRoad(road);
    initCar(botCar, BOT_ROW + 1, BOT_COL, 85, 0, 0, 0);
    initCarList(carList);
    initStore(store);
    

    _this->road = road;
    _this->botCar = botCar;
    _this->userCar = NULL;
    _this->carList = carList;
    _this->store = store;
    _this->menu = &gameMenu;
    _this->printBanner = &printBannerImpl;
    _this->printRules = &printRulesImpl;
    _this->checkCar = &checkCarImpl;
    _this->showInfo = &showInfoImpl;
    _this->startGame = &startGameImpl;
    _this->compete = &competeImpl;
    _this->switchCars = &switchCarsImpl;
    _this->finishGame = &finishGameImpl;
    _this->readInput = &readGameInputImpl;
    _this->visitStore = &visitStoreImpl;
}

void gameMenu()
{
    char banner[] = "============";
    printf("\n%sGameMenu%s\n",banner, banner);
    printf("\t1. New a Game\n\t2. Show Information\n\t3. Visit The Store\n\t4. Switch Cars\n\t5. Rules\n\t6. Quit");
    printf("\n%sGameMenu%s\n",banner, banner);
    printf("> ");
    fflush(stdout);
}

void printBannerImpl()
{
    char banner[] = "Welcome to play this simple game in RCTF 2022!";
    char rules[] = "Press space to start game. Press q to quit.";
    attron(COLOR_PAIR(1) | A_BOLD);
    mvprintw(BANNER_ROW, (winCol - strlen(banner)) / 2, "%s", banner);
    mvprintw(BANNER_ROW + 1, (winCol - strlen(rules)) / 2, "%s", rules);
    attroff(COLOR_PAIR(1) | A_BOLD);
}

void printRulesImpl()
{
    char banner[] = "============";
    char rules[] = "In this game, you are going to race against the bot to earn money to buy what you want.\n\
Note that the better your car is, the more possibly you are going to win.";

    printf("\n%sGameRules%s\n",banner, banner);
    printf("%s\n", rules);
    printf("\n%sGameRules%s\n",banner, banner);

}

void readGameInputImpl(game_t *_this)
{
    int ch;
    char buf[8];
    _this->menu();
    read(0, buf, 8);
    ch = atoi(buf);
    switch(ch)
    {
        case 1:
            _this->startGame(_this);
            break;
        case 2:
            _this->showInfo(_this);
            break;
        case 3:
            _this->visitStore(_this);
            break;
        case 4:
            _this->switchCars(_this);
            break;
        case 5:
            _this->printRules();
            break;
        case 6:
            exit(0);
    }
}

void visitStoreImpl(game_t *_this)
{
    store_t *store = _this->store;
    store->readInput(store, _this);
}


void showInfoImpl(game_t *_this)
{
    char banner[] = "============";
    printf("\n%sInformation%s\n",banner, banner);
    printf("Money: %d\tCars: %d \tWinTimes: %d\n", _this->money, _this->carList->carNums, _this->winTimes);
    _this->carList->showCars(_this->carList);
    if(_this->userCar)
        printf("Your using car is: %s\n", _this->userCar->name);
    printf("%sInformation%s\n\n",banner, banner);
}

void competeImpl(game_t *_this)
{
    gameover = 0;
    int ch;
    car_t *car = _this->userCar;
    car_t *botCar = _this->botCar;
    
    pthread_create(&userThread, NULL, moveCarImplThread, (void *)(car));
    pthread_create(&botThread, NULL, moveCarImplThread, (void *)(botCar));
    

    while(1)
    {
        ch = getch();
        if(ch == 'q' || ch == 'Q')
        {
            gameover = 1;
            break;
        }

        if(gameover)
            break;
    }

Over:
    pthread_join(userThread, NULL);
    pthread_join(botThread, NULL);

    
}

void switchCarsImpl(game_t *_this)
{
    car_t *car;
    char name[9];
    if(_this->carList->carNums == 0)
    {
        puts("You don't have cars");
        return;
    }
    _this->carList->showCars(_this->carList);
    printf("Which car do you want to switch to?\n");
    printf("> ");
    fflush(stdout);
    int nread = read(0, name, 8);
    if(name[nread-1] == '\n')   
        name[nread-1] = '\0';
    else
        name[nread] = '\0';
    car = _this->carList->findCar(name, _this->carList);
    if(car == NULL)
    {
        puts("You don't have this one.");
        return;
    }
    _this->userCar = car;
    puts("Switch succesfully!");
}

int checkCarImpl(game_t *_this)
{
    car_t *car = _this->userCar;
    if(car == NULL)
    {
        puts("You don't have a car,go to the store to buy one.\nIf your car is being fixed, go to fetch your car.\n");
        return 0;
    }
    if(car->fixed)
    {
        puts("Your car is being fixed.");
        return 0;
    }
    if(car->health < MIN_HEALTH)
    {
        puts("Your car is under bad condition. You should fix it.");
        return 0;
    }
    if(car->fuel < MIN_FUEL)
    {
        puts("Your car has run out of fuel. You should buy some fuel");
        return 0;
    }
    
    return 1;
}

void startGameImpl(game_t *_this)
{
    int ch;
    if(_this->checkCar(_this) == 0)
        return ;
    initBoard();
    _this->userCar->col = USER_COL;
    _this->botCar->col = BOT_COL;
    road_t *road = _this->road;
    if(road != NULL)
    {
        road->buildRoad(road, ROAD_BLOCKS);
        road->printEnd(road);
    }
    _this->printBanner();
    _this->userCar->printCar(_this->userCar);
    _this->botCar->printCar(_this->botCar);
    while(1)
    {
        ch = getch();
        if(ch == 'q' || ch == 'Q')
            goto End;
        if(ch == ' ')
            break;
    }
    _this->compete(_this);

End:
    _this->finishGame(_this);
    clear();
    endwin();

}

void finishGameImpl(game_t *_this)
{
    car_t *car = _this->userCar;
    int fuelCost, healthCost;
    int p = 10; 
    static double steps;

    fuelCost = car->col / 10;
    healthCost = car->col / 5; 
    car->health -= healthCost;
    car->fuel -= fuelCost;
    if(car->health < 0)
        car->health = 0;
    if(car->fuel < 0)
        car->fuel = 0;
    car->fixDifficulty++;

    if(isSlip(p))
    {
        char msg[] = "You are luck!\nYour car's perfomrance increased!";
        mvprintw(MSG_ROW + 1, (winCol - strlen(msg)) / 2, "%s", msg);
        steps += 0.1;
        if(steps == 1.0)
        {
            steps = 0;
            _this->userCar->step += 1;
        }
        if(_this->userCar->stability < 100)
        _this->userCar->stability++;

        _this->userCar->performance++;
    }

    attron(COLOR_PAIR(1));
    if(_this->botCar->isWon)
    {
        int ch;
        char msg[] = "You lose! Press enter to quit...";
        _this->botCar->isWon = 0;
        if(car->stability < _this->botCar->stability)
        {
            car->stability += 5;
            car->performance ++;
        }
        
        mvprintw(BANNER_ROW + 3, (winCol - strlen(msg)) / 2, "%s", msg);
        while((ch = getch()) != '\n');
    }
    else if(_this->userCar->isWon)
    {
        int ch;
        _this->winTimes++;
        _this->userCar->isWon = 0;
        _this->money += 10;
        mvprintw(BANNER_ROW + 3, (winCol - 10) / 2, "%s", "You Won!!! Press enter to quit...");
        while((ch = getch()) != '\n');
    }

    
    attroff(COLOR_PAIR(1));
}