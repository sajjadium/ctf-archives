
#define WIN32_LEAN_AND_MEAN
#define _CRT_SECURE_NO_WARNINGS

#include <Windows.h>
#include <winsock2.h>
#include <WS2tcpip.h>
#include <stdlib.h>
#include <stdio.h>

#pragma comment (lib, "Ws2_32.lib")

#define DEFAULT_BUFLEN 512
#define DEFAULT_PORT "31337"
#define FILENAME_LEN 0x20
#define DEFAULT_PATH "C:\\"

int send_formatted_string(SOCKET socket, char* buffer, int buf_len, char* format, ...) {
    va_list _ArgList;
    __crt_va_start(_ArgList, format);
#pragma warning(suppress:28719)    // 28719
    int result = vsnprintf(buffer, buf_len, format, _ArgList);
    __crt_va_end(_ArgList);

    int iSendResult = send(socket, buffer, strlen(buffer), 0);
    if (iSendResult == SOCKET_ERROR) {
        return 1;
    }

    return 0;
}

int recv_int(SOCKET socket) {
    int iResult = 0x00;
    char recvbuf[DEFAULT_BUFLEN];

    iResult = recv(socket, recvbuf, sizeof(recvbuf), 0);
    if (iResult <= 0) {
        return 0;
    }
    iResult = atoi(recvbuf);
    if (iResult > 0) {
        return iResult;
    }
    return 0x00;
}

int recv_send_loop(SOCKET socket) {
    char recvbuf[DEFAULT_BUFLEN] = { 0 };
    int recvbuflen = DEFAULT_BUFLEN;
    char* filename = NULL;
    char* filebuf = NULL;
    char* file_path = NULL;
    int filebuf_len = 0;
    int res = 0;

    // Initialize filename buffer
    filename = malloc(FILENAME_LEN + 1);
    if (filename == NULL)
    {
        return 1;
    }

    file_path = malloc(MAX_PATH + 1);
    if (file_path == NULL)
    {
        free(filename);
        return 1;
    }

    // Receive until the peer shuts down the connection
    do {
        send_formatted_string(socket, (char*)recvbuf, sizeof(recvbuf), (char*)"Filename:\n");

        // Fill filename buffer
        memset(filename, 0, FILENAME_LEN + 1);
        res = recv(socket, (char*)filename, FILENAME_LEN, 0);
        if (res <= 0) {
            res = 1;
            break;
        }

        // Check if filename is path
        if (strstr(filename, "\\") != 0 || strstr(filename, "/") != 0)
        {
            send_formatted_string(socket, (char*)recvbuf, sizeof(recvbuf), (char*)"Filename can't contain \"\\\" or \"/\"!\n");
            res = 1;
            break;
        }
        char* x = strrchr(filename, 0xa);
        if (x != 0)
        {
            x[0] = 0;
        }

        // Get size of the file to save
        send_formatted_string(socket, (char*)recvbuf, sizeof(recvbuf), (char*)"File size:\n");
        filebuf_len = recv_int(socket);
        if (filebuf_len < 0 || filebuf_len > 0x10000) {
            send_formatted_string(socket, (char*)recvbuf, sizeof(recvbuf), (char*)"File too big\n");
            res = 1;
            break;
        }

        if (filebuf_len == 0) {
            send_formatted_string(socket, (char*)recvbuf, sizeof(recvbuf), (char*)"File size invalid\n");
            res = 1;
            break;
        }

        // Initialize file buffer
        filebuf = malloc(filebuf_len);
        if (filebuf == NULL)
        {
            res = 1;
            break;
        }
        memset(filebuf, 0x00, filebuf_len);

        send_formatted_string(socket, (char*)recvbuf, sizeof(recvbuf), (char*)"File:\n");

        // Fill file buffer
        res = recv(socket, (char*)filebuf, filebuf_len, 0);
        if (res <= 0) {
            res = 1;
            break;
        }

        // Save to file
        memset(file_path, 0, MAX_PATH + 1);
        strcat(file_path, DEFAULT_PATH);
        strcat(file_path, filename);

        HANDLE file_handle = CreateFileA(file_path, GENERIC_READ | GENERIC_WRITE, 0, NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
        if (file_handle == INVALID_HANDLE_VALUE)
        {
            res = 1;
            break;
        }

        res = 0;
        if (!WriteFile(file_handle, filebuf, filebuf_len, &res, NULL) || res != filebuf_len)
        {
            send_formatted_string(socket, (char*)recvbuf, sizeof(recvbuf), (char*)"File save failed.\n\n");

            res = 1;
            break;
        }

        free(filebuf);
        CloseHandle(file_handle);

        send_formatted_string(socket, (char*)recvbuf, sizeof(recvbuf), (char*)"File saved in %s.\n\n", file_path);

        res = 0;
    } while (TRUE);

    send_formatted_string(socket, (char*)recvbuf, sizeof(recvbuf), (char*)"Failed.\n\n");

    free(file_path);
    free(filename);
    return res;
}

int main()
{
    // Mitigate dropping file before full encryption
    Sleep(1000);

    WSADATA wsaData;
    int iResult;

    SOCKET ListenSocket = INVALID_SOCKET;
    SOCKET ClientSocket = INVALID_SOCKET;

    struct addrinfo* result = NULL;
    struct addrinfo hints;


    // Initialize Winsock
    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0) {
        printf("WSAStartup failed with error: %d\n", iResult);
        return 1;
    }

    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    hints.ai_flags = AI_PASSIVE;

    // Resolve the server address and port
    iResult = getaddrinfo(NULL, DEFAULT_PORT, &hints, &result);
    if (iResult != 0) {
        printf("getaddrinfo failed with error: %d\n", iResult);
        WSACleanup();
        return 1;
    }

    // Create a SOCKET for connecting to server
    ListenSocket = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
    if (ListenSocket == INVALID_SOCKET) {
        printf("socket failed with error: %ld\n", WSAGetLastError());
        freeaddrinfo(result);
        WSACleanup();
        return 1;
    }

    // Setup the TCP listening socket
    iResult = bind(ListenSocket, result->ai_addr, (int)result->ai_addrlen);
    if (iResult == SOCKET_ERROR) {
        printf("bind failed with error: %d\n", WSAGetLastError());
        freeaddrinfo(result);
        closesocket(ListenSocket);
        WSACleanup();
        return 1;
    }

    freeaddrinfo(result);

    iResult = listen(ListenSocket, SOMAXCONN);
    if (iResult == SOCKET_ERROR) {
        printf("listen failed with error: %d\n", WSAGetLastError());
        closesocket(ListenSocket);
        WSACleanup();
        return 1;
    }

    while (TRUE)
    {
        // Accept a client socket
        ClientSocket = accept(ListenSocket, NULL, NULL);
        if (ClientSocket == INVALID_SOCKET) {
            printf("accept failed with error: %d\n", WSAGetLastError());
            closesocket(ListenSocket);
            continue;
        }

        if (recv_send_loop(ClientSocket) != 0)
        {
            closesocket(ClientSocket);
            continue;
        }

        // shutdown the connection since we're done
        iResult = shutdown(ClientSocket, SD_SEND);
        if (iResult == SOCKET_ERROR) {
            printf("shutdown failed with error: %d\n", WSAGetLastError());
            closesocket(ClientSocket);
            continue;
        }

        closesocket(ClientSocket);
    }

    // cleanup
    closesocket(ListenSocket);
    WSACleanup();

    return 0;
}