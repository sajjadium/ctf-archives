/**************************************************************
@Program: battleship.c                                        *
@Version: 1.00                                                *
@Description: Player v.s. Computer Battleship Game            *
@Run with: ./battleship 600 win_map.txt                       *
***************************************************************/

#include <stdio.h>
#include <stdlib.h>

/* Global Var For Functions */
int g_map_cols = 0;
int g_map_rows = 0;
int g_shot_counter = 1;
int g_num_ships_hit = 0;

/* Fuction Prototypes */
void read_map(FILE *fp, char master[][g_map_cols]);
void print_map(char arr[][g_map_cols]);
void play_game(char master[][g_map_cols], char player[][g_map_cols], int max_shots);
int input_check(char master[][g_map_cols], char player[][g_map_cols], int in_rows, int in_cols);
int num_ships(char master[][g_map_cols]);
int map_checker(char master[][g_map_cols]);
int flag(char master[][g_map_cols]);

int main(int argc, char const *argv[]) {
    /* Set Max Number of Shots */
    int shot_max = atoi(argv[1]);

    /* Input File From Command Line */
    FILE *fp1 = fopen(argv[2], "r");

    /* File is Valid Check */
    if(fp1 == NULL){
        printf("File Could Not Be Read\n");
        exit(-1);
    }

    /* Read Rows / Cols from File */
    fscanf(fp1, "%d %d", &g_map_rows, &g_map_cols);

    char player_map[g_map_rows][g_map_cols];
    char master_map[g_map_rows][g_map_cols];

    /* Fill Player Map to be Blank */
    for (int rows = 0; rows < g_map_rows; rows++) {
      for (int cols = 0; cols < g_map_cols; cols++) {
        player_map[rows][cols]='~';
      }
    }

    /* Fill Master Map */
    read_map(fp1, master_map);

    /* Close File Pointer */
    fclose(fp1);

    /* Find Max Ships */
    int number_ships = num_ships(master_map);

    /* Make sure map only contains '~' and 'B' */
    if (map_checker(master_map)==-1) {
      printf("Map contains errors, please try with a new map\n");
      exit(-1);
    }

    /* Make sure more shots than ships */
    if (number_ships>shot_max) {
      printf("Not enough shots to win, please try again!\n");
      exit(-1);
    }

    /* Check If Flag */
    printf("Flag: %i\n", flag(master_map));


    while(g_shot_counter <= shot_max+1){
      /* Lose Condition */
      if(g_shot_counter==shot_max+1){
        printf("Map\n\n");
        print_map(player_map);
        printf("Captain, we ran out of ammo. You lose!\n");
        exit(0);
      }
      play_game(master_map, player_map, shot_max);
      /* Win Condition */
      if(g_num_ships_hit==number_ships){
        printf("Map\n\n");
        print_map(player_map);
        printf("Captain, we have sunk all the battleships. You win!\n");
        exit(0);
      }
    }


    printf("\n");
    return 0;
}

void read_map(FILE *fp, char master[][g_map_cols]){
  for (int rows = 0; rows < g_map_rows; rows++){
		for (int cols = 0; cols < g_map_cols; cols++){
			fscanf(fp, "\n%c \n\t", &master[rows][cols]);
      /* (\n & \t) swallows the newline/tab character not taking up space in array */
		}
	}
}

int num_ships(char master[][g_map_cols]){
  int ship_count = 0;
  for (int i = 0; i < g_map_rows; i++) {
    for (int j = 0; j < g_map_cols; j++) {
      if (master[i][j]=='B') {
        ship_count++;
      }
    }
  }
  return ship_count;
}

int map_checker(char master[][g_map_cols]){
  for (int rows = 0; rows < g_map_rows; rows++) {
    for (int cols = 0; cols < g_map_cols; cols++) {
      if ((master[rows][cols]!='B')&&(master[rows][cols]!='~')) {
        return -1;
      }
    }
  }
  return 1;
}

