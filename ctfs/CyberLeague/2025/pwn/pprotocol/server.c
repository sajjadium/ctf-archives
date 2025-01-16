// gcc -Wall -pedantic -O3 -Wno-stringop-truncation -g server.c -o chall && ./chall
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define PACKET_CAP 0x120
#define TOTAL_CAP 0x600
#define RULE_INIT_SZ 0x200
typedef struct Packet
{
    unsigned short signature;
    char header[8];
    char message[PACKET_CAP];
    unsigned short size;
    int checksum;
} Packet;
const unsigned short packet_signature = 0xdead;
const Packet ok_response = { .signature = packet_signature, .header = "RESPOND", .message = "OK", .size = 2, .checksum = 1079021242 };

typedef struct Rules {
    char* buffer;
    size_t length;
    size_t capacity;
} Rules;

void fatal(const char* s)
{
    puts(s);
    exit(EXIT_FAILURE);
}

int calculate_checksum(const char* block, size_t n) {
    int checksum = 0;
    size_t i;
    for (i = 0; i + 4 <= n; i += 4) {
        checksum ^= *(int*)(block + i);
    }
    // remaining block
    for (; i < n; i++) {
        checksum ^= (int)block[i];
    }

    return checksum;
}
#define cc(packet) calculate_checksum((char*)&packet, sizeof(packet) - sizeof(packet.checksum))

// Use STDIO instead of socket for ease of setup
ssize_t recv_(int fd, void* p, size_t n, int flags) {
    (void)fd;
    (void)flags;
    if (n == 0) {
        return 0;
    }
    ssize_t count = read(STDIN_FILENO, p, n);
    if (count == -1) {
        // error
        return count;
    }
    if (count != n) {
        return -1;
    }
    getchar(); // consume newline
    return count;
}

ssize_t send_(int fd, const void* p, size_t n, int flags) {
    (void)fd;
    (void)flags;
    ssize_t count = write(STDOUT_FILENO, p, n);
    if (count == -1) {
        // error
        return count;
    }
    putchar('\n'); // for nicer output
    return count;
}

int close_(int fd) {
    (void)fd;
    puts("closed connection");
    return 0;
}

void start_server() {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
}
void stop_server() {}
int await_connection() {
    return -1;
}

void strrpl(char* str, const char* old_str, const char* new_str)
{
    const size_t old_len = strlen(old_str), new_len = strlen(new_str);
    if (old_len < new_len || old_len < 1)
    {
        puts("strrpl: invalid params");
        return;
    }

    for (int i = 0; str[i + old_len - 1] != '\0'; i++)
    {
        if (strncmp(&str[i], old_str, old_len) == 0)
        {
            memcpy(&str[i], new_str, new_len); // avoid copying null byte
            size_t remaining_length = strlen(&str[i] + old_len);
            memmove(&str[i] + new_len, &str[i] + old_len, remaining_length);            // shifts the remaining string forward
            memset(&str[i] + new_len + remaining_length, 0, old_len - new_len); // zeroes out excess
            i = -1;                                                                                     // restarts search to find any new_str targets
        }
    }
}

// Return -1 on in valid input, 0 on success.
int add_rule(char* input, Rules* rules)
{
    size_t original_len = strlen(input);
    char* old_end = strchr(input, ':');
    if (old_end == NULL) {
        // invalid rule, does not contain ':'
        return -1;
    }
    *old_end = 0;
    size_t old_len = old_end - input, new_len = original_len - old_len - 1;
    if (old_len == 0) {
        // invalid rule
        return -1;
    }

    char* old_str = input;
    char* new_str = old_end + 1;

    if (strcmp(old_str, new_str) == 0) {
        // may cause infinite replacements
        return -1;
    }

    // append <old_str>:<new_str>: to rules->buffer
    size_t new_rules_buffer_size = old_len + new_len + 2 + rules->length;
    if (new_rules_buffer_size > rules->capacity) {
        // resize needed
        size_t new_capacity = new_rules_buffer_size + 0x100;
        if ((rules->buffer = realloc(rules->buffer, new_capacity)) == NULL) {
            fatal("realloc failure");
        }
        rules->capacity = new_capacity;
    }

    memcpy(rules->buffer + rules->length, old_str, old_len);
    rules->buffer[rules->length + old_len] = ':';
    rules->length += old_len + 1;
    memcpy(rules->buffer + rules->length, new_str, new_len);
    rules->buffer[rules->length + new_len] = ':';
    rules->length += new_len + 1;

    return 0;
}

