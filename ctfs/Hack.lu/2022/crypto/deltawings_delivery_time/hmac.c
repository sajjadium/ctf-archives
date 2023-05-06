#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/random.h>
#include <time.h>
// /algorithms is not challenge relevant
#include "algorithms/Blake2b/blake2b.h"
#include "algorithms/sha256/sha256.h"

typedef unsigned char byte;

#define NANOS 1000000000LL
#define MAX_INPUTSIZE 1024
#define MAX_BYTEVOLUME 250
struct timespec GLOBAL_TIMESPEC;

#define FULLNS() GLOBAL_TIMESPEC.tv_nsec+GLOBAL_TIMESPEC.tv_sec*NANOS
#define SETEPOCH() clock_gettime(CLOCK_MONOTONIC,&GLOBAL_TIMESPEC);EPOCH = FULLNS()
#define ROOTLOG(n,...) clock_gettime(CLOCK_MONOTONIC,&GLOBAL_TIMESPEC);printf("[%lld] [%s] ",FULLNS()-EPOCH,n);printf(__VA_ARGS__);printf("\n")
#define LOG(...) ROOTLOG("LOG",__VA_ARGS__)
#define ERROR(...) ROOTLOG("ERROR",__VA_ARGS__);exit(1)

#define FREEBUF(n) free(n->data);free(n)

struct timespec local_ts;

long long int EPOCH;

int bytes_processed = 0;

struct Bytearray{
    int sz;
    byte* data;
};

void hash1(struct Bytearray *input){
    SHA256_CTX ctx;
    byte outbuf[32];

    sha256_init(&ctx);
    sha256_update(&ctx,input->data,input->sz);
    sha256_final(&ctx,outbuf);
    memcpy(input->data,outbuf,16);
}

void hash2(struct Bytearray *input){
    for (int i=0;i<50;i++){
        blake2b(input->data,16,input->data,input->sz,0,0);
    }
}

int countbits(byte b){
    int count = 0;
    while (b){
        count += b & 1;
        b >>= 1;
    }
    return count;
}

char* to_hexstring(const struct Bytearray *ba){
    char* outstr = malloc(ba->sz*2);

    for (int i=0;i<ba->sz;i++){
        char hexrep[3];

        snprintf(hexrep,3,"%02x",ba->data[i]);
        
        outstr[i*2] = hexrep[0];
        outstr[i*2+1] = hexrep[1];

    }
    return outstr;
}

struct Bytearray* from_hexstring(char* hstring){
    int num_bytes = strlen(hstring)/2;

    struct Bytearray* ret = malloc(sizeof(struct Bytearray));
    ret->sz = num_bytes;
    ret->data = malloc(num_bytes);

    for (int i=0;i<num_bytes;i++){ 
        unsigned char byt;
        int chars_processed;
        int error = 0;

        if (sscanf(&hstring[i*2],"%2hhx%n",&byt,&chars_processed) != 1){
            error = 1;
        }else if (chars_processed != 2){
            error = 1;
        }
        if (error){
            ERROR("Could not parse hex string");
        }
        ret->data[i] = byt;
    }
    return ret;
}

struct Bytearray* get_userdefined_buffer(){
    char buf[MAX_INPUTSIZE+1];
    printf("Enter a hex string with maximum length of %d chars: ",MAX_INPUTSIZE);
    fgets(buf,MAX_INPUTSIZE+1,stdin);

    return from_hexstring(buf);
}

void fill_random(struct Bytearray *container){
    getrandom(container->data,container->sz,0); 
}

void pad(struct Bytearray *container){

    if (container->sz % 16 == 0){
        return;
    }
    
    int toadd = 16-(container->sz % 16);
    int newsize = container->sz+toadd;

    struct Bytearray* tmpbytes = malloc(sizeof(struct Bytearray));
    tmpbytes->sz = newsize;
    tmpbytes->data = malloc(newsize);

    memcpy(tmpbytes->data,container->data,container->sz);

    unsigned char s = 0;
    for (int i=0;i<container->sz;i++){
        s += container->data[i];
    }
    
    memset(tmpbytes->data+container->sz,s^toadd,toadd);

    hash1(tmpbytes);
    hash2(tmpbytes);

    byte* outbytes = malloc(newsize);

    memcpy(outbytes,container->data,container->sz);
    memcpy(outbytes+container->sz,tmpbytes->data,toadd);
    
    FREEBUF(tmpbytes);
    free(container->data);

    container->data = outbytes;
    container->sz = newsize;
}

