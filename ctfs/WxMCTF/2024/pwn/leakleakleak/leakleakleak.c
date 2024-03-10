// compile with: gcc leakleakleak.c -o leakleakleak -fpie -pie

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>

char flag[128] = {0};

typedef struct {
    char username[32];
    char *description;
} User;

void warmup_heap(void) {
    void *addrs[3];
    for (size_t i = 0; i < 3; ++i) {
        addrs[i] = malloc(9000);
    }

    free(addrs[1]);
}

User *create_user(void) {
    User *user = calloc(1, sizeof (User));
    user->description = calloc(1, 256);
    return user;
}

void destroy_user(User *user) {
    free(user->description);
    free(user);
}

void init(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void read_flag(void) {
    int flag_fd = open("./flag.txt", O_RDONLY);
    off_t flag_size = lseek(flag_fd, 0, SEEK_END);
    lseek(flag_fd, 0, SEEK_SET);
    read(flag_fd, flag, flag_size);
    flag[flag_size] = '\00';
    close(flag_fd);
}

int main() {
    init();
    read_flag();
    warmup_heap();

    User *user = create_user();

    for (_Bool quit = 0; !quit; ) {
        printf("What is your name? ");
        read(STDIN_FILENO, user, sizeof(*user));
        printf("Hello %s!\n", user->username);
            
        puts("Let me tell you something about yourself! :3");
        printf("%s\n", user->description);
        
        printf("Continue? (Y/n) ");
        char c = getchar();
        if (c == 'n' || c == 'N')
            quit = 1;
    }

    puts("Boom! Boom, boom, boom! I want YOU in my room!");
    
    destroy_user(user);
    return 0;
}