void print_map(char arr[][g_map_cols]){
  for (int rows = 0; rows < g_map_rows; rows++){
		for (int cols = 0; cols < g_map_cols; cols++){
			printf("%c", arr[rows][cols]);
		}
  printf("\n");
	}
}

void play_game(char master[][g_map_cols], char player[][g_map_cols], int max_shots){
  /* Print Map & Shots */
  printf("Map\n\n");
  print_map(player);
  printf("%d shots remaining.\n", max_shots-g_shot_counter+1);

  /* Get User Input */
  int user_in_row = 0, user_in_col = 0;
  printf("Captain, please enter coordinates: ");
  scanf("%d %d", &user_in_row, &user_in_col);

  /* Check User Input */
  while (input_check(master, player, user_in_row, user_in_col)!=1) {
    if(input_check(master, player, user_in_row, user_in_col)==-1){
      printf("Out of Range\n");
      printf("Captain, please enter coordinates: ");
      scanf("%d %d", &user_in_row, &user_in_col);
    }
    if (input_check(master, player, user_in_row, user_in_col)==-2) {
      printf("Captian, you've already shot in that position!\n");
      printf("Captain, please enter coordinates: ");
      scanf("%d %d", &user_in_row, &user_in_col);
    }
  }
  /* See if it is a Hit or Miss */
  if(input_check(master, player, user_in_row, user_in_col)==1){
    if (master[user_in_row][user_in_col]=='B') {
      printf("HIT!\n\n");
      player[user_in_row][user_in_col]='H';
      g_num_ships_hit++;
    } else {
      printf("MISS!\n\n");
      player[user_in_row][user_in_col]='M';
    }
  }
  g_shot_counter++;

}

int input_check(char master[][g_map_cols], char player[][g_map_cols], int in_rows, int in_cols){
  if ((in_rows>=g_map_rows)||(in_cols>=g_map_cols)) {
    return -1;
  }
  if ((in_rows<0)||(in_cols<0)) {
    return -1;
  }
  if ((player[in_rows][in_cols]=='H')||(player[in_rows][in_cols]=='M')) {
    return -2;
  }
  return 1;
}


