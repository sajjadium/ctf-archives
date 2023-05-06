#include <stdio.h>
int decompress(const char *fname);
int main(int argc, char** argv) {
    if (argc != 2) return -1;
    printf("Decompressing %s\n", argv[1]);
    decompress(argv[1]);
    return -1;
}
