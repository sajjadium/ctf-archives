#include <stdio.h>
#include <string.h>

// Convert each byte of the flag to hex and print it
void print_flag_hex(unsigned char *flag, int length, int step) {
    printf("Flag after reverse step %d: ", step);
    for (int i = 0; i < length; i++) {
        printf("%02x", flag[i]);  // Print each byte in hexadecimal
    }
    printf("\n");
}

// Reverse the modification of the flag bytes based on the seed
void reverse_modify_flag(unsigned char *flag, unsigned int seed) {
    int length = strlen((char *)flag);

    for (int i = 0; i < length; i++) {
        flag[i] = (flag[i] - (seed % 10)) % 256;  // Reverse each byte modification
        seed = seed / 10;
        if (seed == 0) {
            seed = 88974713;  // Reset seed if it runs out
        }
    }
}

int main() {
    unsigned char encoded_flag[] = { 0x8e, 0x79, 0xa9, 0x9c, 0xac, 0xd5, 0xc5, 0xc7, 0x91, 0x7a, 0xa5, 0x8a, 0xb8, 0x8d, 0xc6, 0x81, 0x55, 0x83, 0xa5, 0x59, 0x7b, 0xb9, 0x87, 0xb8, 0x51, 0x69, 0x7b, 0x58, 0xbb, 0x8b, 0xcd};

    unsigned int seed = 88974713;
    int length = sizeof(encoded_flag);

    printf("Encoded flag: ");
    print_flag_hex(encoded_flag, length, 0);

    // Reverse the modifications 10 times (finish this!)
    printf("Decode function not added yet!");

    printf("Decoded flag (plaintext in hex): ");
    print_flag_hex(encoded_flag, length, 0);  // Print final decoded flag in hex

    return 0;
}
