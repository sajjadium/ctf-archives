
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>


#define BASE_PATH "/home/game/"
#define DEFAULT_SAVEFILE "gamesave"

struct player_struct {
    unsigned short current_score;
    unsigned short high_score;
    unsigned short username_size;
    unsigned short current_guess;
    char *username;
} player_struct;

struct linked_list_entry {
    struct linked_list_entry* fw;
    struct linked_list_entry* bk;
    struct player_struct player;
} linked_list_entry;
 
struct linked_list_head {
    struct linked_list_entry* fw;
} linked_list_head;

// Code stolen from stackoverflow
// https://stackoverflow.com/questions/822323/how-to-generate-a-random-int-in-c
int random_number(int min_num, int max_num)
{
    int result = 0, low_num = 0, hi_num = 0;
    if (min_num < max_num)
    {
        low_num = min_num;
        hi_num = max_num + 1; // include max_num in output
    } else {
        low_num = max_num + 1; // include max_num in output
        hi_num = min_num;
    }
    result = (rand() % (hi_num - low_num)) + low_num;
    return result;
}


void print_rules() {
    puts("[+] Welcome to our dice game :)");
    puts("[+] The rules are as follows:");
    puts("\t- There are 10 rounds to a game");
    puts("\t- Each player chooses a number from 1 to 6 each round");
    puts("\t- There will then be 6 dice throws");
    puts("\t- Each player gets one point per dice, that shows their number");
}

void print_options() {
    puts("[+] Please choose what you want to do:");
    puts("\t1) Play game round");
    puts("\t2) Create player");
    puts("\t3) List players and score");
    puts("\t4) Rename player");
    puts("\t5) Remove player");
    puts("\t6) List rules");
    puts("\t7) Exit game");
}

int read_option() {
    char line[256];
    int i = 0;
    if (fgets(line, sizeof(line), stdin)) {
        if (1 == sscanf(line, "%d", &i)) {
            return i;
        }
        else {
            return -1;
        }
    }
    return -1;
}

// Function, that mainly reads the username from stdin
void read_input(char **buffer, unsigned short *size) {
    char* input = *buffer;
    
    // Check if input buffer is already initialized
    // If it is not we allocate 16 bytes as the initial buffer
    if(*size == 0) {
        input = malloc(16);
        if(input == NULL) {
            puts("[-] malloc failed");
            return;
        }
        *size = 16;
    }

    size_t len = 0;
    
    // Reading in one char at a time
    int ch = 0;
    //flush(stdout);
    while(EOF!=(ch=fgetc(stdin)) && ch != '\n'){
        input[len++]=ch;
        if(len==(*size)){
            if(*size < 2048) {
                *size = *size + 16;
                input = realloc(input, *size);
                if(input == NULL) {
                    puts("[-] realloc failed");
                    return;
                }
            }
            else {
                input[*size-1] = 0;
                *buffer = input;
                return;
            }
        }
    }

    // Terminate string
    input[len]='\0';
    *buffer = input;
    return;
}


void rename_player(struct player_struct* player) {
    puts("[+] Please enter the username");
    read_input(&(player->username), &(player->username_size));
    puts("[+] Set username to:");
    if(player->username != NULL)
        puts(player->username);
}

void print_players(struct linked_list_head *head) {
    struct linked_list_entry* current_entry = head->fw;
    puts("[+] Printing all user information");
    unsigned int player_number = 0;
    while(current_entry != NULL) {
        printf("[+] Printing information of player number %d\n", player_number++);
        printf("\t[+] Username: %s\n", current_entry->player.username);
        printf("\t[+] Current score: %d\n", current_entry->player.current_score);
        printf("\t[+] High score: %d\n", current_entry->player.high_score);
        current_entry = current_entry->fw;
    }
}

void delete_player(struct linked_list_entry* entry) {
    // Set the fw pointer of the previous element to our fw pointer
    entry->bk->fw = entry->fw;
    
    // Check if our fw pointer is null
    if (entry->fw != NULL) {
        // If our fw pointer is not null we need to update the bk pointer of the next element
        entry->fw->bk = entry->bk;
    }

    // We need to free the buffer, that contains our username
    puts("[+] Freeing username");
    free(entry->player.username);
    
    // We also need to free the complete struct
    puts("[+] Freeing struct");
    free(entry);
}

