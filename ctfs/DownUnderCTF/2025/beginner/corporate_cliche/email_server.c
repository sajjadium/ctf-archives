#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void open_admin_session() {
    printf("-> Admin login successful. Opening shell...\n");
    system("/bin/sh");
    exit(0);
}

void print_email() {
    printf(" ______________________________________________________________________\n");
    printf("| To:      all-staff@downunderctf.com                                  |\n");
    printf("| From:    synergy-master@downunderctf.com                             |\n");
    printf("| Subject: Action Item: Leveraging Synergies                           |\n");
    printf("|______________________________________________________________________|\n");
    printf("|                                                                      |\n");
    printf("| Per my last communication, I'm just circling back to action the      |\n");
    printf("| sending of this email to leverage our synergies. Let's touch base    |\n");
    printf("| offline to drill down on the key takeaways and ensure we are all     |\n");
    printf("| aligned on this new paradigm. Moving forward, we need to think       |\n");
    printf("| outside the box to optimize our workflow and get the ball rolling.   |\n");
    printf("|                                                                      |\n");
    printf("| Best,                                                                |\n");
    printf("| A. Manager                                                           |\n");
    printf("|______________________________________________________________________|\n");
    exit(0);
}

const char* logins[][2] = {
    {"admin", "🇦🇩🇲🇮🇳"},
    {"guest", "guest"},
};

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    char password[32];
    char username[32];

    printf("┌──────────────────────────────────────┐\n");
    printf("│      Secure Email System v1.337      │\n");
    printf("└──────────────────────────────────────┘\n\n");

    printf("Enter your username: ");
    fgets(username, sizeof(username), stdin);
    username[strcspn(username, "\n")] = 0;

    if (strcmp(username, "admin") == 0) {
        printf("-> Admin login is disabled. Access denied.\n");
        exit(0);
    }

    printf("Enter your password: ");
    gets(password);

    for (int i = 0; i < sizeof(logins) / sizeof(logins[0]); i++) {
        if (strcmp(username, logins[i][0]) == 0) {
            if (strcmp(password, logins[i][1]) == 0) {
                printf("-> Password correct. Access granted.\n");
                if (strcmp(username, "admin") == 0) {
                    open_admin_session();
                } else {
                    print_email();
                }
            } else {
                printf("-> Incorrect password for user '%s'. Access denied.\n", username);
                exit(1);
            }
        }
    }
    printf("-> Login failed. User '%s' not recognized.\n", username);
    exit(1);
}
