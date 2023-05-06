#ifndef CAR_H
#define CAR_H
#include <ncurses.h>  
#include <string.h>
#include <time.h>
#include <stdint.h>


typedef struct car car_t;
typedef struct carList carList_t;


struct car
{
    char        name[8];
    uint8_t     type; 
    uint8_t     performance;
    uint8_t     isTaken;
    uint8_t     isWon;
    uint8_t     fixed;
    uint8_t     step;
    uint8_t     fixDifficulty; 
    
    int         fuel;
    int         stability;
    int         health; 
    int         row;
    int         col;
    int         cost;
    int         padding;
    time_t      fixTime;

    int         (*moveCar)(car_t *_this);
    void        (*addFuel)(car_t *_this);
    void        (*increaseSpeed)(car_t *_this);
    void        (*gainExp)(car_t *_this);
    void        (*fix)(car_t *_this);
    void        (*printCar)(car_t *_this);
    int         (*getStep)(car_t *_this);

};

struct carList
{
    int         carNums;
    car_t       *car;
    carList_t   *next;

    void        (*addCar)(car_t *car, carList_t *_this);
    void        (*showCars)(carList_t *_this);
    car_t*      (*switchCar)(carList_t *_this);
    car_t*      (*findCar)(char *name, carList_t *_this);
    void        (*deleteCar)(car_t *car, carList_t **_this);
};

void initCar(car_t *_this, int row, int col, 
            int stability, int fuel, int step, int type);
void initCarList(carList_t *_this);
int moveCarImpl(car_t *_this);
void printCarImpl(car_t *_this);
void showCarsImpl(carList_t *_this);
void addCarImpl(car_t *car, carList_t *entry);
car_t* switchCarImpl(carList_t *_this); 
car_t* findCarImpl(char *name, carList_t *_this);
void deleteCarImpl(car_t *car, carList_t **_this);
int getStepImpl(car_t *_this);

void *moveCarImplThread(void *args);
extern int winCol;
#endif

