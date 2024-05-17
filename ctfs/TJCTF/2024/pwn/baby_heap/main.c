#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <malloc.h>
#include <assert.h>


int main()
{

        uint8_t* updater = (uint8_t*) malloc(0x20);
        int size = 0x78;
        uint8_t* a = (uint8_t*) malloc(size);
        uint8_t* b = (uint8_t*) malloc(0x10);
        uint8_t* reader = (uint8_t*) malloc(size);

        FILE* f = fopen("flag.txt","r");
        fgets(&reader[1], 28, f);

        printf("a, b, reader = %p, %p, %p\n", a, b, reader);


        size_t* b_size_ptr = (size_t*) (b - 8);

        uint8_t attack_size;

        fflush(stdout);

        int temp;
        scanf("%i", &temp);
        attack_size = temp;

        //1 byte attack
        a[size] = attack_size;

        printf("b size val = %#lx\n", *b_size_ptr);

        free(b);

        //create dangling chunk

        int new_size;
        fflush(stdout);
        scanf("%i", &new_size);

        printf("allocing %i bytes\n", new_size);

        uint8_t* chunk = (uint8_t*) malloc(new_size);

        printf("chunk = %p, blocker + 0x10 == c: %i\n", chunk, chunk + 0x20 == reader);
        printf("chunk %p\n", chunk); 

        assert((chunk + 0x20 == reader));

        assert(new_size > 0x20 + 0x20);

        printf("%s\n", &chunk[0x21]);

        fflush(stdout);
        free(a);
        free(chunk);
        free(reader);

        return 0;
}