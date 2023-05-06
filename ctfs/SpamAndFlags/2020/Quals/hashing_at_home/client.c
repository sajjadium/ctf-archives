#include "sha256.h"
#include <unistd.h>
#include <stdint.h>
#define CHUNK_SIZE 32

void sha256_hash(char* input, char* output){
    SHA256_CTX ctx;
    sha256_init(&ctx);
    sha256_update(&ctx, (BYTE*)input, CHUNK_SIZE);
    sha256_final(&ctx, (BYTE*)output);
}

int main(int argc, char** argv){
    while (1) {
        uint64_t request_id;
        char data[CHUNK_SIZE];
        if (read(0, &request_id, sizeof(request_id)) != sizeof(request_id)){
            return 0;
        }
        if (read(0, &data, CHUNK_SIZE) != CHUNK_SIZE){
            return 0;
        }
        sha256_hash(data, data);
        write(1,  &request_id, sizeof(request_id));
        write(1, &data, CHUNK_SIZE);
    }
}
