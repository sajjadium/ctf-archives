#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <signal.h>
#include <sys/wait.h>
#include <winscard.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define NUM_PID 2
#define TIMEOUT 5
#define MAX_BUF 384
#define MAX_REQ_BUF 1024

#define HOST "127.0.0.1"
#define PORT 19091
#define BK_HOST "backend"
#define BK_PORT 29092

struct card
{
    char card_holder[32];
    char card_number[20];
    unsigned short card_exp_year;
    unsigned short card_exp_month;
    unsigned short card_cvv;
    unsigned int card_money;
};

typedef struct card Card;

int connection_sock;

void cleanup()
{
    char *err = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\nConnection: close\r\n\r\n";
    send(connection_sock, err, strlen(err), 0);
    close(connection_sock);
    exit(-1);
}

void exception_handler(int signum)
{
    cleanup();
}

LONG check_transmit(char* buf, DWORD bufLen)
{
    if (bufLen < 2)
        return -1;
    if (buf[bufLen-2] == '\x90' && buf[bufLen-1] == '\x00')
        return 0;

    return -1;
}

LONG get_readers(LPSCARDCONTEXT hContext, LPSTR readersBuf)
{
    LONG rv;
    DWORD readersLen;

    readersLen = SCARD_AUTOALLOCATE;
    rv = SCardListReaders(*hContext, NULL, readersBuf, &readersLen);
    if (rv != SCARD_S_SUCCESS)
        return rv;

    return SCARD_S_SUCCESS;
}

LONG connect_card(LPSCARDCONTEXT hContext, LPSTR readersBuf, LPSCARDHANDLE hCard)
{
    LONG rv;
    DWORD dwActiveProtocol;

    rv = SCardConnect(*hContext, readersBuf, SCARD_SHARE_SHARED, SCARD_PROTOCOL_ANY, hCard, &dwActiveProtocol);
    if (rv != SCARD_S_SUCCESS)
        return rv;

    return SCARD_S_SUCCESS;
}

LONG card_status(LPSCARDHANDLE hCard, LPSTR readersBuf, LPBYTE atrBuf)
{
    LONG rv;
    DWORD readersLen;
    DWORD atrLen;
    DWORD pdwState;
    DWORD pdwProtocol;

    readersLen = SCARD_AUTOALLOCATE;
    rv = SCardStatus(*hCard, readersBuf, &readersLen, &pdwState, &pdwProtocol, atrBuf, &atrLen);
    if (rv != SCARD_S_SUCCESS)
        return rv;

    return SCARD_S_SUCCESS;
}

LONG transmit(SCARDHANDLE hCard, LPCBYTE sendBuf, DWORD sendLen, LPBYTE transmitBuf, DWORD *transmitLen)
{
    LONG rv;
    SCARD_IO_REQUEST pioSendPci;
    DWORD recvLen;
    BYTE recvBuf[MAX_BUF];
    
    recvLen = sizeof(recvBuf);
    rv = SCardTransmit(hCard, &pioSendPci, sendBuf, sendLen, NULL, recvBuf, &recvLen);
    if (rv != SCARD_S_SUCCESS)
        return rv;

    memcpy(transmitBuf, recvBuf, recvLen);
    *transmitLen = recvLen;

    return SCARD_S_SUCCESS;
}

LONG init_scard(LPSCARDCONTEXT hContext, LPSCARDHANDLE hCard, LPSTR *readersBuf, LPBYTE atrBuf)
{
    LONG rv;

    rv = SCardEstablishContext(SCARD_SCOPE_SYSTEM, NULL, NULL, hContext);
    if (rv != SCARD_S_SUCCESS)
        return rv;

    rv = get_readers(hContext, (LPSTR)readersBuf);
    if (rv != SCARD_S_SUCCESS)
        return rv;

    rv = connect_card(hContext, *readersBuf, hCard);
    if (rv != SCARD_S_SUCCESS)
        return rv;

    rv = card_status(hCard, (LPSTR)readersBuf, atrBuf);
    if (rv != SCARD_S_SUCCESS)
        return rv;

    return SCARD_S_SUCCESS;
}

