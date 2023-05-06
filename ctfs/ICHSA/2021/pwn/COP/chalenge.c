#include "chalenge.h"
// Functions declaration start

void init_game()
{
    
    // Allocate some memory for the game_ctx
    game_ctx = mmap(GAME_CTX_ID, PAGE_SIZE, PROT_WRITE | PROT_READ , MAP_PRIVATE | MAP_ANONYMOUS, -1,0);
    
    if(game_ctx == NULL)
    {
        printf("Somthing whent wrong while allocation memory for game_ctx, please try again!");
        exit(-1);
    }

    // Set ctx to default values
    memset(game_ctx, 0x0, sizeof(*game_ctx));
    strncpy(game_ctx->player_name, DEFAULT_PLAYER_NAME, sizeof(DEFAULT_PLAYER_NAME));
   
    // Allocate some memory for the game_ctx->array_of_plays
    game_ctx->array_of_plays = mmap(ARRAY_OF_PLAYS_ID, PAGE_SIZE, PROT_WRITE | PROT_READ , MAP_PRIVATE | MAP_ANONYMOUS, -1,0);
    if(game_ctx->array_of_plays == NULL)
    {
        printf("Somthing whent wrong while allocation memory for game_ctx->list_of_plays, please try again!");
        exit(-1);
    }
    
    // initializing pseudo-random values and populate array_of_plays
    srand(0);
    for(uint8_t i = 0; i < ARRAY_OF_PLAYS_MAX_SIZE; i++)
    {
        game_ctx->array_of_plays[i].id = i;
        game_ctx->array_of_plays[i].handsign = (rand() % MAX_HANDSIGNS) + MIN_HANDSIGN;
        game_ctx->array_of_plays[i].animation_function = print_ascii;
    }
	
	change_permission_game_ctx(false);
	change_permission_array_of_plays(false);
    
}

bool change_permission_address(void * address, bool writable)
{   
    bool status = false;
    int prot = (writable) ? PROT_WRITE | PROT_READ : PROT_READ;
    
    do
    {   

        // round down address if necessary
        address = (void *)((uint64_t) ROUND_DOWN(address,PAGE_SIZE));
  
        if(NULL == game_ctx)
        {
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        }
        
        if(0 != mprotect(address, PAGE_SIZE, prot))
        {
            printf("FAIL:%d\n", errno);
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        }
        
        status = true;

    }while(false);
    
    return status;
}

bool change_permission_game_ctx(bool writable)
{   
    return change_permission_address(GAME_CTX_ID, writable);
}

bool change_permission_array_of_plays(bool writable)
{   
    return change_permission_address(ARRAY_OF_PLAYS_ID, writable);
}

bool is_player1_winner(enum handsigns player1, enum handsigns player2)
{
    bool status = false;
    
    do
    {
        if( (player1 == ROCK && player2 == SCISSORS) ||
            (player1 == SCISSORS && player2 == PAPPER) ||
            (player1 == PAPPER && player2 == ROCK) )
        {
            status = true;
        }
            
    }
    while(false);
    
    return status;
}

bool is_player2_winner(enum handsigns player1, enum handsigns player2)
{
    return is_player1_winner(player2, player1);
}

enum menu_input_options print_menu_and_get_user_input_option()
{   
    enum menu_input_options user_input = INVALID_OPTION;
    char input_buffer[INPUT_BUFF_SIZE] = {0};
    
