#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <math.h>
#include <float.h>
#include <string.h>
#include "boat.h"
#include <pthread.h>
#include "console.h"
#include <openssl/sha.h>
#include <readline/readline.h>
#include <readline/history.h>
#include <sys/ioctl.h>
#include <asm/termbits.h> 


#define BOAT_NUM 5
boat_t boats[BOAT_NUM];
int slot_size[5] = {0};
int myId = -1;
int mySendSocket = -1;

uint8_t g_logging = 0;
double pi = 4.0 * atan(1.0);

char password_hash[] = {0x55, 0x00, 0xb7, 0xf6, 0x62, 0x2c, 0x0a, 0x79, 
                           0x1c, 0xec, 0x13, 0x28, 0x1f, 0xd9, 0xc2, 0xc3,
                           0x27, 0x91, 0xbe, 0x02, 0x8c, 0x23, 0x1f, 0x94,
                           0x7d, 0xa4, 0x19, 0x5c, 0x3a, 0x9a, 0xfc, 0xb6};

commands_t *commands;
commands_t *dev_commands;

void alloc_commands()
{
    commands = malloc(sizeof(commands_t) * CMD_NUM);
    
    strcpy(commands[0].command, "help");
    commands[0].func = help;
    
    strcpy(commands[1].command, "name boat");
    commands[1].func = set_name;
    
    strcpy(commands[2].command, "status");
    commands[2].func = status;
    
    strcpy(commands[3].command, "vhf");
    commands[3].func = send_vhf;
    
    strcpy(commands[4].command, "safety");
    commands[4].func = send_safety;
    
    strcpy(commands[5].command, "exit");
    commands[5].func = exit;
    
    strcpy(commands[6].command, ".cshelladmin");
    commands[6].func = VHFADMIN;

}
void alloc_dev_commands()
{
    dev_commands = malloc(sizeof(commands_t) * DEV_CMD_NUM);
    
    strcpy(dev_commands[0].command, "send_safety_msg");
    dev_commands[0].func = send_safety_msg;
    
    strcpy(dev_commands[1].command, "send_bin_msg");
    dev_commands[1].func = send_bin_msg;
    
    strcpy(dev_commands[2].command, "send_position");
    dev_commands[2].func = send_position;
    
    strcpy(dev_commands[3].command, "toggle_logging");
    dev_commands[3].func = toggle_logging;
    
    strcpy(dev_commands[4].command, "status");
    dev_commands[4].func = status;

}

boat_t *alloc_boat()
{
    boat_t *boat = calloc(1, sizeof(boat_t));
    return boat;
}

int init_send_socket()
{
    int sock;
    struct sockaddr_in addr;

    // Create socket
    mySendSocket = socket(AF_INET, SOCK_DGRAM, 0);
    if (mySendSocket == -1)
    {
#ifdef DEBUG
        LOG_PRINT("Failed to create socket");
#endif
        return SOCKET_FAIL;
    }
    return STATUS_SUCCESS;
}


void send_frame(const ais_frame_t *pFrame, uint16_t boatID)
{
    // Init socket if needed
    if (mySendSocket == -1)
    {
        init_send_socket();
    }

    struct sockaddr_in addr;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(boatID);
    sendto(mySendSocket, pFrame, 0xff, 0, (struct sockaddr *)&addr, sizeof(addr));
}

void broadcast(const ais_frame_t *pFrame)
{
    // Loop though all boat ports to broadcast message
    for (int i = 0; i < BOAT_NUM; i++)
    {
        uint16_t boatID = PORT + i;
        if (boatID != myId)
        {
            send_frame(pFrame, boatID);
        }        
    }
}