void create_player(struct linked_list_head* head) {
    struct linked_list_entry *new_entry =  malloc(sizeof(linked_list_entry));
    if(new_entry == NULL) {
        puts("[-] malloc failed");
        return;
    }
    new_entry->player.current_score = 0;
    new_entry->player.high_score = 0;
    new_entry->player.current_guess = 0;
    new_entry->player.username_size = 0;
    new_entry->player.username = NULL;
    rename_player(&(new_entry->player));
    if(head->fw == NULL) {
        new_entry->fw = NULL;
        new_entry->bk = (struct linked_list_entry*)head;
        head->fw = new_entry;
    }
    else {
        head->fw->bk = new_entry;
        new_entry->fw = head->fw;
        new_entry->bk = (struct linked_list_entry*)head;
        head->fw = new_entry;
    }
}

struct linked_list_entry* choose_player(struct linked_list_head* head) {
    puts("[+] Please provide the number of the player:");
    int option = read_option();
    if (option != -1) {
        struct linked_list_entry* current_entry = head->fw;
        unsigned int player_number = 0;
        while(current_entry != NULL) {
            if(player_number == option) {
                return current_entry;
            }
            current_entry = current_entry->fw;
            player_number++;
        }

        return NULL;
    }
    else {
        return NULL;
    }
}

void play_game_round(struct linked_list_head* head) {
    // Get one guess for each player in the list
    struct linked_list_entry* current_entry = head->fw;
    puts("[+] Gathering guesses");
    while(current_entry != NULL) {
        printf("[+] Please provide your guess %s\n", current_entry->player.username);
        while(1) {
            int tmp_guess = read_option();
            if ((tmp_guess > 6) || (tmp_guess < 1) ) {
                continue;
            }
            current_entry->player.current_guess = tmp_guess;
            break;
        }
        current_entry = current_entry->fw;
    }
    // Throw the 6 dices
    puts("[+] Throwing dice");
    int dice_array[6];
    for(int i = 0; i < 6; i++ ){
        dice_array[i] = random_number(1,6);
        printf("\t [+] Number %d: %d \n", i, dice_array[i]);
    }

    // Evaluate the guesses and update the score for each player
    current_entry = head->fw;
    while(current_entry != NULL) {
        unsigned int tmp_score = 0;
        for(int i = 0; i < 6; i++ ){
            if(current_entry->player.current_guess == dice_array[i]) {
                tmp_score++;
            }
        }
        current_entry->player.current_score = current_entry->player.current_score + tmp_score; 
        printf("\t [+] %s got %d points. Current score is %d\n", current_entry->player.username, tmp_score, current_entry->player.current_score);
        current_entry = current_entry->fw;
    }
}

void evaluate_game(struct linked_list_head* head) {
    // Iterate over all players
    struct linked_list_entry* current_entry = head->fw;
    puts("[+] Game finished. Evaluating scores");
    unsigned int highscore = 0;
    char* winner = NULL;
    // Find player with high score
    while(current_entry != NULL) {
        // Compare high score to current score and set current score to 0
        int tmp_score = current_entry->player.current_score;
        current_entry->player.current_score = 0;
        if (tmp_score > current_entry->player.high_score) {
            current_entry->player.high_score = tmp_score;
        } 
        if (tmp_score > highscore) {
            highscore = tmp_score;
            winner = current_entry->player.username;
        }
        current_entry = current_entry->fw;
    }
    printf("[+] %s won with a score of %d\n", winner, highscore);
}

int main(int argc, char *argv[])  {
    
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);

    // Initialize our linked list of players
    struct linked_list_head player_list;
    player_list.fw = NULL;

    puts("[+] Starting game");
    
    // Start by printing the rules
    print_rules();

    // Choose option
    int round_number = 0;
    int option = 0;
    while(1) {
        print_options();
        option = read_option();

        // Play game
        if(option == 1) {
            if(player_list.fw == NULL) {
                puts("[-] Please create at least one player");
                continue;
            }
            play_game_round(&player_list);
            if (round_number == 9) {
                evaluate_game(&player_list);
                round_number = 0;
            }
            else {
                round_number++;
            }
        }
        // Add new user
        else if (option == 2) { 
            puts("[+] Creating new player");
            create_player(&player_list);
        }
        // List players
        else if (option == 3) {
            print_players(&player_list);        
        }
        // Rename player
        else if (option == 4) {
            // Print all player names with a number
            print_players(&player_list);
            struct linked_list_entry* player = choose_player(&player_list);
            if (player != NULL)
                rename_player(&(player->player));
            else 
                puts("[-] Could not retrieve player");
        }
        // Remove player
        else if (option == 5) {
            print_players(&player_list);
            struct linked_list_entry* player = choose_player(&player_list);
            if(player != NULL)
                delete_player(player);
        }
        else if(option == 6) {
            print_rules();
        }
        // Exit
        else {
            puts("Goodbye :)");
            return 0;
        }

    }
}