#include <stddef.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/resource.h>
#include <pwd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define PATH_EXECUTABLE "./child"
#define BASE_PATH "/home/game/"

int main(int argc, char *argv[]) {

    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);

    puts("[+] Setting up for game execution.");
    char valid_save = 0;

    // Check if the provided file is a valid gamesave 
    if(argc >= 2) {
        puts("[+] Validating game save");
        char game_save_path[256] = {0};
        strcpy(game_save_path, BASE_PATH);
        strncat(game_save_path, argv[1], (size_t) (255 - strlen(BASE_PATH)));

        // Open game save
        int fd = open(game_save_path, O_RDONLY);
        char buffer[5];
        read(fd, buffer, 4);
        buffer[4] = 0;
        // Check if the file starts with GAMESAVE
        if(strcmp(buffer, "GAME")) {
            valid_save = 1;
        }
        else {
            puts("[-] The provided file does not seem to be a valid game save");
        }
    }

    // Drop privileges to game account
    
    // Retrieve the ids for the game account
    puts("[+] Getting the uid and gid for user game");
    struct passwd* pwd = getpwnam("game");
    if (pwd == NULL) {
        puts("[-] Cannot find UID for name game"); 
        return 1;
    }

    // Change our privileges to the game user

    if (geteuid() == 0) {
        puts("[+] Setting gid");
        if (setgid(pwd->pw_gid) != 0){
            puts("[-] setgid: Unable to drop group privileges");
            return 1;
        }
        puts("[+] Setting uid");
        if (setuid(pwd->pw_uid) != 0) {
            puts("[-] setuid: Unable to drop user privileges");
            return 1;
        }
    }
    else {
        puts("[-] Execution was not privileged.");
        return 1;
    }


    // Call the child executable
    puts("[+] Executing the game binary");
    fflush(stdout);
    if(valid_save) {
        execl(PATH_EXECUTABLE, argv[1], NULL);
    }
    else {
        execl(PATH_EXECUTABLE, "", NULL);
    }
}