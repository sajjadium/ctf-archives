#include <iostream>
#include <limits>
#include <string>
#include <cstdlib>
#include <cstring>
#include <csignal>
#include <unistd.h>

#define USERINPUT 1

#define LOG_ERR(...) fprintf(stderr, __VA_ARGS__)

void goodbye(){
    std::cout << "Goodbye!" << std::endl;
    exit(0);
}

void flushcin(){
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

void get_flag(){
    char *flag = nullptr;

    flag = getenv("FLAG");
    if(!flag){
        flag = "flag{CONTACT_AN_ADMIN}";
    }
    std::cout << "Here ya go: " << flag << std::endl;

    exit(0);
}

class Warning{
    public:
        Warning( );
        ~Warning();
        void get_str();
        void get_input();
        void jump_around(char *start, char *end, char *uncompressed, size_t uncomp_len);
        void output();
        bool check(uint8_t lvl);
    protected:
        int a;
        int b;
        int c;
        char buf[0x10C];
};

// Pack it up, pack it in, let me begin
void Warning::jump_around(char *start,
                          char *end,
                          char *uncompressed,
                          size_t uncomp_len){
    // wow this whole function seems so contrived
    // it makes literally no sense
    char *uptr = uncompressed;
    char *bptr = start;
    // The bug in this function would never b a bug in real life
    while(bptr < end && uptr < (uncompressed + uncomp_len)){
        size_t ulen;
        size_t pos = 0;
        char name[63] = {0};

#if !USERINPUT
		if (!convert_label(start, end, ptr, name, NS_MAXLABEL,
					&pos, &comp_pos))
			goto out;

        /*
        * Copy the uncompressed resource record, type, class and \0 to
        * tmp buffer.
        */
#else
        // Give me your con man name
        std::cout << "> ";
        fgets(name, sizeof(name), stdin);

		ulen = strnlen(name, sizeof(name));
#endif
        // Error checking, thats good
        if((uptr - uncompressed) > uncomp_len){
            return;
        }
        strncpy(uptr, name, uncomp_len - (uptr - uncompressed));
        // C++ but pointer math? :thinking_face:
        uptr += ulen;
		*uptr++ = '\0';

        bptr += pos;

        memcpy(uptr, bptr, 10);

        bptr += 10;
        uptr += 10;
    }

    return;
}

void Warning::get_input(){
    struct {    
        char buf1[1025];
        char buf2[257];
    } input_bufs = {0};

    flushcin();
    std::cout << "> ";
    if(!fgets(input_bufs.buf1, sizeof(input_bufs.buf1), stdin)){
		exit(-1);
	}
    // Do you like TBONE steak?
    jump_around(input_bufs.buf1, 
                input_bufs.buf1 + 1024,
                input_bufs.buf2, 
                sizeof(input_bufs.buf2));

    printf("Jump! Jump! Jump! Jump!\n");
}

void Warning::get_str(){
    std::cout << "> " << std::flush;
    
    fgets(this->buf, 0x115, stdin);
    return;
}

bool Warning::check(uint8_t lvl){
    switch(lvl){
        case 1:
            std::cout << "Case 1: " << 0x1000 << std::endl;
            if((a+b-c) == 0x1000){
                std::cout << "Nice." << std::endl;
                return true;
            }
            return false;
        case 2:
            std::cout << "Case 2: " << -256 << std::endl;
            if(a == -256){
                std::cout << "Nicee." << std::endl;
                return true;
            }
            return false;
        default:
            return false;
    }

    return false;
}

// I hate c++
Warning::Warning(): 
    c( 10 ),
    b( c+20 ),
    a( b-5 ){
}

Warning::~Warning(){}

void timeout_func(int signo){
    LOG_ERR("Oops. You ran out of time. Goodbye!\n");
    exit(-1);
}

int main(){
    // Shamelessly stolen from pedant
    int timeout = 120;
    char *timeout_str = getenv("TIMEOUT");
    if (timeout_str) {
        timeout = atoi(timeout_str);
    }
    signal(SIGALRM, timeout_func);
    alarm(timeout+2);
    signal(SIGPIPE, SIG_IGN);

    std::cout << "> " << std::flush;

    // I really hate C++
    {
        std::string s;
        std::cin >> s;
    }

    Warning* w0 = new Warning();

    if(!w0->check(1)){
        goodbye();
    }

    Warning* w1 = new Warning();

    flushcin();
    w0->get_str();

    if(!w1->check(2)){
        goodbye();
    }

    // I'll just give you the leak. Screw it
    printf("get_flag: %p\n", get_flag);

    w1->get_input();

    return 0;
}