LONG do_transmit(LPSCARDHANDLE hCard, Card* credit)
{
    LONG rv;
    BYTE transmitBuf[MAX_BUF];
    DWORD transmitLen;

    BYTE cmd1[] = { 0x00, 0xA4, 0x04, 0x00, 0x10, 0xCA, 0x44, 0x6F, 0x66, 0xD3, 0x52, 0x89, 0x58, 0xAA, 0x06, 0xC6, 0xEB, 0xF5, 0x57, 0x6B, 0x3E };
    rv = transmit(*hCard, cmd1, sizeof(cmd1), transmitBuf, &transmitLen);
    if (rv != SCARD_S_SUCCESS)
        return rv;
    if (check_transmit(transmitBuf, transmitLen) < 0)
        return -1;

    BYTE cmd2[] = { 0x00, 0xB2, 0x00, 0x00, 0x40 };
    rv = transmit(*hCard, cmd2, sizeof(cmd2), transmitBuf, &transmitLen);
    if (rv != SCARD_S_SUCCESS)
        return rv;
    if (check_transmit(transmitBuf, transmitLen) < 0)
        return -1;

    memcpy(credit, transmitBuf, sizeof(Card));

    return SCARD_S_SUCCESS;
}

void fini_scard(LPSCARDCONTEXT hContext, LPSCARDHANDLE hCard, LPSTR *readersBuf)
{
    LONG rv;

    rv = SCardDisconnect(*hCard, SCARD_LEAVE_CARD);
    rv = SCardReleaseContext(*hContext);
}

LONG connect_scard(Card *credit)
{
    LONG rv;
    SCARDCONTEXT hContext;
    SCARDHANDLE hCard;
    LPSTR readersBuf;
    BYTE atrBuf[MAX_ATR_SIZE];

    rv = init_scard(&hContext, &hCard, &readersBuf, atrBuf);
    if (rv == SCARD_S_SUCCESS)
    {
        if (memcmp(atrBuf, "\x3B\xFC\x18\x00\x00\x81\x31\xFE\x45\x80\x73\xC8\x21\x13\x66\x02\x04\x03\x55\x00\x02\xD2", 22))
            cleanup();

        rv = do_transmit(&hCard, credit);
    }

    fini_scard(&hContext, &hCard, &readersBuf);
    return rv;
}

void connect_backend(char *host, char *port, char **data, size_t *dataLen)
{
    int sock_fd;
    size_t n, curN;
    struct sockaddr_in backend_addr;
    struct hostent *server;

    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0)
        cleanup();

    server = gethostbyname(host);
    if (!server)
        cleanup();

    bzero(&backend_addr, sizeof(backend_addr));
    backend_addr.sin_family = AF_INET;
    backend_addr.sin_addr.s_addr = *((unsigned long *)server->h_addr);
    backend_addr.sin_port = htons(atoi(port));

    if (connect(sock_fd, (struct sockaddr*)&backend_addr, sizeof(backend_addr)) < 0)
        cleanup();

    send(sock_fd, *data, *dataLen, 0);
    bzero(*data, MAX_REQ_BUF);
    
    n = 0;
    do
    {
        curN = read(sock_fd, *data + n, MAX_REQ_BUF - n);
        n += curN;
    } while (n < MAX_REQ_BUF && curN > 0);
    *dataLen = n;
    close(sock_fd);
}

