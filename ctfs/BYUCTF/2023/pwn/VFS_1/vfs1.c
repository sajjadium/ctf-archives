#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

__attribute__((constructor)) void flush_buf() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void banner() {
    puts("VVVVVVVV           VVVVVVVVFFFFFFFFFFFFFFFFFFFFFF   SSSSSSSSSSSSSSS ");
    puts("V::::::V           V::::::VF::::::::::::::::::::F SS:::::::::::::::S");
    puts("V::::::V           V::::::VF::::::::::::::::::::FS:::::SSSSSS::::::S");
    puts("V::::::V           V::::::VFF::::::FFFFFFFFF::::FS:::::S     SSSSSSS");
    puts(" V:::::V           V:::::V   F:::::F       FFFFFFS:::::S            ");
    puts("  V:::::V         V:::::V    F:::::F             S:::::S            ");
    puts("   V:::::V       V:::::V     F::::::FFFFFFFFFF    S::::SSSS         ");
    puts("    V:::::V     V:::::V      F:::::::::::::::F     SS::::::SSSSS    ");
    puts("     V:::::V   V:::::V       F:::::::::::::::F       SSS::::::::SS  ");
    puts("      V:::::V V:::::V        F::::::FFFFFFFFFF          SSSSSS::::S ");
    puts("       V:::::V:::::V         F:::::F                         S:::::S");
    puts("        V:::::::::V          F:::::F                         S:::::S");
    puts("         V:::::::V         FF:::::::FF           SSSSSSS     S:::::S");
    puts("          V:::::V          F::::::::FF           S::::::SSSSSS:::::S");
    puts("           V:::V           F::::::::FF           S:::::::::::::::SS ");
    puts("            VVV            FFFFFFFFFFF            SSSSSSSSSSSSSSS   ");
    puts("");
    puts("");
    puts("[+] Welcome to the Virtual File System! Here you can create, delete, and");
    puts("modify files. In order to save space, multiple people are using this same");
    puts("system. But don't worry! We've implemented a system to prevent people from");
    puts("seeing each other's files. Enjoy!\n\n");
}

int menu() {
    int choice;

    puts("[+] What would you like to do?");
    puts("1. Create a file");
    puts("2. Delete a file");
    puts("3. Modify a file");
    puts("4. Read a file");
    puts("5. Exit");

    printf("> ");
    scanf("%d", &choice);

    return choice;
}

int main() {
    banner();

    // INITIALIZATIONS
    struct filesystem {
        char contents[2880];
        char flag[64];
        int current_file;
    };

    // get flag
    struct filesystem fs;
    char * buffer = 0;
    long length;
    FILE * f = fopen ("flag.txt", "rb");

    if (f) {
        fseek (f, 0, SEEK_END);
        length = ftell (f);
        fseek (f, 0, SEEK_SET);
        buffer = malloc (length);
        if (buffer) {
            fread (buffer, 1, length, f);
        }
        fclose (f);
    }

    if (buffer) {
        strcpy(fs.flag, buffer);
        free(buffer);
    }
    else {
        puts("[-] Error reading flag");
        exit(1);
    }
    
    fs.current_file = 0;
    char filename[32];
    char contents[256];

    while (1==1) {
        int choice = menu();

        if (choice == 1) {

            if (fs.current_file == 10) {
                puts("[-] Sorry, you can't create any more files!");
                continue;
            }
            // create
            

            puts("[+] What would you like to name your file?");
            printf("> ");
            scanf("%32s", filename);

            puts("[+] What would you like to put in your file?");
            printf("> ");
            scanf("%256s", contents);

            // copy filename
            memcpy(fs.contents + (fs.current_file*288), filename, 32);

            // copy contents
            memcpy(fs.contents + (fs.current_file*288) + 32, contents, 256);

            printf("[+] File created! (#%d)\n\n", fs.current_file);
            fs.current_file++;
        }
        else if (choice == 2) {
            // delete
            //delete_file();
            printf("Sorry, that hasn't been implemented yet!\n");
        }
        else if (choice == 3) {
            // modify
            //modify_file();
            printf("Sorry, that hasn't been implemented yet!\n");
        }
        else if (choice == 4) {
            // read
            int file_to_read;

            puts("[+] Which file # would you like to read?");
            printf("> ");
            scanf("%d", &file_to_read);

            if ((file_to_read >= fs.current_file) || (file_to_read < 0)) {
                puts("[-] Invalid file number");
                continue;
            }

            printf("[+] Filename: %s", fs.contents + (file_to_read*288));
            printf("[+] Contents: %s", fs.contents + (file_to_read*288) + 32);
        }
        else if (choice == 5) {
            exit(0);
        }
        else {
            puts("[-] Invalid choice");
            exit(1);
        }
    }
}