// gcc -Wl,-z,relro,-z,now chall.c -o chall

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define buffer_size 0x100
#define num_files 3

char prev[buffer_size] = {0};
char buf[buffer_size] = {0};
char backup[buffer_size] = {0};
char *buffers[num_files] = {buf, prev, backup};

FILE *fp;

int min(int a, int b) {
    return (a > b) ? b : a;
}

int main()
{
    setbuf(stdout, 0);

    puts("CS Intro: Constant, modify in place, modify not in place.");
    puts("First, you will modify a file's contents not in place.");
    puts("Next, you will modify a file's contents in place.");
    puts("Finally, I will demonstrate what constant means.");

    int i;
    char filename[10];
    for (i = 0; i < num_files; i++)
    {
        snprintf(filename, 10, "key%d.txt", i);
        fp = fopen(filename, "r");
        fread(buffers[i], 1, buffer_size, fp);
    }

    puts("\nDemonstration 1:");
    puts("Modify not in place: First allocate more memory");

    int chunk_size;
    char *chunk_ptr;
    puts("What size to allocate?");
    scanf("%d", &chunk_size);
    chunk_ptr = calloc(1, chunk_size);

    puts("Which file to read? (1-3)");
    scanf("%d", &i);
    i -= 1;
    memcpy(chunk_ptr, buffers[i], min(buffer_size, chunk_size));

    // store fp for the constant demonstration at the end
    int j = (i + 1) % num_files;
    snprintf(filename, 10, "key%d.txt", j);
    fp = fopen(filename, "r");
    // --------------------------------------------------

    printf("Allocated you a chunk @ %p\n", chunk_ptr);
    printf("Content: ");

    ssize_t bytes_read = read(0, chunk_ptr, chunk_size);
    if (bytes_read > 0x91)
    {
        puts("Sorry, you're asking too much.");
        exit(0);
    }
    else
    {
        chunk_ptr[bytes_read - 1] = 0;
    }

    puts("\nDemonstration 2:");
    printf("Modify in place:\nContent: ");
    i = (i - 1) % num_files;
    scanf("%s", buffers[i]);

    puts("\nDemonstration 3:");
    puts("Constant!");
    fread(buffers[j], 1, buffer_size, fp);  // fp was previously stored
}