    do
    {
        
        printf("+===============================================+\n");
        printf("|   Wellcome to my Rock-Paper-Scissors's game   |\n");
        printf("+-----------------------------------------------+\n");
        printf("| Current score: \n");
        printf("| %s: %ld Points \n",game_ctx->player_name , game_ctx->user_points);
        printf("| Computer: %ld Points \n", game_ctx->pc_points);
        printf("+-----------------------------------------------+\n");
        printf("| Options:\n");
        printf("| 1) Display game rules ------------- (0 Points)\n");
        printf("| 2) Play next round ---------------- (0 Points)\n");
        printf("| 3) Skip N rounds ------------------ (%u Points)\n",POINTS_TO_CHANGE_SKIP_N_ROUNDS);
        printf("| 4) Enable Ascii-art --------------- (%u Points)\n",POINTS_TO_ENABLE_ASCII_ART);
        printf("| 5) Change user name --------------- (%u Points)\n",POINTS_TO_CHANGE_USERNAME);
        printf("| 6) Print the flag! ------- (%u Points)\n",POINTS_TO_PRINT_FLAG);
        printf("| 7) Exit --------------------------- (0 Points)\n");
        printf("+-----------------------------------------------+\n");
        printf("| Please chose an option [ ]\b\b");

		fflush(NULL);
		
        if(NULL == fgets(input_buffer, INPUT_BUFF_SIZE,stdin))
        {
            user_input = INVALID_OPTION;
            break;
        }
        
        if(1 != sscanf(input_buffer, "%u" , &user_input))
        {
            user_input = INVALID_OPTION;
            break;
        }

        // system("clear");
        printf("+===============================================+\n");
        
        //ToDo remove this
        printf("| User input is: %u\n", user_input);
        
        if( user_input < MIN_OPTION || user_input >= MAX_OPTION)
        {
            user_input = INVALID_OPTION;
            break;
        }
        
    }while(false);
    
    return user_input;
    
}

void print_rules()
{
    printf("+-----------------------------------------------+\n");
    printf("| The rules are simple:\n");
    printf("| * Each player chose between: ROCK, PAPER and SCISSORS\n");
    printf("| * ROCK beats SCISSORS\n");
    printf("| * SCISSORS beats PAPER\n");
    printf("| * PAPER beats ROCK\n");
    printf("| * Each win you will receive a point\n");
    printf("| * You have up to %u tries to make points\n",ARRAY_OF_PLAYS_MAX_SIZE);
    printf("| * Make %u points to be able to skip N rounds!\n",POINTS_TO_CHANGE_SKIP_N_ROUNDS);
    printf("| * Make %u points to be able to change your username!\n",POINTS_TO_CHANGE_USERNAME);
    printf("| * Make %u points to be able to enable ASCII Art!\n",POINTS_TO_ENABLE_ASCII_ART);
    printf("| * Make %u points to get the flag!\n",POINTS_TO_PRINT_FLAG);
    printf("+-----------------------------------------------+\n");

}

bool play_next_round()
{
    bool status = false;
    char input_buffer[INPUT_BUFF_SIZE] = {0};
    enum handsigns handsig_input = INVALID_HANDSIGN;
    struct play current_play = {0};
    do
    {
        if( game_ctx->current_play == ARRAY_OF_PLAYS_MAX_SIZE)
        {
            printf("+-----------------------------------------------+\n");
            printf("| I'm sorry,\n");
            printf("| You have reached the maximum number of games\n");
            printf("| Try again next time\n");
            SET_STATUS_TO_FALSE_AND_BREAK(status)
            
        }

        printf("+-----------------------------------------------+\n");
        printf("| Game #%d\n", game_ctx->current_play);
        printf("+-----------------------------------------------+\n");
        printf("| What do you want to do?\n");
        printf("| %d) ROCK\n",ROCK);
        printf("| %d) PAPPER\n",PAPPER);
        printf("| %d) SCISSORS\n",SCISSORS);
        printf("+-----------------------------------------------+\n");
        printf("| Please chose an option [ ]\b\b");

		fflush(NULL);

        if(NULL == fgets(input_buffer, INPUT_BUFF_SIZE,stdin))
            SET_STATUS_TO_FALSE_AND_BREAK(status)   
        
        if(1 != sscanf(input_buffer, "%u" , &handsig_input))
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        
        current_play = game_ctx->array_of_plays[game_ctx->current_play];
        
        //ToDo remove this
        printf("| Computer chosed: %u\n", current_play.handsign);
        printf("| You chosed: %u\n", handsig_input);
        
        if( handsig_input < MIN_HANDSIGN || handsig_input > MAX_HANDSIGNS)
        {
            printf("| Invalid option: %u\n", handsig_input);
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        }
        
        
        if(is_player1_winner(current_play.handsign, handsig_input))
        {
            printf("| Point goes to: Computer\n");
            CHANGE_GAME_CTX_FIELD(pc_points, game_ctx->pc_points+1)

        }
        
        else if(is_player2_winner(current_play.handsign, handsig_input))
        {
            printf("| Point goes to: %s\n", game_ctx->player_name);
            CHANGE_GAME_CTX_FIELD(user_points, game_ctx->user_points+1)
        }        
        else
        {
            printf("| It is a tie\n");
            printf("| Point goes to: no one\n");
        }
        // if ascii art enabled, call function ptr
        if(game_ctx->ascii_art_enabled)
        {
            current_play.animation_function(current_play.handsign, handsig_input);
        }
        
        CHANGE_GAME_CTX_FIELD(current_play, game_ctx->current_play+1)
        
        status = true;
        
    }while(false);

    change_permission_game_ctx(false);
    return status;

}

