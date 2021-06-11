#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define ROUNDS 100
#define CHUNK_SIZE 32
#define CONTEXT_MAGIC 0x6861736822686f6dULL

static char* key_bytes;

typedef struct hash_rpc_context_s {
    unsigned long magic;
    unsigned rounds_left;
    struct hash_rpc_context_s *next;
    char data_to_hash[CHUNK_SIZE];
} hash_rpc_context;

hash_rpc_context* first_context = NULL;

void send_request(const hash_rpc_context* request_context){
    /* XXX: the request's pointer is used as the request ID
     * maybe this should be an UUID? */
    write(1, &request_context, sizeof(request_context));
    write(1, request_context->data_to_hash, CHUNK_SIZE);
}

void hash_together_the_first_two(){
    for (unsigned i=0; i<CHUNK_SIZE; ++i){
        first_context->next->data_to_hash[i] ^= first_context->data_to_hash[i];
    }
    /* TODO: free the first context. It crashes for some reason sometimes though */
    first_context = first_context->next;
    first_context->rounds_left = ROUNDS;
    send_request(first_context);
}

void process_response(hash_rpc_context* request_context, char response_data[CHUNK_SIZE]){
    --request_context->rounds_left;
    if(request_context->rounds_left){
        memcpy(request_context->data_to_hash, response_data, CHUNK_SIZE);
        send_request(request_context);
    } else {
        if (
            first_context->next &&
            first_context->rounds_left == 0 &&
            first_context->next->rounds_left == 0
        ){
            hash_together_the_first_two();
        }
    }
}


void receive_response(){
    hash_rpc_context* request_context;
    char response_data[CHUNK_SIZE];
    if (read(0, &request_context, sizeof(request_context)) != sizeof(request_context)){
        exit(2);
    }
    if (read(0, response_data, CHUNK_SIZE) != CHUNK_SIZE) {
        exit(3);
    }
    if (request_context->magic != CONTEXT_MAGIC) {
        exit(4);
    }
    process_response(request_context, response_data);
}

void read_input(char* filename){
    int fd = open(filename, O_RDONLY);
    char record[CHUNK_SIZE];
    hash_rpc_context * previous=NULL;
    while(read(fd,record,CHUNK_SIZE)==CHUNK_SIZE){
        hash_rpc_context *context = calloc(1, sizeof(hash_rpc_context));
        context->magic = CONTEXT_MAGIC;
        context->next = previous;
        context->rounds_left = ROUNDS;
        for (unsigned i=0; i<CHUNK_SIZE; ++i)
            context->data_to_hash[i] = record[i] ^ key_bytes[i];
        previous = context;
    }
    first_context = previous;
    close(fd);
}

void do_the_work(){
    for (hash_rpc_context* context = first_context; context; context = context->next){
        send_request(context);
    }
    while(first_context->next) {
        receive_response();
    }
}

void write_output(char* filename){
    int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    write(fd, first_context->data_to_hash, CHUNK_SIZE);
    close(fd);
}

int main(int argc, char** argv){
    if (argc != 4) {
        printf(
            "Usage: hashing_at_home_server key_bytes records_file output_file\n"
            "\n"
            "This software reads a file in chunks, hashes these chunks many times\n"
            "and then combine the hashes and hash them again for extra secureness.\n"
            "Unfortunately, this is resource-intensive, so it uses a networked worker\n"
            "to do the hash rounds in parallel.\n"
            "\n"
            "(TEST VERSION USING STDIO. use xinetd or something to make it networked)\n");
        return 1;
    }
    key_bytes = calloc(1, 64);
    strncpy(key_bytes, argv[1], 63);
    read_input(argv[2]);
    do_the_work();
    write_output(argv[3]);
    return 0;
}