// stolen from https://www.geeksforgeeks.org/program-distance-two-points-earth/# except turned long doubles into doubles..
double toRadians(const double degree)
{
    double one_deg = (pi) / 180;
    return (one_deg * degree);
}
// gets distance in miles between two coordinates 
double distance(double lat1, long double long1,
                     double lat2, long double long2)
{
    // Convert the latitudes
    // and longitudes
    // from degree to radians.
    lat1 = toRadians(lat1);
    long1 = toRadians(long1);
    lat2 = toRadians(lat2);
    long2 = toRadians(long2);
     
    // Haversine Formula
    //https://en.wikipedia.org/wiki/Haversine_formula
    double dlong = long2 - long1;
    double dlat = lat2 - lat1;
 
    double ans = pow(sin(dlat / 2), 2) +
                          cos(lat1) * cos(lat2) *
                          pow(sin(dlong / 2), 2);
 
    ans = 2 * asin(sqrt(ans));
 
    // Radius of Earth in
    // Kilometers, R = 6371
    // Use R = 3956 for miles
    double R = 3956;
     
    // Calculate the result
    ans = ans * R;
 
    return ans;
}

void sha256_password(char *password, char *digest)
{
    char *salt = "Leopard 45";

    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, password, strlen(password));
    SHA256_Update(&sha256, salt, strlen(salt));
    SHA256_Final(digest, &sha256);   
}

uint8_t crc8(uint8_t *ptr, size_t n)
{
    uint8_t crc = 0xff;
    
    for (size_t i = 0; i < n; i++)
    {
        crc ^= ptr[i];
    }
    
    return crc;
}

ais_frame_t *callocFrame()
{
    ais_frame_t *pFrame = (ais_frame_t *)calloc(1, 0xff);
    pFrame->preamble = 0x55555555;
    pFrame->start_flag = 0x7e;
    pFrame->stop_flag = 0x7e;
    return pFrame;
}

void setFrame(ais_frame_t* pFrame)
{
    pFrame->preamble = 0x55555555;
    pFrame->start_flag = 0x7e;
    pFrame->stop_flag = 0x7e;
    return;
}


void listener(int port)
{
    int sock;
    struct sockaddr_in addr;
    socklen_t addr_len = sizeof(addr);
    char buffer[1024];
    int bytes_read;
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1)
    {
        LOG_PRINT("Could not create socket\n");
    }
    LOG_PRINT("Created socket\n");
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
        {
        LOG_PRINT("Could not bind socket\n");
        }
    while(1)
    {
        bytes_read = recvfrom(sock, buffer, 1024, 0, (struct sockaddr *)&addr, &addr_len);
        if (bytes_read < 0)
        {
            perror("No transmission received\n");
            return bytes_read;
        }
        ais_frame_t *pFrame = calloc(1, bytes_read);
        memcpy(pFrame, buffer, bytes_read);
        process_transmission(pFrame);
    }
}

void process_transmission(ais_frame_t *pFrame)
{
    enum MSG_TYPE type = pFrame->type;

    switch(pFrame->type)
    {
        case POS_SCH_REPORT:
        case POS_ASS_REPORT:
        case POS_SPC_REPORT:
            handle_position_report(pFrame);
            break;
        case BIN_ADDR_MSG:
        case BIN_ADDR_BDC:
            handle_bin(pFrame);
            break;
        case BIN_ADDR_ACK:
            break;
        case SAFETY_MSG:
        case SAFETY_BDC:
            handle_safe_report(pFrame);
            break;
        case SAFETY_ACK:
            AIS_SAFETY_ACK_t *pSafetyAck = &pFrame->data;
            LOG_PRINT("SAFETY[%d] copied %u bytes\n", pSafetyAck->boat_id, pSafetyAck->bytes_copied);
            break;
        default:
            LOG_PRINT("Message type %u not implemented... yet.\n", pFrame->type);
    }

    free(pFrame);
}

