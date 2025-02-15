#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void encrypt(const char *text, const char *mapping[], char *encrypted_text) {
    size_t len = strlen(text);
    for (size_t i = 0; i < len; i++) {
        char char_to_encrypt = text[i];
        if (char_to_encrypt >= 'a' && char_to_encrypt <= 'z') {
            strcat(encrypted_text, mapping[char_to_encrypt - 'a']);
        } else if (char_to_encrypt >= 'A' && char_to_encrypt <= 'Z') {
            strcat(encrypted_text, mapping[char_to_encrypt - 'A' + 26]);
        } else {
            strncat(encrypted_text, &char_to_encrypt, 1);
        }
    }
}

int main() {
    char text[256];
    printf("Enter the text to be encrypted: ");
    fgets(text, sizeof(text), stdin);
    text[strcspn(text, "\n")] = 0;

    const char *mapping[52] = {
        "@!", "#$", "%^", "&*", "()", "_+", "-=", "{}", "[]", ":;", "\"\"", "<>", ",.", "/?", "|\\", "`~",
        "12", "34", "56", "78", "90", "AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST", "UV",
        "WX", "YZ", "ab", "cd", "ef", "gh", "ij", "kl", "mn", "op", "qr", "st", "uv", "wx", "yz", "01",
        "23", "45", "67", "89"
    };

    char encrypted_text[1024] = "";
    encrypt(text, mapping, encrypted_text);

    FILE *file = fopen("enc.txt", "w");
    if (file != NULL) {
        fputs(encrypted_text, file);
        fclose(file);
    } else {
        perror("Error opening file");
    }

    return 0;
}

