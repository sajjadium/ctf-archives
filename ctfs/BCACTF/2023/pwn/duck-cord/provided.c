/*
    Attention, this is not the challenge source code
    This is only a reproduction of some of it
    For analysis purposes only
*/

#define MAX_MSG_COUNT (14)
#define SYSTEM_TAG (0x30303030 /* #0000 */)
#define MAX_NAME_LEN (32)

uint16_t current_time;

int print_time(uint16_t time) {
    return printf("%2d:%02d", time / 60, time % 60);
}

void time_goes_by() {
    current_time += 1 + (rand() % 3);
}

typedef struct {
    char name[MAX_NAME_LEN];
    union {
        uint32_t tag_raw;
        char tag[4];
    };
} user_t;

typedef struct {
    user_t* author;
    char content[100];
    uint16_t time_sent; // in minutes
} msg_t;

user_t system_user = {
    .name = "Agent Duck",
    .tag_raw = SYSTEM_TAG // #0000
};

void make_system_only_msg(msg_t* out, char* content) {
    out->author = &system_user;
    strcpy(out->content, content);
    out->time_sent = current_time;

    time_goes_by();
}

#define RANDOM_USER_CNT (5)
user_t random_users[RANDOM_USER_CNT] = {
    { .name = "Classic Ducky", .tag_raw = 0x30323139 },
    { .name = "Profesor Ducky", .tag_raw = 0x34383735 },
    { .name = "Scuba Ducky", .tag_raw = 0x31333832 },
    { .name = "Sailor Ducky", .tag_raw = 0x39393233 },
    { .name = "Techno Ducky", .tag_raw = 0x34373135 }
};

#define RANDOM_MSG_CNT (7)
char* random_msgs[RANDOM_MSG_CNT] = {
    "What a beautiful day today!",
    "It really is remarkable, isn't it?",
    "How do I invite my friends to this?",
    "Duck cord is so awesome!",
    "I wish there wasn't a user name limit",
    "Anyone know how to access the system mesages?",
    "This is a great alternative to email"
};

void make_random_msg(msg_t* out) {
    out->author = &random_users[rand() % RANDOM_USER_CNT];
    strcpy(out->content, random_msgs[rand() % RANDOM_MSG_CNT]);
    out->time_sent = current_time;
    time_goes_by();
}

int main() {
    srand(time(NULL));
    current_time = (1 + (rand() % 8)) * 60 + ((rand() % 60));

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    char flag[100];
    load_flag(flag, 100);

    int msg_count = 0;
    msg_t msgs[MAX_MSG_COUNT];
    
    make_system_only_msg(&msgs[msg_count++], flag);
    while (msg_count < 7) {
        make_random_msg(&msgs[msg_count]);
        msg_count += 1;
    }

    puts("## Hello! Welcome to Duck Cord");
    puts("## Duck Cord is a version of discord made just for ducks");

    user_t self;
    self.tag[0] = '0' + (rand() % 10);
    self.tag[1] = '0' + (rand() % 10);
    self.tag[2] = '0' + (rand() % 10);
    // made this always be > 1, to prevent from acessing the SYSTEM_USER text with #0000
    self.tag[3] = '1' + (rand() % 9);

    printf("What do you want your name to be? (maximum of %d chars)\n", MAX_NAME_LEN);
    printf("> ");

    gets(self.name);

    printf("Welcome ");
    print_user(&self);
    printf("!\n");

    printf("Loading messages...\n");

    msg_t* msg;
    for (int i = 0; i < msg_count; ++i) {
        msg = &msgs[i];
        // if the tag is #0000, don't read it unless our tag is also #0000
        if (msg->author->tag_raw == SYSTEM_TAG) {
            if (self.tag_raw == SYSTEM_TAG) print_msg(msg);
        } else {
            // by default we have access
            print_msg(msg);
        }
        sleep(1);
    }

    while (msg_count < MAX_MSG_COUNT) {
        msg = &msgs[msg_count++];
        msg->author = &self;
        msg->time_sent = current_time;
        printf("(send a message)> ");
        fgets(msg->content, sizeof(msg->content), stdin);
        print_msg(msg);
        time_goes_by();
        sleep(1);
        if (msg_count >= MAX_MSG_COUNT) break;

        msg = &msgs[msg_count++];
        make_random_msg(msg);
        print_msg(msg);
        time_goes_by();
        sleep(1);
        if (msg_count >= MAX_MSG_COUNT) break;
    }

    puts("----");
    puts("You've sent enough messages for today.");
    puts("Hope you enjoyed your stay. Goodbye.");

    return 0;
}