void handle_safe_report(ais_frame_t *pFrame)
{
    LOG_PRINT("[%u] In handle_safe_report.\n", myId);
    char msg[0x100]; // need to make buffer bigger just because who knows how much data someone might transmit if they were in danger...
    uint32_t copied;
    uint32_t sender_id;
    if (pFrame->type == SAFETY_MSG)
    {
        AIS_SAFETY_MSG_t *safety_msg = &pFrame->data;

        if (safety_msg->dest_id != myId)
        {
            LOG_PRINT("DEBUG NOT MY ID\n");
            return;
        }
        if (safety_msg->slot_size <=3)
            memcpy(&msg, &safety_msg->data, (slot_size[safety_msg->slot_size-1] & 0xff));
        LOG_PRINT("[%u] SAFETY: %s\n", &safety_msg->sender_id, &msg);
        sender_id = safety_msg->sender_id;
        copied = slot_size[safety_msg->slot_size];
    }
    else if (pFrame->type == SAFETY_BDC)
    {
        AIS_SAFETY_BDC_t *safety_msg = &pFrame->data;
        if (safety_msg->slot_size <=3)
            memcpy(&msg, &safety_msg->data, (slot_size[safety_msg->slot_size-1] & 0xff));
        LOG_PRINT("[%d] SAFETY: %s\n", safety_msg->boat_id, &msg);
        sender_id = safety_msg->boat_id;
        copied = slot_size[safety_msg->slot_size];
    }
    else
    {
        LOG_PRINT("Unknown safety message type of %u\n", pFrame->type);
    }
    ais_frame_t *pAck = callocFrame();
    pAck->type = SAFETY_ACK;
    AIS_SAFETY_ACK_t *pSafetyAck = calloc(1, sizeof(AIS_SAFETY_ACK_t));
    pSafetyAck->boat_id = myId;
    pSafetyAck->bytes_copied = copied;
    memcpy(&pAck->data, pSafetyAck, sizeof(AIS_SAFETY_ACK_t));
    pAck->crc = crc8((uint8_t *)pAck, sizeof(ais_frame_t));
    send_frame(pAck, sender_id);
    free(pAck);
}

void handle_position_report(ais_frame_t *pFrame)
{
    
    A_AIS_BDC_t *A_MSG = &pFrame->data;
    double distance_between = distance(boats[0].coords.lat, boats[0].coords.lon, A_MSG->position.lat, A_MSG->position.lon);
    boats[A_MSG->boat_id % BOAT_NUM].coords = A_MSG->position;
    boats[A_MSG->boat_id % BOAT_NUM].active = 1;
    return;
}


void send_scheduled_position_report()
{
    ais_frame_t *pFrame = callocFrame();
    pFrame->type = POS_SCH_REPORT;
    A_AIS_BDC_t *pData = (A_AIS_BDC_t *)pFrame->data;
    pData->boat_id = myId;
    pData->position.lat = boats[0].coords.lat;
    pData->position.lon = boats[0].coords.lon;
    pData->status = under_way_sailing; // I wish
    pFrame->crc = crc8(pFrame->data, sizeof(pFrame->data));
    broadcast(pFrame);
    free(pFrame);
}


void send_safety_report()
{
    ais_frame_t *pFrame = callocFrame();
    pFrame->type = SAFETY_BDC;
    AIS_SAFETY_BDC_t *pData = (AIS_SAFETY_BDC_t *)pFrame->data;
    pData->boat_id = myId;
    pData->slot_size = 1;
    memcpy(&pData->data, "ALL CLEAR!", 11);
    // Calculate CRC
    pFrame->crc = crc8(pFrame->data, sizeof(pFrame->data));
    broadcast(pFrame);
    free(pFrame);
}

