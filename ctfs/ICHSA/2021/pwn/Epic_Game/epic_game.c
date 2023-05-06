#include "epic_game.h"

/**log vars**/
char error_log[1024] = {0};
uint64_t write_to_log = 0;
uint64_t curr = 0;
/************/

void init_player(player* p_player, uint32_t character_type)
{
    uint64_t luck = rand;
    switch (character_type)
    {
        case 1: //Mighty warrior
        {
            strcpy(p_player->player_type, "Mighty Warrior");
            p_player->game_points = 0;
            p_player->health_points = 1000;
            p_player->shield = 100;
            p_player->strength = 500;
            p_player->luck = luck;
            break;
        }
        case 2: //Wizard
        {
            strcpy(p_player->player_type, "Wizard");
            p_player->game_points = 0;
            p_player->health_points = 1200;
            p_player->shield = 400;
            p_player->strength = 200;
            p_player->luck = luck;
            break;
        }
        case 3: //Elf
        {
            strcpy(p_player->player_type, "Elf");
            p_player->game_points = 0;
            p_player->health_points = 1000;
            p_player->shield = 500;
            p_player->strength = 300;
            p_player->luck = luck;
            break;
        }
        default:
            break;
    }
}

void log_error(char* buff)
{
    puts("Input Error\n");
    if(write_to_log)
    {
        curr += snprintf(error_log+curr, sizeof(error_log)-curr, "%s", buff);
        if (curr == sizeof(error_log))
        {
           write_to_log = false;
           //TODO: write the log buffer to file  
        }
    }
}

int main(int argc, char** argv)
{

    char buffer[BUFFER_SIZE] = {0};
    player current_player = {0};
    uint32_t character_type = 0;
    uint32_t str_length = 0;

    Enemy enemy_arr[3] = {
        {"Dragon", 10000, 10000, 10000}, 
        {"Demon", 200, 100, 100}, 
        {"Evil snake", 100, 50, 50}
    };

    srand(time(NULL));
    
    write_to_log = true;

    puts("Hello epic warrior, it's time to begin your quest\n");
    puts("Choose your character:\n" \
         "\t1 - Mighty warrior\n" \
         "\t2 - Wizard        \n" \
         "\t3 - Elf           \n");
    puts("Your Choice:");

    
    if(fgets (buffer, BUFFER_SIZE, stdin) != NULL) {
        character_type = strtoul(buffer, NULL, 10);
        if(character_type > 0 && character_type < 4){
            init_player(&current_player, character_type);
        }else{
            log_error(buffer);
            init_player(&current_player, 1 + (rand()%3));
        }
    }

    memset(buffer, 0x00, BUFFER_SIZE);

    printf("Choose your character name (limit to %d chars)\n", NAME_MAX_SIZE);
    puts("Your Choice:");

    if(fgets (buffer, BUFFER_SIZE, stdin) != NULL) {
        buffer[BUFFER_SIZE-1] = '\x00';
        str_length = strlen(buffer);
        if (str_length > 0 && str_length <= NAME_MAX_SIZE+1){
            memcpy(current_player.name, buffer, str_length-1);
        }else{
            log_error(buffer);
            memcpy(current_player.name, buffer, NAME_MAX_SIZE);
        }
    }

    printf("Hello %s The %s!!!\n", current_player.name, current_player.player_type);
    printf("Your health is %d pt.\n"\
           "Your shield is %d pt.\n"\
           "Your strength is %d pt.\n"\
           "Your lucky number is %lld\n",
           current_player.health_points,
           current_player.shield,
           current_player.strength,
           current_player.luck);
    printf("You will need %d points to get the flag\n", POINTS_FOR_FLAG);
    puts("Good luck, the kingdom trust you!!\n");

    /*****The Game******/ 
    while (current_player.health_points > 0)
    {
        if(current_player.game_points >= POINTS_FOR_FLAG)
        {
            //read and print flag
            char flag_buf[64] = {0};
            int fd = open("flag.txt", O_RDONLY);
            read(fd, flag_buf, sizeof(flag_buf));
            puts(flag_buf);
            break;
        }
        int r = rand()%3;
        Enemy tmp_enemy = enemy_arr[r];
        printf("You meet a %s!!!\n", tmp_enemy.name);
        bool run = false;
        while(tmp_enemy.health_points > 0 && current_player.health_points > 0 && !run){
            puts(current_player.name);
            puts("choose your move:\n" \
            "1 - hit \n" \
            "2 - protect\n" \
            "3 - run\n");

            memset(buffer, 0x00, BUFFER_SIZE);

            puts("Your Choice:");

            if(fgets (buffer, BUFFER_SIZE, stdin) != NULL) {
                uint32_t move = strtoul(buffer, NULL, 10);
                //play
                switch (move)
                {
                case 1: //hit
                    if(current_player.health_points > tmp_enemy.strength){
                        current_player.health_points -= tmp_enemy.strength;
                    }else{
                        current_player.health_points = 0;
                    }

                    if(tmp_enemy.health_points > current_player.strength){
                        tmp_enemy.health_points -= current_player.strength;
                    }else{
                        tmp_enemy.health_points = 0;
                        current_player.game_points++;
                        puts("you killed an evil creature, kudos!!!\n");
                        printf("your current health %d\n", current_player.health_points);
                    }
                    break;

                case 2: //protect
                    if(tmp_enemy.strength <= current_player.shield || current_player.luck > LUCK_LIMIT){
                        printf("your current health %d\n", current_player.health_points);
                    }else if(current_player.health_points > tmp_enemy.strength - current_player.shield){
                        current_player.health_points -= (tmp_enemy.strength - current_player.shield);
                        printf("your current health %d\n", current_player.health_points);
                    }else{
                        current_player.health_points = 0;
                    }
                    break;

                case 3: //run
                    puts("You run away, no glory in that!!!\n");
                    run = true;
                    break;
                    
                default:
                    log_error(buffer);
                    break;
                }
            }
        }

        if(current_player.health_points == 0)
        {
            printf("R.I.P %s The %s\nYou were a brave warrior but not enough to get a flag\n", 
            current_player.name, current_player.player_type);
        }
    }
}