void hmac(byte* key, struct Bytearray* plain){
    bytes_processed += plain->sz;
    struct Bytearray *state = from_hexstring("0000000000000000ffffffffffffffff");

    int original_size = plain->sz;

    pad(plain);

    LOG("padded plaintext with %d bytes. Plaintext is now %s",plain->sz-original_size,to_hexstring(plain));

    int num_blocks = plain->sz / 16;

    for (int blocknum=0;blocknum<num_blocks;blocknum++){
        LOG("processing block %d",blocknum);

        for (int i=0;i<16;i++){
            int offset = blocknum*16+i;

            byte kbyte = key[i];
            byte pbyte = plain->data[offset];
            byte res = kbyte^pbyte;

            state->data[i] = state->data[i] ^ key[i];

            if (countbits(res) >= 4){
                hash1(state);
                
            }else{
                hash2(state);
            }
            LOG("processed bytes at position %d",offset);
        }

    }
    LOG("hmac result: %s",to_hexstring(state));

}

int menuchoice(){
    int n = -1;
    char line[256];

    printf("choose an action to take\n");
    printf("1) debug hmac implementation\n");
    printf("2) check sessionkey\n");
    printf("3) exit\n> ");
        
    fgets(line,256,stdin);
    sscanf(line,"%d", &n);

    return n;

}

int main(int argc, char *argv[]){
    char* flag = "flag{fakeflag}";
    SETEPOCH();

    struct Bytearray* sesskey = from_hexstring("00000000000000000000000000000000");
    fill_random(sesskey);

    //LOG("generated a random session key %s",to_hexstring(sesskey));
    printf(
        "===============================================================\n"
        "Welcome to the Deltawings customer debug interface!\n"
        "Break our *blazingly fast* hmac algorithm to win a free food coupon!\n"
        "(you can convince yourself how *blazignly fast* our implementation is by looking at the timestamps)\n"
        );

    while (1){
        printf("===============================================================\n");
        printf("you have %d bytes left to send to this instance\n",MAX_BYTEVOLUME-bytes_processed);
        int c = menuchoice();
        switch (c)
        {
        case 1:

            if (bytes_processed == MAX_BYTEVOLUME){
                printf("error: bytevolume depleted\n");
                break;
            }

            printf("please enter the plaintext\n");

            struct Bytearray* plain;
            while (1){
                plain = get_userdefined_buffer();
                if (MAX_BYTEVOLUME-bytes_processed - plain->sz < 0){
                    printf("error: not enough byte volume left (%d bytes left, %d received)\n",MAX_BYTEVOLUME-bytes_processed,plain->sz);
                    FREEBUF(plain);
                    continue;
                }
                break;
            }
            
            hmac(sesskey->data,plain);
            break;
        
        case 2:
            printf("please enter the session key\n");
            struct Bytearray* check_key = get_userdefined_buffer();
            
            if (memcmp(check_key->data,sesskey->data,16) == 0){
                printf("Correct! Enjoy your coupon :) %s\n",flag);
                goto instance_exit;

            }else{
                int correct_bits = 0;
                for (int i=0;i<16;i++){
                    byte kbyte = sesskey->data[i];
                    byte pbyte = check_key->data[i];
                    correct_bits += 8-countbits(kbyte^pbyte);
                }
                printf("%f %% of bits were correct\n",(correct_bits/(float)128)*100);
                goto instance_exit;
            }

        case 3:
            goto instance_exit;

        default:
            printf("invalid option\n");
        }
    }

    instance_exit:
        LOG("instance terminated after processing %d bytes",bytes_processed);

    return 0;
}
