#include <unistd.h>


#define CMD_NUM 7
#define DEV_CMD_NUM 5

#define LOG_PRINT(format, ...) \
        if ((g_logging) != 0) { \
            printf(format, ##__VA_ARGS__); \
        }

void help();
void set_name();
void status();
void send_vhf();
void send_safety();
void VHFADMIN();
void exit();
void toggle_logging();
void send_safety_msg();
void send_bin_msg();
void send_position();
void dev_help();

typedef struct commands {
    char command[0x10];
    void (*func)(void);
} commands_t;