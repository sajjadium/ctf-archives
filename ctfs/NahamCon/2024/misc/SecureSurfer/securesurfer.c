#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void surf(const char *url) {
    char command[512];
    sprintf(command, "/usr/local/bin/lynx --accept_all_cookies -cache=0 -restrictions=all '%s'", url);
    system(command);
    system("stty sane");
}

int main() {
    puts("  _____                           _____             __          ");
    puts(" / ____|                         / ____|           / _|         ");
    puts("| (___   ___  ___ _   _ _ __ ___| (___  _   _ _ __| |_ ___ _ __ ");
    puts(" \\___ \\ / _ \\/ __| | | | '__/ _ \\\\___ \\| | | | '__|  _/ _ \\ '__|");
    puts(" ____) |  __/ (__| |_| | | |  __/____) | |_| | |  | ||  __/ |   ");
    puts("|_____/ \\___|\\___|\\__,_|_|  \\___|_____/ \\__,_|_|  |_| \\___|_|   ");
    puts("");

    int choice;

    while (1) {
        printf("\n===== Menu =====\n");
        printf("  1. Surf SSH\n");
        printf("  2. Surf RSA\n");
        printf("  3. Surf DSA\n");
        printf("  4. Surf ECDSA\n");
        printf("  5. Surf ECDH\n");
        printf("  6. Surf WWW\n");
        printf("  7. Exit\n");
        puts("");
        printf("Enter your choice: ");
        fflush(stdout); 
        scanf("%d", &choice);
        getchar(); 

        switch (choice) {
            case 1:
                surf("https://en.wikipedia.org/wiki/Secure_Shell");
                break;
            case 2:
                surf("https://en.wikipedia.org/wiki/RSA_(cryptosystem)");
                break;
            case 3:
                surf("https://en.wikipedia.org/wiki/Digital_Signature_Algorithm");
                break;
            case 4:
                surf("https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm");
                break;
            case 5:
                surf("https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman");
                break;
            case 6:
                {
                    char url[1024];
                    printf("Online URL: ");
                    fflush(stdout); 
                    fgets(url, sizeof(url), stdin);
                    url[strcspn(url, "\n")] = 0; // Remove newline character

                    if (strstr(url, "https://") == NULL) {
                        printf("\nWe are secure here at the SecureSurfer! You must use https:// !\n");
                    } else {
                        surf(url);
                    }
                }
                break;
            case 7:
                printf("Exiting SecureSurfer...\n");
                return 0;
                break;
            default:
                printf("Invalid choice. Please try again.\n");
                break;
        }
    }

    return 0;
}
