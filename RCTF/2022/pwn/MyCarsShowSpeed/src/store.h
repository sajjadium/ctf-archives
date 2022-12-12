#ifndef STORE_H
#define STORE_H
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "car.h"
#include "road.h"

#define GOODS_NUM 10

typedef struct goods goods_t;
typedef struct goodsList goodsList_t;
typedef struct store store_t;
typedef struct game game_t;
struct game
{
    void        (*printRules)();
    void        (*showCars)(game_t *_this);
    void        (*showInfo)(game_t *_this);
    int         (*checkCar)(game_t *_this);
    void        (*startGame)(game_t *_this);
    void        (*switchCars)(game_t *_this);
    void        (*compete)(game_t *_this);
    void        (*visitStore)(game_t *_this);
    void        (*menu)(void);
    void        (*printBanner)();
    void        (*readInput)(game_t *_this);
    void        (*finishGame)(game_t *_this);
    
    store_t     *store;
    road_t      *road;
    car_t       *userCar;
    car_t       *botCar;
    carList_t   *carList;
    uint32_t    money;
    int         winCol;
    uint32_t    winTimes;

};

struct goods
{
    char        *name;
    int         price;
};

struct goodsList
{
    goods_t         *goods;
    goodsList_t     *next;
};

struct store
{
    goodsList_t *goodsList;
    carList_t    *carList;
    void        (*menu)(void);
    void        (*showGoods)(store_t *_this);
    void        (*readInput)(store_t *_this, game_t *game);
    void        (*buyGoods)(store_t *_this, game_t *game);
    void        (*sellGoods)(store_t *_this, game_t *game);
    void        (*fixCar)(store_t *_this, game_t *game);
    car_t*      (*fetchCar)(store_t *_this, game_t *game);
    
};

void initStore(store_t *_this);
void storeMenu(void);
void showGoodsImpl(store_t *_this);
void readStoreInputImpl(store_t *_this, game_t *game);
void sellGoodsImpl(store_t *_this, game_t *game);
void buyGoodsImpl(store_t *_this, game_t *game);
void fixCarImpl(store_t *_this, game_t *game);
car_t * fetchCarImpl(store_t *_this, game_t *game);

#endif