void apply_rules(Rules* rules, char* msg)
{
    char* old_start = rules->buffer;
    while ((old_start - rules->buffer) < rules->length && *old_start != 0) {
        char* old_end = strchr(old_start, ':');
        char* new_start = old_end + 1;
        char* new_end = strchr(new_start, ':');
        *old_end = 0;
        *new_end = 0;

        strrpl(msg, old_start, new_start);
        *old_end = ':';
        *new_end = ':';

        old_start = new_end + 1;
    }
}

// Return 0 on success, -1 if protocol specification is not followed.
int handle_new_message(int client_socket, Packet* packet, Rules* rules, char* buffer) {
    if (packet->size >= TOTAL_CAP)
    {
        return -1;
    }

    if (packet->size < PACKET_CAP)
    {
        // for 1-part messages, apply rules to first part of message
        apply_rules(rules, packet->message);
        // applying the rules first may shrink packet->message, making the subsequent strcpy more performant
    }

    strcpy(buffer, packet->message);

    // send OK for 1-part messages and for the first part of 2-part messages
    send_(client_socket, (void*)&ok_response, sizeof(Packet), 0);

    if (packet->size < PACKET_CAP)
    {
        return 0;
    }
    else
    {
        // Part 2 of protocol: for 2-part message packets
        char* buffer2 = buffer + (PACKET_CAP - 1);
        size_t recv_amt = packet->size - (PACKET_CAP - 1);
        if (recv_(client_socket, buffer2, recv_amt, 0) != recv_amt)
        {
            return -1;
        }
        apply_rules(rules, buffer);
        // send OK for second part of 2-part messages
        send_(client_socket, (void*)&ok_response, sizeof(Packet), 0);
    }

    return 0;
}

int main()
{
    start_server();
    const int client_socket = await_connection();
    char work_buffer[TOTAL_CAP] = { 0 };
    Rules rules = { .buffer = calloc(RULE_INIT_SZ, 1), .length = 0, .capacity = RULE_INIT_SZ };
    if (rules.buffer == NULL) {
        fatal("calloc failure");
    }
    Packet packet;
    memset(&packet, 0, sizeof(Packet));

    while (1)
    {
        // receive data from the client
        if (recv_(client_socket, (void*)&packet, sizeof(Packet), 0) <= 0) {
            // recv error or client disconnect
            break;
        }

        if (packet.signature != packet_signature || packet.header[sizeof(packet.header) - 1] != 0 || packet.checksum != cc(packet)) {
            break;
        }

        if (strcmp(packet.header, "NEWMESG") == 0)
        {
            if (packet.size < PACKET_CAP) {
                // 1 part
                if (packet.message[packet.size] != 0) {
                    break;
                }
            }
            else {
                // 2 part
                if (packet.message[sizeof(packet.message) - 1] != 0) {
                    break;
                }
            }
            if (handle_new_message(client_socket, &packet, &rules, work_buffer) == -1) {
                // invalid message
                break;
            }
        }
        else if (strcmp(packet.header, "NEWRULE") == 0)
        {
            if (add_rule(packet.message, &rules) == 0)
            {
                send_(client_socket, (void*)&ok_response, sizeof(Packet), 0); // shifts fatal to client side
            }
            else {
                // invalid rule
                break;
            }
        }
        else if (strcmp(packet.header, "USERULE") == 0)
        {
            apply_rules(&rules, work_buffer);
            send_(client_socket, (void*)&ok_response, sizeof(Packet), 0);
        }
        else if (strcmp(packet.header, "GETMESG") == 0)
        {
            send_(client_socket, (void*)&ok_response, sizeof(Packet), 0);
            strcpy(packet.header, "OUTMESG");
            packet.size = strlen(work_buffer);
            memset(&packet.message, 0, sizeof(packet.message));
            strncpy(packet.message, work_buffer, MIN(PACKET_CAP, packet.size));
            packet.checksum = cc(packet);
            send_(client_socket, (void*)&packet, sizeof(Packet), 0);

            if (packet.size > PACKET_CAP) // 2-part protocol
            {
                send_(client_socket, (void*)&work_buffer[PACKET_CAP], packet.size - PACKET_CAP, 0);
            }
        }
        else
        {
            break;
        }
    }

    close_(client_socket);
    stop_server();

    return 0;
}