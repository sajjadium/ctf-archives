#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <sys/random.h>
// sudo apt install libsecp256k1-dev
#include <secp256k1.h>
#include <secp256k1_ecdh.h>

const char flag[32] = "p4{TODO - put real flag here :)}";
secp256k1_context* ctx;
secp256k1_pubkey pk;
uint8_t sk[32];

void gen_seckey(uint8_t * sk) {
    for (int i = 0; i < 16; i++) {
        int r = rand();
        *sk++ = (r >> 8) & 0xff;
        *sk++ = (r >> 0) & 0xff;
    }
}

void bad_input(void) {
    puts("Very funny. Come back when you decide you want to cooperate.");
    exit(0);
}

void printhex(uint8_t * buf, size_t size) {
    for (size_t i = 0; i < size; i++) {
        printf("%02x", buf[i]);
    }
    printf("\n");
}

void readhex(uint8_t * buf, size_t size) {
    for (size_t i = 0; i < size; i++) {
        if (scanf("%02hhx", buf + i) != 1) bad_input();
    }
}

const char * random_name(void) {
    static const char *names[] = {
        "James", "Robert", "John", "Michael", "William", "David", "Richard",
        "Joseph", "Thomas", "Charles", "Christopher", "Daniel", "Matthew",
        "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
        "Kenneth", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy",
        "Jason", "Jeffrey", "Ryan", "Jacob", "Gary",
    };
    const int count = sizeof(names) / sizeof(*names);
    return names[rand() % count];
}

struct guy {
    const char * name;
    secp256k1_pubkey * pk;
};

void make_up_a_guy(struct guy * guy) {
    guy->name = random_name();
    guy->pk = NULL;
}

void ensure_pk(struct guy * guy) {
    if (!guy->pk) {
        uint8_t sk[32];
        gen_seckey(sk);
        guy->pk = malloc(sizeof(secp256k1_pubkey));
        if (!secp256k1_ec_pubkey_create(ctx, guy->pk, sk)) abort();
    }
}

void talk(void) {
    uint8_t buf[33];
    size_t size = 33;
    puts("Okay, hold on. THEY might be listening. Let's encrypt!");
    printf("Here's my public key: ");
    secp256k1_ec_pubkey_serialize(ctx, buf, &size, &pk, SECP256K1_EC_COMPRESSED);
    printhex(buf, size);
    printf("What's yours? ");
    readhex(buf, 33);

    secp256k1_pubkey their_pk;
    if (secp256k1_ec_pubkey_parse(ctx, &their_pk, buf, 33) != 1) bad_input();

    uint8_t shared_secret[32];

    if (secp256k1_ecdh(ctx, shared_secret, &their_pk, sk, secp256k1_ecdh_hash_function_sha256, NULL) != 1) abort();

    printf("Okay, if everything went well, we should both arrive at ");
    printhex(shared_secret, 32);
    puts("Wait, shit! I shouldn't have said that out loud, should I? Do you want to try again?");
}

void get_flag(void) {
    puts("Hmm, are you allowed to have one, though?");

    char c;
    struct guy guy;

    do {
        make_up_a_guy(&guy);
        printf("Do you know %s? He's a very good friend of mine and will surely pass on the flag to you if you're authorized... [y/n] ", guy.name);
        if (scanf(" %c", &c) != 1) bad_input();
        c = tolower(c);
    } while(c != 'y');

    ensure_pk(&guy);
    uint8_t ciphertext[32];

    if (secp256k1_ecdh(ctx, ciphertext, guy.pk, sk, secp256k1_ecdh_hash_function_sha256, NULL) != 1) abort();

    for (int i = 0; i < 32; i++) {
        ciphertext[i] ^= flag[i];
    }

    puts("Splendid! Give him this message and you'll have your flag in no time:");
    puts("============================================================================");
    printf("Dear %s,\n\n", guy.name);
    puts("This fine gentleman has kindly asked me to share my knowledge of the flag.");
    puts("I'm not sure, though, if I'm allowed to give it to him, so I encrypted it");
    puts("with your public key. That way, you can decide:");
    printhex(ciphertext, 32);
    puts("To be clear, it's the key you gave me last time we met,");

    uint8_t buf[33];
    size_t size = 33;
    secp256k1_ec_pubkey_serialize(ctx, buf, &size, guy.pk, SECP256K1_EC_COMPRESSED);
    printhex(buf, size);

    puts("\nYours truly,");
    puts(random_name());
    puts("============================================================================");
    puts("\nWhat would you like to do?");
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    char entropy[256 + 4];
    if (getrandom(entropy, sizeof entropy, 0) < sizeof entropy) {
        abort();
    }

    if (!initstate(*(unsigned int*)(entropy + 256), entropy, 256)) {
        abort();
    }

    ctx = secp256k1_context_create(SECP256K1_CONTEXT_SIGN);
    gen_seckey(sk);
    if (!secp256k1_ec_pubkey_create(ctx, &pk, sk)) abort();

    puts("What would you like to do?");
    while (1) {
        puts("1) Let's talk");
        puts("2) I want a flag");
        int choice;
        if (scanf("%d", &choice) != 1) bad_input();
        switch(choice) {
        case 1: talk(); break;
        case 2: get_flag(); break;
        default: bad_input(); break;
        }
    }

}
