#include <stdio.h>
#include <string.h>
#include <stdint.h>

/*
 * SPACE PIRATES CTF CHALLENGE
 * ===========================
 * Theme: You've intercepted an encrypted transmission from space pirates!
 * Decode their secret coordinates to find their hidden treasure.
 * 
 * CHALLENGE MECHANICS:
 * The input undergoes a series of reversible operations:
 * 1. XOR with a rotating key (reversible by XORing again)
 * 2. Byte swap pairs (reversible by swapping again)
 * 3. Addition modulo 256 (reversible by subtraction)
 * 4. Final XOR with position (reversible by XORing again)
 * 
 */

#define FLAG_LEN 30
const uint8_t TARGET[FLAG_LEN] = {
    0x5A,0x3D,0x5B,0x9C,0x98,0x73,0xAE,0x32,0x25,0x47,0x48,0x51,0x6C,0x71,0x3A,0x62,0xB8,0x7B,0x63,0x57,0x25,0x89,0x58,0xBF,0x78,0x34,0x98,0x71,0x68,0x59
};

// The pirate's rotating XOR key
const uint8_t XOR_KEY[5] = {0x42, 0x73, 0x21, 0x69, 0x37};

// The magic addition constant
const uint8_t MAGIC_ADD = 0x2A;
// PCTF{0x_M4rks_tH3_sp0t_M4t3y}
void print_flag(char *input) {
    printf("\n");
    printf("    *     .    *       .   *    .\n");
    printf("  .   *        ___---___      *    .\n");
    printf("    *    .   .'         '.   *   .\n");
    printf("  .  *   *   /   0     0   \\    *\n");
    printf("    *   .   |               |  .    *\n");
    printf("  .    *    |   \\  ___  /   |     .\n");
    printf("    *    .  |    \\_____/    |  *\n");
    printf("  *   .      \\             /    .    *\n");
    printf("    .    *    '._________.'   *   .\n");
    printf("  *    .   *    TREASURE!   .   *\n");
    printf("\n");
    printf("🏴‍☠️  DECRYPTION SUCCESSFUL! 🏴‍☠️\n");
    printf("\n");
    printf("Flag: %s\n",input);
    printf("\n");
}

int main(int argc, char *argv[]) {
    printf("===========================================\n");
    printf("  SPACE PIRATES TRANSMISSION DECODER v1.0\n");
    printf("===========================================\n");
    printf("\n");
    printf("Mission: Decode the pirate coordinates!\n");
    printf("\n");

    // Check command line argument
    if (argc != 2) {
        printf("  Usage: %s <encrypted_coordinates>\n", argv[0]);
        printf("   Example: %s GALAXY_SECTOR_ALPHA_1234567\n", argv[0]);
        return 1;
    }

    char *input = argv[1];
    size_t len = strlen(input);

    // Validate length
    if (len != FLAG_LEN) {
        printf("  Invalid transmission length!\n");
        return 1;
    }

    // Create a working buffer
    uint8_t buffer[FLAG_LEN];
    memcpy(buffer, input, FLAG_LEN);

    printf("Processing transmission...\n\n");

    // OPERATION 1: XOR with rotating key
    // Each byte is XORed with one of 5 key bytes (cycling through them)
    // This obscures the plaintext with a repeating pattern
    printf("[1/4] Applying quantum entanglement cipher...\n");
    for (int i = 0; i < FLAG_LEN; i++) {
        buffer[i] ^= XOR_KEY[i % 5];
    }

    // OPERATION 2: Swap adjacent byte pairs
    // Bytes at positions (0,1), (2,3), (4,5), etc. are swapped
    // This scrambles the byte order in a predictable way
    printf("[2/4] Applying spatial transposition...\n");
    for (int i = 0; i < FLAG_LEN; i += 2) {
        uint8_t temp = buffer[i];
        buffer[i] = buffer[i + 1];
        buffer[i + 1] = temp;
    }

    // OPERATION 3: Add magic constant (mod 256)
    // Each byte has MAGIC_ADD added to it (wrapping at 256)
    // This shifts all values by a constant amount
    printf("[3/4] Applying gravitational shift...\n");
    for (int i = 0; i < FLAG_LEN; i++) {
        buffer[i] = (buffer[i] + MAGIC_ADD) % 256;
    }

    // OPERATION 4: XOR each byte with its position
    // Byte at position i is XORed with i
    // This makes each position's transformation unique
    printf("[4/4] Applying coordinate calibration...\n");
    for (int i = 0; i < FLAG_LEN; i++) {
        buffer[i] ^= i;
    }

    printf("\n");
    printf("Verifying coordinates against star charts...\n");
    
    // Check if the result matches our target
    if (memcmp(buffer, TARGET, FLAG_LEN) == 0) {
        print_flag(input);
        return 0;
    } else {
        printf("\n");
        printf("  DECRYPTION FAILED!\n");
        printf("\n");
        printf("The coordinates don't match known pirate sectors.\n");
        printf("Hint: Pirates love to name their sectors after galaxies...\n");
        printf("\n");
        
        // Debug output (helpful for solving)
        // printf("Your result (hex): ");
        // for (int i = 0; i < FLAG_LEN; i++) {
        //     printf("0x%02X,", buffer[i]);
        // }
        printf("\n");
        
        return 1;
    }
}