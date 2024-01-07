#include <cstring>
#include <iostream>
#include <thread>
#include <cstdio>

struct Account {
    char id;
    bool active;
    char* name;
    uint64_t balance;
};

void submit_support_ticket(char* _name, char* _content) {
    // stub
}

char* separator;
char* debug_log;
Account* accounts;
char id_counter = 0;
size_t account_count = 0;

void interface() {
    while(true) {
        printf("Welcome to the ShakyVault Bank Interface\n");
        printf(separator);
        printf("1) Create new Account\n");
        printf("2) Show an Account\n");
        printf("3) Create a Transaction\n");
        printf("4) Deactivate an Account\n");
        printf("5) Create a support ticket\n");
        printf("6) Exit\n");
        printf("> ");

        const int selection = fgetc(stdin) - static_cast<int>('0');
        fgetc(stdin);

        switch (selection) {
            case 1: {
                if (account_count >= 255) {
                    printf("We've unfortunately run out of accounts. Please try again later.");
                    break;
                }

                printf("Account Name: ");

                char* account_name = new char[80];
                std::cin.getline(account_name, 80);
                for (size_t i = 0; i < 80; i++) {
                    if (account_name[i] == '\n') {
                        account_name[i] = '\0';
                        break;
                    }
                }
                account_name[79] = '\0';

                accounts[account_count].id = id_counter++;
                accounts[account_count].active = true;
                accounts[account_count].name = account_name;
                accounts[account_count].balance = 35;

                printf("Account created. Your id is %d\n", accounts[account_count++].id);
                printf("We have granted you a $35 starting bonus.\n");

                break;
            }
            case 2: {
                printf("Which id do you want to read? ");
                size_t number;
                std::cin >> number;
                if (std::cin.fail()) {
                    printf("Invalid Input.");
                    exit(EXIT_FAILURE);
                }
                fgetc(stdin);

                if (number >= account_count) {
                    printf("That account does not exist.");
                    break;
                }

                const Account acc = accounts[number];

                printf("Id: %d\n", acc.id);
                printf("Name: %s\n", acc.name);
                printf("Active: %s\n", acc.active ? "true" : "false");
                printf("Balance: %lu\n", acc.balance);

                break;
            }
            case 3: {
                printf("Which account do you want to transfer from? ");
                size_t id_from;
                std::cin >> id_from;
                if (std::cin.fail()) {
                    printf("Invalid Input.");
                    exit(EXIT_FAILURE);
                }
                fgetc(stdin);

                printf("Which account do you want to transfer to? ");
                size_t id_to;
                std::cin >> id_to;
                if (std::cin.fail()) {
                    printf("Invalid Input.");
                    exit(EXIT_FAILURE);
                }
                fgetc(stdin);

                if (id_from >= account_count || id_to >= account_count) {
                    printf("Invalid account id\n");
                    break;
                }

                printf("How much money do you want to transfer? ");
                uint64_t amount;
                std::cin >> amount;
                if (std::cin.fail()) {
                    printf("Invalid Input.");
                    exit(EXIT_FAILURE);
                }
                fgetc(stdin);

                const Account from = accounts[id_from];
                const Account to = accounts[id_to];

                if (from.balance < amount) {
                    printf("You don't have enough money for that.");
                    break;
                }

                if (!from.active || !to.active) {
                    printf("That account is not active.");
                    break;
                }

                accounts[from.id].balance -= amount;
                accounts[to.id].balance += amount;

                printf("Transaction created!\n");

                break;
            }
            case 4: {
                printf("Which account do you want to disable? ");
                size_t number;
                std::cin >> number;
                if (std::cin.fail()) {
                    printf("Invalid Input.");
                    exit(EXIT_FAILURE);
                }
                fgetc(stdin);

                if (number >= account_count) {
                    printf("That account does not exist.");
                    break;
                }

                accounts[number].active = false;
            }
            case 5: {
                printf("Which account does this issue concern? ");
                size_t number;
                std::cin >> number;
                if (std::cin.fail()) {
                    printf("Invalid Input.");
                    exit(EXIT_FAILURE);
                }
                fgetc(stdin);

                Account acc = accounts[number];

                char name[40] = "Support ticket from ";
                char* content = new char[1000];

                printf("Please describe your issue (1000 charaters): ");
                std::cin.getline(content, 1000);
                if (std::cin.fail()) {
                    printf("Invalid Input.");
                    exit(EXIT_FAILURE);
                }

                char* name_ptr = name + strlen(name);
                strcpy(name_ptr, acc.name);
                name_ptr += strlen(acc.name);
                *name_ptr = '\0';

                submit_support_ticket(name, content);
                printf("Thanks! Our support technicians will help you shortly.\n");

                delete[] content;

                break;
            }
            case 6: {
                return;
            }
            default: {
                printf("Invalid option %d\n\n\n", selection);
                break;
            }
        }
    }
}

int main() {
    setbuf(stdout, nullptr);

    separator = new char[128];
    debug_log = new char[2900];
    accounts = new Account[256];

    strcpy(debug_log, "TODO");

    for (int i = 0; i < 126; i++) separator[i] = '_';
    separator[126] = '\n';
    separator[127] = '\0';

    interface();

    delete[] separator;
    delete[] debug_log;
    delete[] accounts;

    return 0;
}
