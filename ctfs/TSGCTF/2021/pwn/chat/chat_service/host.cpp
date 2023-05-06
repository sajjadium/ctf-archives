#include "service.hpp"

void setup() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(int argc, char *argv[]) {
    setup();
    auto client =  make_unique<Client>();

    main_loop(move(client));
    return 0;
}