void send_binary_encoded_bdc()
{
    ais_frame_t *pFrame = callocFrame();
    pFrame->type = BIN_ADDR_BDC;
    AIS_BAM_BDC_t *pData = (AIS_BAM_BDC_t *) &pFrame->data;
    pData->boat_id = myId;
    pData->slot_size = 2;
    memcpy(&pData->data, "Beautiful Weather Today!", 25);
    pFrame->crc = crc8(pFrame->data, sizeof(pFrame->data));
    broadcast(pFrame);
    free(pFrame);
}
void handle_bin(ais_frame_t *pFrame)
{
    char data[SLOT_MAX] = {0};
    if (crc8(pFrame->data, sizeof(pFrame->data)) != pFrame->crc)
    {
        LOG_PRINT("CRC mismatch, dropping frame.\n");
        return;
    }

    if (pFrame->type == BIN_ADDR_BDC)
    {
        AIS_BAM_BDC_t *pData = (AIS_BAM_BDC_t *)pFrame->data;
        if (pData->slot_size <=3)
            memcpy(data, &pData->data, (slot_size[pData->slot_size-1] & 0xff));
        LOG_PRINT("[%u] Received binary encoded broadcast: %s\n",pData->boat_id, &data);
        if (strstr(data, "boat_name: ") != NULL) {
            char *boat_name = strstr(data, "boat_name: ");
            boat_name += 11;
            strncpy(&boats[pData->boat_id % BOAT_NUM].boat_name, boat_name, 0x10);
        }
    }
    else if (pFrame->type == BIN_ADDR_MSG)
    {
        
        AIS_BAM_MSG_t *pData = (AIS_BAM_MSG_t *)pFrame->data;
        if (pData->dest_id != myId)
        {
            LOG_PRINT("Message not for me, dropping frame.\n");
            return;
        }
        if (pData->slot_size <=3)
            printf("copying %d\n",  (slot_size[pData->slot_size-1] & 0xff));
            memcpy(data, &pData->data, (slot_size[pData->slot_size-1] & 0xff));
        LOG_PRINT("[%u] Received binary encoded message: %s\n", pData->boat_id, &data);
    }
    else
    {
        LOG_PRINT("Unknown binary encoded message type: %d\n", pFrame->type);
    }
}

void broadcast_name(char *name)
{
    // set up frame
    char data[SLOT_MAX] = {0};
    ais_frame_t *pFrame = callocFrame();
    // broadcast a binary encoded msg
    pFrame->type = BIN_ADDR_BDC;
    AIS_BAM_BDC_t *pData = (AIS_BAM_BDC_t *) &pFrame->data;
    pData->boat_id = myId;
    pData->slot_size = 2;
    snprintf(data, SLOT_MAX, "boat_name: %s", name);
    memcpy(&pData->data, data, slot_size[1]);
    // Calculate CRC
    pFrame->crc = crc8(pFrame->data, sizeof(pFrame->data));
    // broadcast msg
    broadcast(pFrame);
    free(pFrame);
}
void listen_loop(int port)
{
    listener(port);
}

void robo_loop()
{
    int ctr = 0;
    while (1)
    {
        // Robot boats just send position every so often
        if (ctr % 8 == 0)
            send_safety_report();
        if (ctr % 7 == 0)
            send_binary_encoded_bdc();
        if (ctr % 4 == 0)
            broadcast_name(&boats[0].boat_name);
        send_scheduled_position_report();
        sleep(5);
        // randomly increase or decrase the lon and lat of boat
        boats[0].coords.lat += (rand() % 2) ? 0.0005 : -0.0005;
        boats[0].coords.lon += (rand() % 2) ? 0.0005 : -0.0005;

        ctr++;
    }
}

void send_vhf()
{
    // set up frame
    ais_frame_t *pFrame = callocFrame();
    char data[SLOT_MAX] = {0};
    char *usr_msg;
    // send bcd message
    pFrame->type = BIN_ADDR_BDC;
    AIS_BAM_BDC_t *pData = (AIS_BAM_BDC_t *) &pFrame->data;
    pData->boat_id = myId;
    pData->slot_size = 3;
    usr_msg = readline("Enter message to broadcast over vhf: ");
    snprintf(data, SLOT_MAX, "vhf: %s", usr_msg);
    printf("sent %s\n", data);
    memcpy(&pData->data, data, slot_size[3]);
    pFrame->crc = crc8(pFrame->data, sizeof(pFrame->data));
    broadcast(pFrame);
    free(pFrame);
    free(usr_msg);
}

