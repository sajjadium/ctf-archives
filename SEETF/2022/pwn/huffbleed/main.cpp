// g++ main.cpp huffman.cpp -o huffbleed
#include <fstream>
#include <iostream>

// two functions from huffman.cpp
size_t encode(const void* p_inbuf, size_t inlen, void* p_outbuf);
size_t decode(const void* p_inbuf, void* p_outbuf);

void init(bool printflag) {
    static char flag[32];
    std::ifstream{"flag.txt"}.getline(flag, sizeof flag);
    if (printflag)
        printf("The flag is %s\n", flag);
}


constexpr unsigned MAX_SIZE = 4096;
char rawBuffer[MAX_SIZE];
char cmpBuffer[MAX_SIZE+2];

void hexdump(const char* message, void* buffer, int length) {
    printf("%s%i bytes:\n", message, length);
    for (int i = 0; i < length; i++)
        printf(" %02x", ((uint8_t*)buffer)[i]);
    printf("\n\n");
}

int main() {
    init(0);
    printf("Please feed me some data (up to %u bytes).\n", MAX_SIZE);

    // get input of up to MAX_SIZE bytes
    std::cin.read(rawBuffer, MAX_SIZE);
    int rawSize = std::cin.gcount();
    hexdump("Successfully read in ", rawBuffer, rawSize);

    // compress input to compressed buffer
    int cmpSize = encode(rawBuffer, rawSize, cmpBuffer);
    hexdump("Compressed to ", cmpBuffer, cmpSize);

    // decompress from compressed buffer
    int decSize = decode(cmpBuffer, rawBuffer);
    hexdump("Decompressed back to ", rawBuffer, decSize);
}
