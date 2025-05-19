#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>

__attribute__((constructor)) void flush_buf() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

typedef struct {
    long uid;
    char username[8];
    long keycard;
} user_t;

typedef struct {
    long mfg_date;
    char first[8];
    char last[8];
} nametag_t;

long UID = 0x1;
char filename[] = "flag.txt";
user_t* curr_user = NULL;
nametag_t* curr_nametag = NULL;

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

void register_user() {
    printf("WELCOME!! We're so excited to have you here! Tell us your username / tag and we'll get you set up with access to the facilities!\n");
    curr_user = (user_t*)malloc(sizeof(user_t));
    curr_user->uid = UID++;
    printf("Please go ahead an type your username now: \n");
    read(0, curr_user->username, 8);
}

void log_out() {
    free(curr_user);
    curr_user = NULL;
    if (curr_nametag != NULL) {
        free(curr_nametag);
        curr_nametag = NULL;
    }
}

int print_menu() {
    int choice;
    printf("What would you like to do now?\n");
    printf("1. Register a new user\n");
    printf("2. Learn about the Time Keepers\n");
    printf("3. Collect gear\n");
    printf("4. Elevate to super user\n");
    printf("5. Change characters\n");
    printf("6. Leave\n");
    // 7 is try to free loki but it's not technically an option, you have to be rebellious to get there
    scanf("%d", &choice);
    if (choice < 1 || choice > 7) {
        printf("Invalid choice. You broke the simulation\n");
        return 0;
    }
    return choice;
}

int main(void) {
    init();
    srand(time(NULL)); int gear;
    printf("Hello! My name is Miss Minutes, and I'll be your helper here at the TVA!!\nHow about we get you oriented first!\nThe only rule is that we under no circumstances can free Loki... he's locked up for a reason!\n");

    int input = 1;
    while (input) {
        switch (input) {
            case 1: // register a new user
                register_user();
                break;
            case 2:
                printf("The Time Keepers are the three beings who created the TVA and the Sacred Timeline. They are powerful beings who exist at the end of time and are responsible for maintaining the flow of time.\n");
                break;
            case 3: // collect gear
                if (curr_user == NULL) {
                    printf("You must register a user first!\n");
                    break;
                }
                gear = rand() % 5 + 1;
                if (curr_nametag != NULL) {
                    free(curr_nametag);
                }
                switch (gear) {
                    case 1:
                        printf("You have received a Time Twister! This powerful device allows you to manipulate time and space.\n");
                        break;
                    case 2:
                        printf("You have received a Name Tag! Please input your first and last name:\n");
                        curr_nametag = (nametag_t*)malloc(sizeof(nametag_t));
                        curr_nametag->mfg_date = (long)time(NULL);
                        read(0, curr_nametag->first, 8);
                        read(0, curr_nametag->last, 8);
                        break;
                    case 3:
                        printf("You have received a Time Stick! This device allows you to reset the flow of time in a specific area.\n");
                        break;
                    case 4:
                        printf("You have received a Time Loop! This device allows you to trap someone in a time loop.\n");
                        break;
                    case 5:
                        printf("You have received a Time Bomb! This device allows you to create a temporal explosion.\n");
                        break;
                }
                break;
            case 4:
                if (curr_user == NULL) {
                    printf("You must register a user first!\n");
                    break;
                }
                if (curr_user->uid >= 0x600000) {
                    printf("Well, everything here checks out! Go ahead and take this key card!\n");
                    curr_user->keycard = 0x1337;
                } else {
                    printf("Unfortunately, it doesn't look like you have all the qualifications to get your own key card! Stay close to Miss Minutes and she should be able to get you anywhere you need to go...\n");
                }
                break;
            case 5:
                if (curr_user == NULL) {
                    printf("You must register a user first!\n");
                    break;
                }
                log_out();
                printf("You have been logged out.\n");
                printf(". "); sleep(1);
                printf(". "); sleep(1);
                printf(". \n"); sleep(1);
                register_user();
                break;
            case 6:
                input = 0;
                break;
            case 7:
                if (curr_user == NULL) {
                    printf("You must register a user first!\n");
                    break;
                }
                if (curr_user->keycard == 0x1337) {
                    printf("You have freed Loki! In gratitude, he offers you a flag!\n");
                    FILE* flag = fopen(filename, "r");
                    if (flag == NULL) {
                        printf("Flag file not found. Please contact an admin.\n");
                        return EXIT_FAILURE;
                    } else {
                        char ch;
                        while ((ch = fgetc(flag)) != EOF) {
                            printf("%c", ch);
                        }
                    }
                    fclose(flag);
                    exit(0);
                    break;
                } else {
                    printf("EMERGENCY EMERGENCY UNAUTHORIZED USER HAS TRIED TO FREE LOKI!\n");
                    printf("Time police rush to the room where you stand in shock. They rush you away, take your gear, and kick you back to your own timeline.\n");
                    log_out();
                    input = 0;
                    break;
                }
        }

        if (input != 0) {
            input = print_menu();
        }
    }
    return input;
}