void send_safety()
{
    ais_frame_t *pFrame = callocFrame();
    char data[SLOT_MAX] = {0};
    char *usr_msg;
    pFrame->type = SAFETY_BDC;
    AIS_SAFETY_BDC_t *pData = (AIS_SAFETY_BDC_t *) &pFrame->data;
    pData->boat_id = myId;
    pData->slot_size = 3;
    usr_msg = readline("Enter Safety Message: ");
    snprintf(data, SLOT_MAX, "%s", usr_msg);
    memcpy(&pData->data, data, slot_size[3]);
    broadcast(pFrame);
    free(pFrame);
    free(usr_msg);
}

void help()
{
    printf("Available commands:\n");
    for (int i = 0; i < CMD_NUM-1; i++)
    {
        printf("\t%s\n", commands[i].command);
    }
}
void status()
{
    for (int i = 0; i < BOAT_NUM; i++)
    {
        if (boats[i].active == 0)
            continue;
        double d = distance(boats[i].coords.lat, boats[i].coords.lon, boats[0].coords.lat, boats[0].coords.lon);
        printf("\tBoat %d: %s is %.2f miles away @ %.4f %.4f\n", i, boats[i].boat_name, d, boats[i].coords.lat, boats[i].coords.lon);

    }
}

void set_name()
{
    char buff[0x10];
    printf("Enter new name:\n");
    read(STDIN_FILENO, &buff, 0x10);
    buff[0x10-1] = '\0';
    memcpy(&boats[0].boat_name, buff, 0x10);
    printf("\tNew name: %s\n", &boats[0].boat_name);
}

void VHFADMIN()
{
    
    char *username, *password;
    username = readline("Enter username: ");
    password = readline("Enter password: ");
    char l_password_hash[65] = {0};
    sha256_password(password, l_password_hash);
    if (strcmp(username, "admin") == 0 && strcmp(l_password_hash, password_hash) == 0)
    {
        printf("Welcome admin\n");
        free(username);
        free(password);
        dev_console();
    }
    else
    {
        printf("Incorrect username or password\n");
        free(username);
        free(password);
    }
}

void toggle_logging()
{
    g_logging ^= 1;
    printf("logging is now %d\n", g_logging);
}

void console()
{
    char *buf;
    help();
    while (1)
    {
        buf = readline("Enter command: ");
        for (int i = 0; i < CMD_NUM; i++)
        {
            if (strcmp(buf, commands[i].command) == 0)
            {
                commands[i].func();
                break;
            }
        }
        free(buf);
    }
}


void send_safety_msg()
{
    char *inp1, *inp2;
    
    char msg[0xff] = {0};
    int receiver_id;
    int8_t slot_size;
    ais_frame_t *pFrame = callocFrame();
    pFrame->type = SAFETY_MSG;
    AIS_SAFETY_MSG_t *pData = (AIS_SAFETY_MSG_t *) &pFrame->data;
    pData->sender_id = myId;
    inp1 = readline("Enter slot size: ");
    slot_size = atoi(inp1);
    pData->slot_size = slot_size & 0xff;
    inp2 = readline("Enter receiver id: ");
    receiver_id = atoi(inp2);
    pData->dest_id = receiver_id;
    // set_terminal_sane_mode();
    read(0, &msg, 0xf0);
    //set_terminal_raw_mode();
    memcpy(&pData->data, msg, 0xf0);
    // send msg
    send_frame(pFrame, receiver_id);
    printf("Sent to boat %d\n", receiver_id);
    free(pFrame);
    free(inp1);
    free(inp2);
}
void send_bin_msg()
{
    char *inp1, *inp2;
    char msg[0xff] = {0};
    int receiver_id;
    uint8_t slot_size;
    ais_frame_t *pFrame = callocFrame();
    pFrame->type = BIN_ADDR_MSG;
    AIS_BAM_MSG_t *pData = (AIS_BAM_MSG_t *) &pFrame->data;
    pData->boat_id = myId;
    // read in slotsize
    inp1 = readline("Enter slot size: ");
    slot_size = atoi(inp1);
    pData->slot_size = slot_size & 0xff;
    inp2 = readline("Enter receiver id: ");
    receiver_id = atoi(inp2);
    pData->dest_id = receiver_id;
    read(0, &msg, 0xf0);
    memcpy(&pData->data, msg, 0xf0);
    pFrame->crc = crc8(pFrame->data, sizeof(pFrame->data));
    send_frame(pFrame, receiver_id);
    printf("Sent to boat %d\n", receiver_id);
    free(pFrame);
    free(inp1);
    free(inp2);
}
void send_position()
{
    // send the position of boat[0]
    int receiver_id;
    char *inp1;
    ais_frame_t *pFrame = callocFrame();
    pFrame->type = POS_SCH_REPORT;
    A_AIS_MSG_t *pData = (A_AIS_MSG_t *) &pFrame->data;
    pData->boat_id = myId;
    pData->position.lat = boats[0].coords.lat;
    pData->position.lon = boats[0].coords.lon;
    // get receiver boat
    inp1 = readline("Enter receiver id: ");
    receiver_id = atoi(inp1);
    pData->dest_id = receiver_id;
    // send msg
    send_frame(pFrame, receiver_id);
    printf("Sent to boat %d\n", receiver_id);
    free(pFrame);
}
void dev_help()
{
    // for dev command print it out
    printf("Commands:\n");
    for (int i = 0; i < DEV_CMD_NUM - 1; i++)
    {
        printf("\t%s\n", dev_commands[i].command);
    }

}

