#include"store.h"
#include <time.h>
#include "args.h"
#include <unistd.h>
#include <fcntl.h>


void addGoods(goodsList_t *entry, goods_t *goods)
{
    goodsList_t *cur = entry;
    while(cur && cur->next)
    {
        if(cur->goods == NULL)
        {
            cur->goods = goods;
            break;
        }
        cur = cur->next;
    }
    
    if(cur->next == NULL)
    {
        if(cur->goods != NULL)
        {
            goodsList_t *newGoods = malloc(sizeof(goodsList_t));
            newGoods->goods = goods;
            newGoods->next = NULL;
            cur->next = newGoods;
        }
        else
            cur->goods = goods;

    }
    
}

goods_t* findGoods(char *name, store_t *_this)
{
    goodsList_t *cur = _this->goodsList;
    while(cur != NULL)
    {
        goods_t *goods = cur->goods;
        if(strcmp(name, goods->name) == 0)
            return goods;
        cur = cur->next;
    }
    return NULL;
}

void initStore(store_t *_this)
{
    int goodsNum = 0;
    goodsList_t *goodsList = malloc(sizeof(goodsList_t));
    carList_t *carList = malloc(sizeof(carList_t));

    static goods_t normalCar = {"NormalCar", 50};
    static goods_t superCar = {"SuperCar", 100};
    static goods_t LongCar = {"LongCar", 180};
    static goods_t ghostCar = {"GhostCar", 200};
    static goods_t fuel = {"Fuel", 10};
    static goods_t normalTire = {"NormalTire", 20};
    static goods_t SuperTire = {"SuperTire", 80};
    static goods_t flag = {"flag", 9999};

    addGoods(goodsList, &normalCar);
    addGoods(goodsList, &superCar);
    addGoods(goodsList, &LongCar);
    addGoods(goodsList, &ghostCar);
    addGoods(goodsList, &fuel);
    addGoods(goodsList, &normalTire);
    addGoods(goodsList, &SuperTire);
    addGoods(goodsList, &flag);
    initCarList(carList);

    _this->goodsList = goodsList;
    _this->carList = carList;
    _this->menu = &storeMenu;
    _this->sellGoods = &sellGoodsImpl;
    _this->buyGoods = &buyGoodsImpl;
    _this->fixCar = &fixCarImpl;
    _this->fetchCar = &fetchCarImpl;
    _this->readInput = &readStoreInputImpl;
    _this->showGoods = &showGoodsImpl;

}

void storeMenu()
{
    printf("Welcome to my store!\n");
    printf("==================================\n");
    printf("\t1. Buy Goods\n\t2. Sell Goods\n\t3. Fix Cars\n\t4. Fetch Cars\n\t5. Leave\n");
    printf("==================================\n");
    printf("> ");
    fflush(stdout);
}

void readStoreInputImpl(store_t *_this, game_t *game)
{
    int ch;
    char buf[8];
    while(1)
    {
        _this->menu();
        read(0, buf, 8);
        ch = atoi(buf);
        switch(ch)
        {
            case 1:
                _this->sellGoods(_this, game);
                break;
            case 2:
                _this->buyGoods(_this, game);
                break;
            case 3:
                _this->fixCar(_this, game);
                break;
            case 4:
                _this->fetchCar(_this, game);
                break;
            case 5:
                puts("Good bye~");
                return;
        }
    }

}


void showGoodsImpl(store_t *_this)
{
    goodsList_t *curGoods = _this->goodsList;
    while(curGoods != NULL)
    {
        goods_t *goods = curGoods->goods;
        printf("Goods:\t%-20sPrice:  %d\n", goods->name, goods->price);
        curGoods = curGoods->next;
    }
    printf("which one do you want to buy?\n");
    printf("> ");
    fflush(stdout);
}

void sellGoodsImpl(store_t *_this, game_t *game)
{
    _this->showGoods(_this);
    char name[32];
    memset(name, 0, sizeof(name));
    int nread = read(0, name, 31);
    if(name[nread-1] == '\n')   
        name[nread-1] = '\0';
    else
        name[nread] = '\0';
    goods_t *goods = findGoods(name, _this);
    if(goods == NULL)
    {
        puts("We don't provide that.");
        return ;
    }
    if(game->money >= goods->price)
    {
        if(strcmp(goods->name, "NormalCar") == 0 
            || strcmp(goods->name, "SuperCar") == 0
                || strcmp(goods->name, "LongCar") == 0
                    || strcmp(goods->name, "GhostCar") == 0)
        {
            car_t *car = malloc(sizeof(car_t));
            int stability, fuel, step, type;
            
            switch(goods->name[0])
            {
                case 'N':
                    stability = 65, fuel = 130, step = 1, type = 1;
                    break;
                case 'S':
                    stability = 75, fuel = 140, step = 1, type = 1;
                    break;
                case 'L':
                    stability = 55, fuel = 150, step = 2, type = 1;
                    break;
                case 'G':
                    stability = 85, fuel = 155, step = 1, type = 1;
                    break;

            }
            initCar(car, USER_ROW + 1, USER_COL + 1,
                    stability, fuel, step, type);

            car->cost = goods->price;
            game->userCar = car;
            game->carList->addCar(car, game->carList);
            game->carList->carNums++;
        }
        else if(strcmp(goods->name, "Fuel") == 0)
        {            
            car_t *car = game->userCar;
            if(car == NULL)
            {
                puts("You must have a car\n");
                return ;
            }
            car->fuel += 10;
        }
        else if(strcmp(goods->name, "NormalTire") == 0
                 || strcmp(goods->name, "SuperTire") == 0)
        {
            car_t *car = game->userCar;
            if(car == NULL)
            {
                puts("You must have a car\n");
                return ;
            }
        }

        else if(strcmp(goods->name, "flag") == 0)
        {
            if(game->winTimes < 1000)
            {  
                puts("No! You cheated in this game! Where did your money come from?\n");
                puts("Punish for cheaters!\nYour cars are confiscated!");
                carList_t *curCar = game->carList;
                while(curCar)
                {
                    car_t *car = curCar->car;
                    if(car)
                    {
                        free(car);
                        curCar->car = NULL;
                    }
                    curCar = curCar->next;
                }
                game->carList->carNums = 0;
                game->userCar = NULL;
            }
            else
            {
                int fd;
                char buf[64];
                puts("You've earned it!");
                puts("Here is your flag!");
                fd = open("./flag", O_RDONLY);
                if(fd >= 0)
                {
                    read(fd, buf, 64);
                    write(1, buf, 64);
                }
            }
            return;
            
        }

        game->money -= goods->price;
        printf("Deal!\n");
        printf("You remained %d money\n\n", game->money);


    }
    else
    {
        puts("You don't have enough money.\n");
        return ;
    }
}