bool skip_n_rounds()
{
    bool status = false;
    char input_buffer[INPUT_BUFF_SIZE] = {0};
    uint8_t rounds_to_skip = 0;
    
    do
    {
        if(game_ctx->user_points < POINTS_TO_CHANGE_SKIP_N_ROUNDS)
        {
            printf("| You don't have enouth points for this command\n");
            printf("| You have: %ld but you need at least %u\n",game_ctx->user_points, POINTS_TO_CHANGE_SKIP_N_ROUNDS);
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        }
        

        printf("+-----------------------------------------------+\n");
        printf("| Please chose the number of games to skip [  ]\b\b\b");

		fflush(NULL);

        if(NULL == fgets(input_buffer, INPUT_BUFF_SIZE,stdin))
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        
        if(1 != sscanf(input_buffer, "%hhu" , &rounds_to_skip))
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        
        printf("| You chose to skip %u rounds\n", rounds_to_skip);

        // Check for uint8_t integer overflow
        if(OVERFLOW_CHECK(rounds_to_skip,ARRAY_OF_PLAYS_MAX_SIZE))
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        
        if(game_ctx->current_play + rounds_to_skip > ARRAY_OF_PLAYS_MAX_SIZE)
            SET_STATUS_TO_FALSE_PRINT_AND_BREAK(status, "| Overflow - Not jumping\n")
        
        CHANGE_GAME_CTX_FIELD(current_play, game_ctx->current_play + rounds_to_skip)
        
        status = true;
    }    
    while(false);
    change_permission_game_ctx(false);
    
    return status;
}

bool enable_ascii_art()
{
    bool status = false;
    do
    {
        if(game_ctx->user_points < POINTS_TO_ENABLE_ASCII_ART)
        {
            printf("| You don't have enouth points for this command\n");
            printf("| You have: %ld but you need at least %u\n",game_ctx->user_points, POINTS_TO_ENABLE_ASCII_ART);
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        }
        
        printf("| ASCII Art: enable\n");
        CHANGE_GAME_CTX_FIELD(ascii_art_enabled, true)
        
        status = true;
        
    }while(false);
    
    return status;
}