void route(int fd, char* host, char* port, char* method, char *path, size_t reqLen, char* reqBuf)
{
    char *flagBuf;
    Card *credit;
    char *buf;
    size_t bufLen;
    
    if (!memcmp(method, "BUY_FLAG", 8) && !memcmp(path, "buy_flag", 8))
    {
        credit = calloc(1, sizeof(Card));
        if (connect_scard(credit) == SCARD_S_SUCCESS)
        {
            flagBuf = calloc(1, 4096);
            bufLen = snprintf(flagBuf, 4096, "SPECIAL_METHOD_TO_BUY_FLAG /buy_flag?");
            bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "card_holder=%s&", credit->card_holder);
            bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "card_number=%s&", credit->card_number);
            bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "card_exp_year=%hu&", credit->card_exp_year);
            bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "card_exp_month=%hu&", credit->card_exp_month);
            bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "card_cvv=%hu&", credit->card_cvv);
            bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "card_money=%u HTTP/1.1\r\n", credit->card_money);
            bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "Content-Type: application/x-www-form-urlencoded\r\n");
            bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "Content-Length: %u\r\n\r\npadding=", 0x80*3+0x80*6+8);

            int i;
            for (i = 0; i < 0x80; ++i)
                bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "%%%02hhx", i);

            for (i = 0x80; i < 0xc0; ++i)
                bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "%%c2%%%02hhx", i);

            for (i = 0x80; i < 0xc0; ++i)
                bufLen += snprintf(flagBuf+bufLen, 4096-bufLen, "%%c3%%%02hhx", i);

            connect_backend(host, port, &flagBuf, &bufLen);
            write(fd, flagBuf, bufLen);
            free(flagBuf);
            return;
        }
        free(credit);
    }

    buf = calloc(1, MAX_REQ_BUF);
    memcpy(buf, reqBuf, reqLen);
    bufLen = reqLen;
    connect_backend(host, port, &buf, &bufLen);
    write(fd, buf, bufLen);
    free(buf);
}

size_t read_input(int fd, char *buf, size_t sz)
{
    size_t n;

    n = read(fd, buf, sz - 1);

    buf[n] = 0;
    return n;
}

void connection_handler(int sock_fd)
{
    char request[MAX_REQ_BUF] = {};
    char method[MAX_BUF] = {};
    char path[MAX_BUF] = {};
    char port[MAX_BUF] = {};
    char host[MAX_BUF] = {};
    size_t n = 0;
    size_t reqLen = 0;

    connection_sock = sock_fd;
    signal(SIGALRM, exception_handler);
    signal(SIGABRT, exception_handler);
    alarm(TIMEOUT);

    snprintf(host, MAX_BUF, "%s", BK_HOST);
    snprintf(port, MAX_BUF, "%d", BK_PORT);

    reqLen = read_input(sock_fd, request, MAX_REQ_BUF);

    n = sscanf(request, "%s /%s HTTP/1.1", method, path);
    if (n != 2)
        snprintf(path, MAX_BUF, "500");

    route(sock_fd, host, port, method, path, reqLen, request);

    close(sock_fd);
    exit(0);
}

int main(void)
{
    int server_fd;
    int accepted_client_fd;
    struct sockaddr_in serverInfo;
    struct sockaddr_in clientInfo;
    socklen_t optval = 1;
    pid_t pid[50];
    int pid_n = 0;

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0)
        exit(-1);

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, (void *)&optval, sizeof(optval)) != 0)
        exit(-1);

    int addrlen = sizeof(clientInfo);
    bzero(&serverInfo, sizeof(serverInfo));

    serverInfo.sin_family = PF_INET;
    serverInfo.sin_addr.s_addr = INADDR_ANY;
    serverInfo.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr*)&serverInfo, sizeof(serverInfo)) < 0)
        exit(-1);

    if (listen(server_fd, NUM_PID) < 0)
        exit(-1);

    while (1)
    {
        accepted_client_fd = accept(server_fd, (struct sockaddr*)&clientInfo, &addrlen);

        if (accepted_client_fd < 0)
            exit(-1);

        pid_t pid_c = fork();
        if (pid_c == 0)
            connection_handler(accepted_client_fd);
        else
        {
            pid[pid_n++] = pid_c;
            if (pid_n >= NUM_PID)
            {
                for (pid_n = 0; pid_n < NUM_PID; ++pid_n)
                    waitpid(pid[pid_n], NULL, 0);
                pid_n = 0;
            }
        }
    }
}