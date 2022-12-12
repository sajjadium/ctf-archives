#include"car.h"
#include <unistd.h>
#include "util.h"
#include <stdlib.h>
#include <pthread.h>
#include "args.h"

int gameover;
pthread_mutex_t mx = PTHREAD_MUTEX_INITIALIZER;

char *carShape[] = {" ______",
                    "/|_||_\\`._",
                    "(   _   _ _\\",
                    "=`-(_)--(_)-`",
                    NULL};

char *botCarShape[] = {" ______",
                        "/|_||_\\`._",
                        "(  _BOT _ _\\",
                        "=`-(_)--(_)-`",
                        NULL};


void initCar(car_t *_this, int row, int col, 
            int stability, int fuel, int step, int type)
{

    if(type != BOT)
    {
        char *name = _this->name;
        printf("Name your car:\n");
        printf("> ");
        fflush(stdout);
        int nread = read(0, name, 7);
        if(name[nread-1] == '\n')   
            name[nread-1] = '\0';
        else
            name[nread] = '\0';

        _this->health = 100;
    }

    _this->row = row;
    _this->col = col;
    _this->stability = stability;
    _this->fuel = fuel;
    _this->step = step;
    _this->type = type;
    _this->fixed = 0;
    _this->isTaken = 0;
    _this->isWon = 0;
    _this->fixDifficulty = 1;
    _this->getStep = &getStepImpl;
    _this->moveCar = &moveCarImpl;
    _this->printCar = &printCarImpl;

}

void initCarList(carList_t *_this)
{
    _this->car = NULL;
    _this->next = NULL;
    _this->carNums = 0;

    _this->addCar = &addCarImpl;
    _this->findCar = &findCarImpl;
    _this->switchCar = &switchCarImpl;
    _this->showCars = &showCarsImpl;
    _this->deleteCar = &deleteCarImpl;
}

void addCarImpl(car_t *car, carList_t *entry)
{
    carList_t *cur = entry;
    while(cur && cur->next)
    {
        if(cur->car == NULL)
        {
            cur->car = car;
            break;
        }
        cur = cur->next;
    }
    
    if(cur->next == NULL)
    {
        if(cur->car != NULL)
        {
            carList_t *newCar = malloc(sizeof(carList_t));
            newCar->car = car;
            newCar->next = NULL;
            cur->next = newCar;
        }
        else
            cur->car = car;

    }
}


car_t* switchCarImpl(carList_t *_this)
{
    car_t *car;
    char name[8];
    memset(name, 0, sizeof(name));
    int nread = read(0, name, 8);
    name[nread - 1] = name[nread - 1] == '\n' ? '\0' : name[nread - 1];

    car = _this->findCar(name, _this);
    
    return car;
}

int getStepImpl(car_t *_this)
{
    int stability = _this->stability, p, step;
    p = 100 - stability;
    step = !isSlip(p);
    return step;
}


int moveCarImpl(car_t *_this)
{
    int row = _this->row, col = _this->col;
    int ch = 0, moveStep;
    moveStep = _this->getStep(_this);

    
    if(_this->type != BOT)
    {
        usleep(35000);
        //while( (ch = getch())!= 'd' && ch !='D' );
    }

    else
    {
        usleep(35000);
    }

    pthread_mutex_lock (&mx);
    for(int i = 0; i < CAR_HEIGHT; ++i)
    {
        col = _this->col;
        for(int j = 0; j < BLOCK - 2; ++j)
            mvchgat(row, col++, 2, A_INVIS, 3, NULL);
        row++;
    }
    _this->col += _this->getStep(_this);
    _this->printCar(_this);
    
    if(_this->col + CAR_LENGTH >= END_COL)
    {
        pthread_mutex_unlock (&mx);
        _this->isWon = 1;
        return 1;
    }
    pthread_mutex_unlock (&mx);    
    return 0;
} 

void *moveCarImplThread(void *args)
{
    int won = 0;
    car_t *car = (car_t *)args;
    while(gameover == 0)
    {
        won = car->moveCar(car);
        if(won)
            gameover = 1;
    }

    return NULL;
}

void printCarImpl(car_t *_this)
{   
    char **shape; 
    int row = _this->row;
    int col = _this->col;
    int i = 0;
    
    if(_this->type == BOT)
        shape = botCarShape;
    else
        shape = carShape;
    while(shape[i])
    {
        mvprintw(row, col, "%s", shape[i]);
        refresh();
        row++;
        i++;
    }
    
}

void showCarsImpl(carList_t *_this)
{
    carList_t *curCar = _this;
    while(curCar)
    {
        car_t *car = curCar->car;
        if(car)
            printf("CarName: %s   Fuel: %d   Health: %d   Stability: %d\n", 
                    car->name, car->fuel, car->health, car->stability);
        curCar = curCar->next;
    }
}

car_t* findCarImpl(char *name, carList_t *_this)
{
    carList_t *cur = _this;
    while(cur)  
    {
        car_t *car = cur->car;
        if(car && strcmp(name, car->name) == 0)
            return car;
        cur = cur->next;
    }
    return NULL;
}

void deleteCarImpl(car_t *car, carList_t **_this)
{
    carList_t *cur = *_this;
    while(cur)  
    {
        if(cur->car == car)
        {
            cur->car = NULL;
            break;
        }
        cur = cur->next;
    }

}