bool change_user_name()
{   
    bool status = false;
    char * curr_ptr = NULL;
    
    do
    {
        if(game_ctx->user_points < POINTS_TO_CHANGE_USERNAME)
        {
            printf("| You don't have enouth points for this command\n");
            printf("| You have: %ld but you need at least %u\n",game_ctx->user_points, POINTS_TO_CHANGE_USERNAME);
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        }
    
        printf("| Enter your new username: ");
        
        // change ctx to R/W
        change_permission_game_ctx(true);

		fflush(NULL);

        //Get user input
        if(NULL == fgets(game_ctx->player_name, PLAYER_NAME_SIZE, stdin))
            SET_STATUS_TO_FALSE_AND_BREAK(status)

        //remove /n from name, if exists
        curr_ptr = game_ctx->player_name;
        
        while(*curr_ptr)
        {

            if(*curr_ptr == '\n')
            {                
                *curr_ptr = 0;
                break;
            }
            curr_ptr++;
        }

		// move ctx to RO
    	change_permission_game_ctx(false);
		
        status = true;
    
    }while(false);
    
	change_permission_game_ctx(false);
    return status;
}

bool print_flag()
{
    bool status = false;
    char flag[FLAG_SIZE] = {0};
    char * flag_ptr = NULL;
    FILE *fd = NULL;

    do
    {
        if(game_ctx->user_points < POINTS_TO_PRINT_FLAG)
        {
            printf("| You don't have enouth points for this command\n");
            printf("| You have: %ld but you need at least %u\n",game_ctx->user_points, POINTS_TO_PRINT_FLAG);
            SET_STATUS_TO_FALSE_AND_BREAK(status)
        }
        
        fd = fopen(FLAG_FILE, "r");
        if(fd == NULL)
        {
            printf("| Somthing whent wrong while opeining the file %s\n", FLAG_FILE);
            exit(-1);
        }
        
        flag_ptr = fgets(flag, FLAG_SIZE, fd);
        
        if(flag_ptr == NULL)
        {
            printf("| Somthing whent wrong while reading the file %s\n", FLAG_FILE);
            exit(-1);
        }
        
        printf("| The flag is:%s\n", flag);
        fflush(NULL);
        
        bool status = false;
    }while(false);
    
    return status;
}

void print_ascii(enum handsigns pc, enum handsigns user)
{

    printf("%s",pc_vs_user);
    
    if(pc == ROCK && user == ROCK)
        printf("%s",rock_vs_rock);
    if(pc == ROCK && user == PAPPER)
        printf("%s",rock_vs_paper);
    if(pc == ROCK && user == SCISSORS)
        printf("%s",rock_vs_scissors);
    if(pc == PAPPER && user == ROCK)
        printf("%s",papper_vs_rock);        
    if(pc == PAPPER && user == PAPPER)
        printf("%s",papper_vs_papper);       
    if(pc == PAPPER && user == SCISSORS)
        printf("%s",papper_and_scissors);
    if(pc == SCISSORS && user == ROCK)
        printf("%s",scissors_vs_rock);
    if(pc == SCISSORS && user == PAPPER)
        printf("%s",scissors_and_papper);
    if(pc == SCISSORS && user == SCISSORS)
        printf("%s",scissors_vs_scissors);
}

int main()
{   

    enum menu_input_options user_input = INVALID_OPTION;
    bool status = true;
	
    init_game();
    
    while(true)
    {
        user_input = print_menu_and_get_user_input_option();
        
        switch (user_input)
        {
            case DISPLAY_GAME_RULES:
                print_rules();
				status = true;
				break;
                
            case PLAY_NEXT_ROUND:
                status = play_next_round();

                break;
                
            case SKIP_N_ROUNDS:
                status = skip_n_rounds();
                break;
                
            case ENABLE_ASCII_ART:
                status = enable_ascii_art();
                break;
                
            case CHANGE_USER_NAME:
                status = change_user_name();
                break;
                
            case PRINT_FLAG:
                status = print_flag();
                break;
            
            case EXIT:
                printf("| Exiting, bye bye!\n");
                printf("+-----------------------------------------------+\n");
                exit(0);
                break;
                                     
            case INVALID_OPTION:
            default:
				status = false;
                
        }

		if(!status)
		{
			printf("| Invalid input, bye bye!\n");
            printf("+-----------------------------------------------+\n");
            exit(-1);
		}
    
    }
    
    return 0;
    
}