void buyGoodsImpl(store_t *_this, game_t *game)
{
    car_t *car;
    char name[32];
    memset(name, 0, sizeof(name));
    printf("We only accept cars.\nWhich car do you want to sell?\n");
    game->carList->showCars(game->carList);
    printf("> ");
    fflush(stdout);
    int nread = read(0, name, 31);
    if(name[nread-1] == '\n')   
        name[nread-1] = '\0';
    else
        name[nread] = '\0';
    car = game->carList->findCar(name, game->carList);
    if(car == NULL)
    {
        puts("You don't have this one.");
        return ;
    }
    else if(car->fixed)
    {
        puts("You can't sell it because your car is being fixed.");
        return ;
    }
    else
    {
        puts("Deal!");
        game->money += car->cost / 2 + car->performance * 2;
        game->carList->carNums--;

        game->carList->deleteCar(car, &game->carList); 
        free(car);
        if(car == game->userCar)
        {
            int found = 0;
            carList_t *cur = game->carList;
            while(cur)
            {
                if(cur->car)
                {
                    game->userCar = cur->car;
                    found = 1;
                    break;
                }
                cur = cur->next;
            }
            if(!found)
                game->userCar = NULL;
        }
    }
}

void fixCarImpl(store_t *_this, game_t *game)
{
    char name[9];
    car_t *car;
    carList_t *carList = game->carList;
    if(carList->carNums == 0)
    {
        puts("You don't have a car.");
        return ;
    }
    carList->showCars(carList);
    printf("Which one do you want to fix?\n");
    printf("> ");
    fflush(stdout);
    int nread = read(0, name, 8);
    if(name[nread-1]=='\n')
        name[nread-1] = '\0';
    else
        name[nread] = '\0';

    car = carList->findCar(name, carList);
    if(car == NULL)
    {
        puts("You don't have this one");
        return;
    }

    if(_this->carList->findCar(name, _this->carList) !=NULL )
    {
        puts("This car is being fixed now.");
        return;
    }
    car->fixTime = time(NULL);
    car->fixed = 1;
    _this->carList->addCar(car, _this->carList);
    _this->carList->carNums++;
    if(carList->carNums > 1)
    {
        car->isTaken = 1;
        carList->deleteCar(car, &carList);
        carList->carNums--;
        puts("OK! We will temporily take your car and fix it soon!");
        return;
    }
    puts("OK! We'll soon fix it!");

}

car_t * fetchCarImpl(store_t *_this, game_t *game)
{
    int     fetchTime, fixedTime, fixTime;
    int     cost, fixDifficulty;
    int     fetchHour, fetchMin, fetchSec, fixHour, fixMin, fixSec;
    
    char name[9];
    carList_t *carList = _this->carList;
    car_t *car;
    if(carList->carNums == 0)
    {
        puts("You don't have cars here.");
        return NULL;
    }
    carList->showCars(_this->carList);
    printf("Which one do you want to take?\n");
    printf("> ");
    fflush(stdout);
    int nread = read(0, name, 8);
    if(name[nread-1] == '\n')   
        name[nread-1] = '\0';
    else
        name[nread] = '\0';

    car = carList->findCar(name, _this->carList);
    if(car == NULL)
    {
        puts("We don't have this one.");
        return NULL;
    }
    fixDifficulty = car->fixDifficulty;
    
    struct tm *fixTp = localtime(&car->fixTime);
    fixHour = fixTp->tm_hour; fixMin = fixTp->tm_min; fixSec = fixTp->tm_sec;

    time_t fetchT = time(NULL);
    struct tm *fetchTp = localtime(&fetchT);
    fetchHour = fetchTp->tm_hour; fetchMin = fetchTp->tm_min; fetchSec = fetchTp->tm_sec;

    fetchTime = fetchHour * 3600 +  fetchMin * 60 + fetchSec * fixDifficulty;// 0
    fixTime   = fixHour * 3600 + fixMin * 60 + fixSec; 

    fixedTime = fetchTime - fixTime;    
    cost = 5 * fixedTime;
    if(cost > (int)game->money)
        cost = game->money;
    car->health += (int)(fixedTime * 0.4) + 50;
    game->money -= cost;

    car->fixed = 0;
    _this->carList->deleteCar(car, &_this->carList);
    _this->carList->carNums--;
    if(car->isTaken)
    {
        car->isTaken = 0;
        game->carList->addCar(car, game->carList);
        game->carList->carNums++;
    }

    printf("Your car has been fixed for %d seconds, cost is %d\n", fixedTime, cost);
    return car;

}