void dev_console()
{
    char *buf;
    while (1)
    {
        buf = readline("[ADMIN] Enter command: ");
        for (int i = 0; i < DEV_CMD_NUM; i++)
        {
            if (strcmp(buf, dev_commands[i].command) == 0)
            {
                dev_commands[i].func();
                break;
            }
        }
        free(buf);
    }
}

void run_user(int port)
{
    pthread_t listen_thread;
    pthread_t sender_thread;
    pthread_t user_thread;
    pthread_create(&listen_thread, NULL, listen_loop, port);
    pthread_create(&sender_thread, NULL, robo_loop, NULL);
    pthread_create(&user_thread, NULL, console, NULL);
    pthread_join(listen_thread, NULL);
    pthread_join(sender_thread, NULL);
    pthread_join(user_thread, NULL);
}

void run_robo(int port)
{
    pthread_t listen_thread;
    pthread_t sender_thread;
    pthread_create(&listen_thread, NULL, listen_loop, port);
    pthread_create(&sender_thread, NULL, robo_loop, NULL);
    pthread_join(listen_thread, NULL);
    pthread_join(sender_thread, NULL);
}

int main(int argc, char *argv[])
{
    // Seed RNG if not in debug mode
    int seed = 0;
#ifndef DEBUG
    int fd_rand = open("/dev/urandom", O_RDONLY);
    read(fd_rand, &seed, sizeof(seed));
#endif
    srand(seed);
    slot_size[0] = 16;
    slot_size[1] = 53;
    slot_size[2] = 90;
    int manned = 0;
    int port = 0;
    if (argc < 3)
    {
        printf("Usage: %s 0 PORT\n", argv[0]);
        printf("Usage: %s 1 PORT\n", argv[0]);
        return 1;
    }
    manned = atoi(argv[1]);
    port = atoi(argv[2]);
    boats[0].coords.lat = 26.0;
    boats[0].coords.lon = -77.0;
    if (port > 4100 || port < 4001)
    {
        printf("Invalid port\n");
        return 1;
    }
    myId = port;
    if (myId == 4001)
        strcpy(&boats[0].boat_name, "Simple Life");
    if (myId == 4002)
        strcpy(&boats[0].boat_name, "robot boat");
    if (myId == 4003)
        strcpy(&boats[0].boat_name, "My Ideal");
    if (myId == 4004)
        strcpy(&boats[0].boat_name, "Seashine");
    if (myId == 4004)
        strcpy(&boats[0].boat_name, "Skylark");

// 26.5500 -76.9000
    if (manned > 0)
    {
        alloc_commands();
        alloc_dev_commands();
        run_user(port);
    }
    else
    {
        sleep(rand() % 3);
        run_robo(port);
    }
}