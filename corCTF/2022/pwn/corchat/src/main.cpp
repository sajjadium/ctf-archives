#include <iostream>
#include <vector>
#include <string>
#include <pthread.h>
#include "server.h"

void printBanner()
{
    std::vector<std::string> banner{
        " ________  ________  ________  ________  ___  ___  ________  _________    \n",
            "|\\   ____\\|\\   __  \\|\\   __  \\|\\   ____\\|\\  \\|\\  \\|\\   __  \\|\\___   ___\\  \n",
            "\\ \\  \\___|\\ \\  \\|\\  \\ \\  \\|\\  \\ \\  \\___|\\ \\  \\\\\\  \\ \\  \\|\\  \\|___ \\  \\_|  \n",
            " \\ \\  \\    \\ \\  \\\\\\  \\ \\   _  _\\ \\  \\    \\ \\   __  \\ \\   __  \\   \\ \\  \\   \n",
            "  \\ \\  \\____\\ \\  \\\\\\  \\ \\  \\\\  \\\\ \\  \\____\\ \\  \\ \\  \\ \\  \\ \\  \\   \\ \\  \\  \n",
            "   \\ \\_______\\ \\_______\\ \\__\\\\ _\\\\ \\_______\\ \\__\\ \\__\\ \\__\\ \\__\\   \\ \\__\\ \n",
            "    \\|_______|\\|_______|\\|__|\\|__|\\|_______|\\|__|\\|__|\\|__|\\|__|    \\|__| \n", "\n"};
    for (const std::string &line : banner)
    {
        std::cout << line;
    }
}

int main(int argc, char *argv[])
{
    printBanner();

    if (argc != 2)
    {
        std::cerr << "[i] Usage: ./corchat_server <port>" << std::endl;
        return -1;
    }

    int port = atoi(argv[1]);

    ChatServer cor_server = ChatServer(port);
    if (cor_server.StartListening() != 0)
        return -1;

    cor_server.MainLoop();

    return 0;
}
