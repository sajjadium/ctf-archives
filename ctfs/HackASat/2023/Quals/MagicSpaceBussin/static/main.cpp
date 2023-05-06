#include <iostream>
#include <limits>
#include <csignal>
#include <unistd.h>
#include "bus.h"
#include "startracker.h"

StarTracker* st1 = nullptr;
StarTracker* st2 = nullptr;

void goodbye(){
    std::cout << "Goodbye!" << std::endl;
    exit(0);
}

void flushcin(){
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

bool checkInput(){
    if( std::cin.fail() )
    {
        flushcin();

        std::cout << "bad input" << std::endl;
        return false;
    }
    return true;
}



void handle_msg(StarTracker* st){
    st->handle_msg();
}

void send_msg(){
    SB_Bus* bus = SB_Bus::GetInstance();

    std::string user_input;
    std::uint8_t msg_id = 0;
    std::uint8_t pipe_id = 0;
    std::uint64_t cur_input = 0;
    bool ishex = false;
    
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    std::cout << "msg_id: " << std::flush;
    std::cin >> cur_input;
    msg_id = static_cast<std::uint8_t>(cur_input);

    std::cout << "pipe_id: " << std::flush;
    std::cin >> cur_input;    
    pipe_id = static_cast<std::uint8_t>(cur_input);

    std::cout << "hex: " << std::flush;
    std::cin >> ishex;

    flushcin();
    checkInput();
    std::cout << "Message to post on bus: " << std::flush;
    std::getline(std::cin, user_input);

    bus->SendMsg(user_input, ishex, pipe_id, msg_id);
}

void menu(){
    std::cout<< "1: Post message on bus" << std::endl;
    std::cout<< "2: Handle startracker 1 messages" << std::endl;
    std::cout<< "3: Handle startracker 2 messages" << std::endl;
    std::cout<< "4: Exit" << std::endl;
    std::cout<< "> " << std::flush;
}

void processChoice( int choice )
{
    switch( choice )
    {
        case 1:
            send_msg();
            break;
        case 2:
            handle_msg(st1);
            break;
        case 3:
            handle_msg(st2);
            break;
        case 4:
            std::cout << "Goodbye!" << std::endl;
            exit(0);
        default:
            std::cout << "Invalid choice!" << std::endl;
            menu();
            break;
    }
}

void timeout_func(int signo){
    LOG_ERR("Oops. You ran out of time. Goodbye!\n");
    exit(-1);
}

int main(void){
    // setvbuf(stdout, NULL, _IONBF, 0);
    // setvbuf(stdin, NULL, _IONBF, 0);
    // setvbuf(stderr, NULL, _IONBF, 0);

    // Shamelessly stolen from pedant
    int timeout = 120;
    char *timeout_str = getenv("TIMEOUT");
    if (timeout_str) {
        timeout = atoi(timeout_str);
    }
    signal(SIGALRM, timeout_func);
    alarm(timeout+2);
    signal(SIGPIPE, SIG_IGN);

    int choice = 0;
    st1 = new StarTracker{};
    st2 = new StarTracker{};

    std::cout << "startracker 1 pipe_id: " << (uint16_t)st1->get_pipe_id() << std::endl;
    std::cout << "startracker 2 pipe_id: " << (uint16_t)st2->get_pipe_id() << std::endl;
    
    while(true){
        {
            menu();

            std::cin >> choice;
            std::cout << std::endl;

            if( !checkInput() ) continue;

            processChoice(choice);
        }
    }
}