int flag(char master[][g_map_cols]) {
  int is_flag = 0; // 0 = True, 1 = False
  
  // Check Row #1
  for(int i = 0; i < g_map_cols; i++) {
    if(master[0][i] != '~'){
      is_flag = 1;
    }
  }

  // Check Row #9
  for(int i = 0; i < g_map_cols; i++) {
    if(master[8][i] != '~'){
      is_flag = 1;
    }
  }

  // Check Row #2
  if(is_flag == 0) {
    if(master[1][2] != 'B') {
      is_flag = 1;
    }
    if(master[1][3] != 'B') {
      is_flag = 1;
    }
    if(master[1][4] != 'B') {
      is_flag = 1;
    }
    if(master[1][5] != 'B') {
      is_flag = 1;
    }
    if(master[1][6] != 'B') {
      is_flag = 1;
    }
    if(master[1][9] != 'B') {
      is_flag = 1;
    }
    if(master[1][16] != 'B') {
      is_flag = 1;
    }
    if(master[1][19] != 'B') {
      is_flag = 1;
    }
    if(master[1][20] != 'B') {
      is_flag = 1;
    }
    if(master[1][21] != 'B') {
      is_flag = 1;
    }
    if(master[1][22] != 'B') {
      is_flag = 1;
    }
    if(master[1][23] != 'B') {
      is_flag = 1;
    }
    if(master[1][26] != 'B') {
      is_flag = 1;
    }
    if(master[1][27] != 'B') {
      is_flag = 1;
    }
    if(master[1][28] != 'B') {
      is_flag = 1;
    }
    if(master[1][29] != 'B') {
      is_flag = 1;
    }
    if(master[1][30] != 'B') {
      is_flag = 1;
    }
    if(master[1][31] != 'B') {
      is_flag = 1;
    }
    if(master[1][32] != 'B') {
      is_flag = 1;
    }
    if(master[1][34] != 'B') {
      is_flag = 1;
    }
    if(master[1][35] != 'B') {
      is_flag = 1;
    }
    if(master[1][36] != 'B') {
      is_flag = 1;
    }
    if(master[1][37] != 'B') {
      is_flag = 1;
    }
    if(master[1][38] != 'B') {
      is_flag = 1;
    }
    if(master[1][39] != 'B') {
      is_flag = 1;
    }
    if(master[1][40] != 'B') {
      is_flag = 1;
    }
    if(master[1][45] != 'B') {
      is_flag = 1;
    }
    if(master[1][48] != 'B') {
      is_flag = 1;
    }
    if(master[1][49] != 'B') {
      is_flag = 1;
    }
    if(master[1][50] != 'B') {
      is_flag = 1;
    }
    if(master[1][51] != 'B') {
      is_flag = 1;
    }
    if(master[1][52] != 'B') {
      is_flag = 1;
    }
    if(master[1][55] != 'B') {
      is_flag = 1;
    }
    if(master[1][56] != 'B') {
      is_flag = 1;
    }
    if(master[1][57] != 'B') {
      is_flag = 1;
    }
    if(master[1][58] != 'B') {
      is_flag = 1;
    }
    if(master[1][59] != 'B') {
      is_flag = 1;
    }
    if(master[1][60] != 'B') {
      is_flag = 1;
    }
    if(master[1][61] != 'B') {
      is_flag = 1;
    }
    if(master[1][63] != 'B') {
      is_flag = 1;
    }
    if(master[1][69] != 'B') {
      is_flag = 1;
    }
    if(master[1][71] != 'B') {
      is_flag = 1;
    }
    if(master[1][76] != 'B') {
      is_flag = 1;
    }
    if(master[1][86] != 'B') {
      is_flag = 1;
    }
    if(master[1][87] != 'B') {
      is_flag = 1;
    }
    if(master[1][88] != 'B') {
      is_flag = 1;
    }
    if(master[1][89] != 'B') {
      is_flag = 1;
    }
    if(master[1][90] != 'B') {
      is_flag = 1;
    }
    if(master[1][91] != 'B') {
      is_flag = 1;
    }
    if(master[1][92] != 'B') {
      is_flag = 1;
    }
    if(master[1][94] != 'B') {
      is_flag = 1;
    }
    if(master[1][101] != 'B') {
      is_flag = 1;
    }
    if(master[1][106] != 'B') {
      is_flag = 1;
    }
    if(master[1][110] != 'B') {
      is_flag = 1;
    }
    if(master[1][111] != 'B') {
      is_flag = 1;
    }
    if(master[1][112] != 'B') {
      is_flag = 1;
    }
    if(master[1][113] != 'B') {
      is_flag = 1;
    }
    if(master[1][114] != 'B') {
      is_flag = 1;
    }
    if(master[1][115] != 'B') {
      is_flag = 1;
    }
    if(master[1][116] != 'B') {
      is_flag = 1;
    }
    if(master[1][127] != 'B') {
      is_flag = 1;
    }
    if(master[1][128] != 'B') {
      is_flag = 1;
    }
    if(master[1][129] != 'B') {
      is_flag = 1;
    }
    if(master[1][130] != 'B') {
      is_flag = 1;
    }
    if(master[1][131] != 'B') {
      is_flag = 1;
    }
    if(master[1][134] != 'B') {
      is_flag = 1;
    }
    if(master[1][141] != 'B') {
      is_flag = 1;
    }
    if(master[1][143] != 'B') {
      is_flag = 1;
    }
    if(master[1][144] != 'B') {
      is_flag = 1;
    }
    if(master[1][145] != 'B') {
      is_flag = 1;
    }
    if(master[1][146] != 'B') {
      is_flag = 1;
    }
    if(master[1][147] != 'B') {
      is_flag = 1;
    }
    if(master[1][148] != 'B') {
      is_flag = 1;
    }
    if(master[1][149] != 'B') {
      is_flag = 1;
    }
    if(master[1][151] != 'B') {
      is_flag = 1;
    }
    if(master[1][152] != 'B') {
      is_flag = 1;
    }
    if(master[1][153] != 'B') {
      is_flag = 1;
    }
    if(master[1][154] != 'B') {
      is_flag = 1;
    }
    if(master[1][155] != 'B') {
      is_flag = 1;
    }
    if(master[1][156] != 'B') {
      is_flag = 1;
    }
    if(master[1][159] != 'B') {
      is_flag = 1;
    }
  }

  // Check Row #3
  if(is_flag == 0) {
    if(master[2][1] != 'B') {
      is_flag = 1;
    }
    if(master[2][7] != 'B') {
      is_flag = 1;
    }
    if(master[2][9] != 'B') {
      is_flag = 1;
    }
    if(master[2][16] != 'B') {
      is_flag = 1;
    }
    if(master[2][18] != 'B') {
      is_flag = 1;
    }
    if(master[2][24] != 'B') {
      is_flag = 1;
    }
    if(master[2][29] != 'B') {
      is_flag = 1;
    }
    if(master[2][34] != 'B') {
      is_flag = 1;
    }
    if(master[2][44] != 'B') {
      is_flag = 1;
    }
    if(master[2][47] != 'B') {
      is_flag = 1;
    }
    if(master[2][53] != 'B') {
      is_flag = 1;
    }
    if(master[2][58] != 'B') {
      is_flag = 1;
    }
    if(master[2][63] != 'B') {
      is_flag = 1;
    }
    if(master[2][64] != 'B') {
      is_flag = 1;
    }
    if(master[2][69] != 'B') {
      is_flag = 1;
    }
    if(master[2][71] != 'B') {
      is_flag = 1;
    }
    if(master[2][75] != 'B') {
      is_flag = 1;
    }
    if(master[2][89] != 'B') {
      is_flag = 1;
    }
    if(master[2][94] != 'B') {
      is_flag = 1;
    }
    if(master[2][101] != 'B') {
      is_flag = 1;
    }
    if(master[2][105] != 'B') {
      is_flag = 1;
    }
    if(master[2][107] != 'B') {
      is_flag = 1;
    }
    if(master[2][113] != 'B') {
      is_flag = 1;
    }
    if(master[2][126] != 'B') {
      is_flag = 1;
    }
    if(master[2][132] != 'B') {
      is_flag = 1;
    }
    if(master[2][134] != 'B') {
      is_flag = 1;
    }
    if(master[2][141] != 'B') {
      is_flag = 1;
    }
    if(master[2][146] != 'B') {
      is_flag = 1;
    }
    if(master[2][151] != 'B') {
      is_flag = 1;
    }
    if(master[2][157] != 'B') {
      is_flag = 1;
    }
    if(master[2][160] != 'B') {
      is_flag = 1;
    }
  }

  // Check Row #4
  if(is_flag == 0) {
    if(master[3][1] != 'B') {
      is_flag = 1;
    }
    if(master[3][9] != 'B') {
      is_flag = 1;
    }
    if(master[3][16] != 'B') {
      is_flag = 1;
    }
    if(master[3][18] != 'B') {
      is_flag = 1;
    }
    if(master[3][29] != 'B') {
      is_flag = 1;
    }
    if(master[3][34] != 'B') {
      is_flag = 1;
    }
    if(master[3][35] != 'B') {
      is_flag = 1;
    }
    if(master[3][36] != 'B') {
      is_flag = 1;
    }
    if(master[3][37] != 'B') {
      is_flag = 1;
    }
    if(master[3][38] != 'B') {
      is_flag = 1;
    }
    if(master[3][43] != 'B') {
      is_flag = 1;
    }
    if(master[3][47] != 'B') {
      is_flag = 1;
    }
    if(master[3][58] != 'B') {
      is_flag = 1;
    }
    if(master[3][63] != 'B') {
      is_flag = 1;
    }
    if(master[3][65] != 'B') {
      is_flag = 1;
    }
    if(master[3][69] != 'B') {
      is_flag = 1;
    }
    if(master[3][71] != 'B') {
      is_flag = 1;
    }
    if(master[3][74] != 'B') {
      is_flag = 1;
    }
    if(master[3][89] != 'B') {
      is_flag = 1;
    }
    if(master[3][94] != 'B') {
      is_flag = 1;
    }
    if(master[3][101] != 'B') {
      is_flag = 1;
    }
    if(master[3][105] != 'B') {
      is_flag = 1;
    }
    if(master[3][107] != 'B') {
      is_flag = 1;
    }
    if(master[3][113] != 'B') {
      is_flag = 1;
    }
    if(master[3][126] != 'B') {
      is_flag = 1;
    }
    if(master[3][134] != 'B') {
      is_flag = 1;
    }
    if(master[3][141] != 'B') {
      is_flag = 1;
    }
    if(master[3][146] != 'B') {
      is_flag = 1;
    }
    if(master[3][151] != 'B') {
      is_flag = 1;
    }
    if(master[3][157] != 'B') {
      is_flag = 1;
    }
    if(master[3][161] != 'B') {
      is_flag = 1;
    }
  }

  // Check Row #5
  if(is_flag == 0) {
    if(master[4][2] != 'B') {
      is_flag = 1;
    }
    if(master[4][3] != 'B') {
      is_flag = 1;
    }
    if(master[4][4] != 'B') {
      is_flag = 1;
    }
    if(master[4][5] != 'B') {
      is_flag = 1;
    }
    if(master[4][6] != 'B') {
      is_flag = 1;
    }
    if(master[4][9] != 'B') {
      is_flag = 1;
    }
    if(master[4][10] != 'B') {
      is_flag = 1;
    }
    if(master[4][11] != 'B') {
      is_flag = 1;
    }
    if(master[4][12] != 'B') {
      is_flag = 1;
    }
    if(master[4][13] != 'B') {
      is_flag = 1;
    }
    if(master[4][14] != 'B') {
      is_flag = 1;
    }
    if(master[4][15] != 'B') {
      is_flag = 1;
    }
    if(master[4][16] != 'B') {
      is_flag = 1;
    }
    if(master[4][18] != 'B') {
      is_flag = 1;
    }
    if(master[4][29] != 'B') {
      is_flag = 1;
    }
    if(master[4][34] != 'B') {
      is_flag = 1;
    }
    if(master[4][42] != 'B') {
      is_flag = 1;
    }
    if(master[4][48] != 'B') {
      is_flag = 1;
    }
    if(master[4][49] != 'B') {
      is_flag = 1;
    }
    if(master[4][50] != 'B') {
      is_flag = 1;
    }
    if(master[4][51] != 'B') {
      is_flag = 1;
    }
    if(master[4][52] != 'B') {
      is_flag = 1;
    }
    if(master[4][58] != 'B') {
      is_flag = 1;
    }
    if(master[4][63] != 'B') {
      is_flag = 1;
    }
    if(master[4][66] != 'B') {
      is_flag = 1;
    }
    if(master[4][69] != 'B') {
      is_flag = 1;
    }
    if(master[4][71] != 'B') {
      is_flag = 1;
    }
    if(master[4][72] != 'B') {
      is_flag = 1;
    }
    if(master[4][89] != 'B') {
      is_flag = 1;
    }
    if(master[4][94] != 'B') {
      is_flag = 1;
    }
    if(master[4][95] != 'B') {
      is_flag = 1;
    }
    if(master[4][96] != 'B') {
      is_flag = 1;
    }
    if(master[4][97] != 'B') {
      is_flag = 1;
    }
    if(master[4][98] != 'B') {
      is_flag = 1;
    }
    if(master[4][99] != 'B') {
      is_flag = 1;
    }
    if(master[4][100] != 'B') {
      is_flag = 1;
    }
    if(master[4][101] != 'B') {
      is_flag = 1;
    }
    if(master[4][104] != 'B') {
      is_flag = 1;
    }
    if(master[4][105] != 'B') {
      is_flag = 1;
    }
    if(master[4][106] != 'B') {
      is_flag = 1;
    }
    if(master[4][107] != 'B') {
      is_flag = 1;
    }
    if(master[4][108] != 'B') {
      is_flag = 1;
    }
    if(master[4][113] != 'B') {
      is_flag = 1;
    }
    if(master[4][127] != 'B') {
      is_flag = 1;
    }
    if(master[4][128] != 'B') {
      is_flag = 1;
    }
    if(master[4][129] != 'B') {
      is_flag = 1;
    }
    if(master[4][130] != 'B') {
      is_flag = 1;
    }
    if(master[4][131] != 'B') {
      is_flag = 1;
    }
    if(master[4][134] != 'B') {
      is_flag = 1;
    }
    if(master[4][135] != 'B') {
      is_flag = 1;
    }
    if(master[4][136] != 'B') {
      is_flag = 1;
    }
    if(master[4][137] != 'B') {
      is_flag = 1;
    }
    if(master[4][138] != 'B') {
      is_flag = 1;
    }
    if(master[4][139] != 'B') {
      is_flag = 1;
    }
    if(master[4][140] != 'B') {
      is_flag = 1;
    }
    if(master[4][141] != 'B') {
      is_flag = 1;
    }
    if(master[4][146] != 'B') {
      is_flag = 1;
    }
    if(master[4][151] != 'B') {
      is_flag = 1;
    }
    if(master[4][152] != 'B') {
      is_flag = 1;
    }
    if(master[4][153] != 'B') {
      is_flag = 1;
    }
    if(master[4][154] != 'B') {
      is_flag = 1;
    }
    if(master[4][155] != 'B') {
      is_flag = 1;
    }
    if(master[4][156] != 'B') {
      is_flag = 1;
    }
    if(master[4][162] != 'B') {
      is_flag = 1;
    }
  }

  // Check Row #6
  if(is_flag == 0){
    if(master[5][7] != 'B') {
      is_flag = 1;
    }
    if(master[5][9] != 'B') {
      is_flag = 1;
    }
    if(master[5][16] != 'B') {
      is_flag = 1;
    }
    if(master[5][18] != 'B') {
      is_flag = 1;
    }
    if(master[5][29] != 'B') {
      is_flag = 1;
    }
    if(master[5][34] != 'B') {
      is_flag = 1;
    }
    if(master[5][43] != 'B') {
      is_flag = 1;
    }
    if(master[5][53] != 'B') {
      is_flag = 1;
    }
    if(master[5][58] != 'B') {
      is_flag = 1;
    }
    if(master[5][63] != 'B') {
      is_flag = 1;
    }
    if(master[5][67] != 'B') {
      is_flag = 1;
    }
    if(master[5][69] != 'B') {
      is_flag = 1;
    }
    if(master[5][71] != 'B') {
      is_flag = 1;
    }
    if(master[5][74] != 'B') {
      is_flag = 1;
    }
    if(master[5][89] != 'B') {
      is_flag = 1;
    }
    if(master[5][94] != 'B') {
      is_flag = 1;
    }
    if(master[5][101] != 'B') {
      is_flag = 1;
    }
    if(master[5][104] != 'B') {
      is_flag = 1;
    }
    if(master[5][108] != 'B') {
      is_flag = 1;
    }
    if(master[5][113] != 'B') {
      is_flag = 1;
    }
    if(master[5][132] != 'B') {
      is_flag = 1;
    }
    if(master[5][134] != 'B') {
      is_flag = 1;
    }
    if(master[5][141] != 'B') {
      is_flag = 1;
    }
    if(master[5][146] != 'B') {
      is_flag = 1;
    }
    if(master[5][151] != 'B') {
      is_flag = 1;
    }
    if(master[5][161] != 'B') {
      is_flag = 1;
    }
  }

  // Check Row #7
  if(is_flag == 0){
    if(master[6][1] != 'B') {
      is_flag = 1;
    }
    if(master[6][7] != 'B') {
      is_flag = 1;
    }
    if(master[6][9] != 'B') {
      is_flag = 1;
    }
    if(master[6][16] != 'B') {
      is_flag = 1;
    }
    if(master[6][18] != 'B') {
      is_flag = 1;
    }
    if(master[6][24] != 'B') {
      is_flag = 1;
    }
    if(master[6][29] != 'B') {
      is_flag = 1;
    }
    if(master[6][34] != 'B') {
      is_flag = 1;
    }
    if(master[6][44] != 'B') {
      is_flag = 1;
    }
    if(master[6][47] != 'B') {
      is_flag = 1;
    }
    if(master[6][53] != 'B') {
      is_flag = 1;
    }
    if(master[6][58] != 'B') {
      is_flag = 1;
    }
    if(master[6][63] != 'B') {
      is_flag = 1;
    }
    if(master[6][68] != 'B') {
      is_flag = 1;
    }
    if(master[6][69] != 'B') {
      is_flag = 1;
    }
    if(master[6][71] != 'B') {
      is_flag = 1;
    }
    if(master[6][75] != 'B') {
      is_flag = 1;
    }
    if(master[6][89] != 'B') {
      is_flag = 1;
    }
    if(master[6][94] != 'B') {
      is_flag = 1;
    }
    if(master[6][101] != 'B') {
      is_flag = 1;
    }
    if(master[6][104] != 'B') {
      is_flag = 1;
    }
    if(master[6][108] != 'B') {
      is_flag = 1;
    }
    if(master[6][113] != 'B') {
      is_flag = 1;
    }
    if(master[6][126] != 'B') {
      is_flag = 1;
    }
    if(master[6][132] != 'B') {
      is_flag = 1;
    }
    if(master[6][134] != 'B') {
      is_flag = 1;
    }
    if(master[6][141] != 'B') {
      is_flag = 1;
    }
    if(master[6][146] != 'B') {
      is_flag = 1;
    }
    if(master[6][151] != 'B') {
      is_flag = 1;
    }
    if(master[6][160] != 'B') {
      is_flag = 1;
    }
  }

  // Check Row #8
  if(is_flag == 0){
    if(master[7][2] != 'B') {
      is_flag = 1;
    }
    if(master[7][3] != 'B') {
      is_flag = 1;
    }
    if(master[7][4] != 'B') {
      is_flag = 1;
    }
    if(master[7][5] != 'B') {
      is_flag = 1;
    }
    if(master[7][6] != 'B') {
      is_flag = 1;
    }
    if(master[7][9] != 'B') {
      is_flag = 1;
    }
    if(master[7][16] != 'B') {
      is_flag = 1;
    }
    if(master[7][19] != 'B') {
      is_flag = 1;
    }
    if(master[7][20] != 'B') {
      is_flag = 1;
    }
    if(master[7][21] != 'B') {
      is_flag = 1;
    }
    if(master[7][22] != 'B') {
      is_flag = 1;
    }
    if(master[7][23] != 'B') {
      is_flag = 1;
    }
    if(master[7][29] != 'B') {
      is_flag = 1;
    }
    if(master[7][34] != 'B') {
      is_flag = 1;
    }
    if(master[7][45] != 'B') {
      is_flag = 1;
    }
    if(master[7][48] != 'B') {
      is_flag = 1;
    }
    if(master[7][49] != 'B') {
      is_flag = 1;
    }
    if(master[7][50] != 'B') {
      is_flag = 1;
    }
    if(master[7][51] != 'B') {
      is_flag = 1;
    }
    if(master[7][52] != 'B') {
      is_flag = 1;
    }
    if(master[7][55] != 'B') {
      is_flag = 1;
    }
    if(master[7][56] != 'B') {
      is_flag = 1;
    }
    if(master[7][57] != 'B') {
      is_flag = 1;
    }
    if(master[7][58] != 'B') {
      is_flag = 1;
    }
    if(master[7][59] != 'B') {
      is_flag = 1;
    }
    if(master[7][60] != 'B') {
      is_flag = 1;
    }
    if(master[7][61] != 'B') {
      is_flag = 1;
    }
    if(master[7][63] != 'B') {
      is_flag = 1;
    }
    if(master[7][69] != 'B') {
      is_flag = 1;
    }
    if(master[7][71] != 'B') {
      is_flag = 1;
    }
    if(master[7][76] != 'B') {
      is_flag = 1;
    }
    if(master[7][78] != 'B') {
      is_flag = 1;
    }
    if(master[7][79] != 'B') {
      is_flag = 1;
    }
    if(master[7][80] != 'B') {
      is_flag = 1;
    }
    if(master[7][81] != 'B') {
      is_flag = 1;
    }
    if(master[7][82] != 'B') {
      is_flag = 1;
    }
    if(master[7][83] != 'B') {
      is_flag = 1;
    }
    if(master[7][84] != 'B') {
      is_flag = 1;
    }
    if(master[7][89] != 'B') {
      is_flag = 1;
    }
    if(master[7][94] != 'B') {
      is_flag = 1;
    }
    if(master[7][101] != 'B') {
      is_flag = 1;
    }
    if(master[7][104] != 'B') {
      is_flag = 1;
    }
    if(master[7][108] != 'B') {
      is_flag = 1;
    }
    if(master[7][113] != 'B') {
      is_flag = 1;
    }
    if(master[7][118] != 'B') {
      is_flag = 1;
    }
    if(master[7][119] != 'B') {
      is_flag = 1;
    }
    if(master[7][120] != 'B') {
      is_flag = 1;
    }
    if(master[7][121] != 'B') {
      is_flag = 1;
    }
    if(master[7][122] != 'B') {
      is_flag = 1;
    }
    if(master[7][123] != 'B') {
      is_flag = 1;
    }
    if(master[7][124] != 'B') {
      is_flag = 1;
    }
    if(master[7][127] != 'B') {
      is_flag = 1;
    }
    if(master[7][128] != 'B') {
      is_flag = 1;
    }
    if(master[7][129] != 'B') {
      is_flag = 1;
    }
    if(master[7][130] != 'B') {
      is_flag = 1;
    }
    if(master[7][131] != 'B') {
      is_flag = 1;
    }
    if(master[7][134] != 'B') {
      is_flag = 1;
    }
    if(master[7][141] != 'B') {
      is_flag = 1;
    }
    if(master[7][143] != 'B') {
      is_flag = 1;
    }
    if(master[7][144] != 'B') {
      is_flag = 1;
    }
    if(master[7][145] != 'B') {
      is_flag = 1;
    }
    if(master[7][146] != 'B') {
      is_flag = 1;
    }
    if(master[7][147] != 'B') {
      is_flag = 1;
    }
    if(master[7][148] != 'B') {
      is_flag = 1;
    }
    if(master[7][149] != 'B') {
      is_flag = 1;
    }
    if(master[7][151] != 'B') {
      is_flag = 1;
    }
    if(master[7][159] != 'B') {
      is_flag = 1;
    }
  }

  // Check if it's the flag
  return is_flag;
}