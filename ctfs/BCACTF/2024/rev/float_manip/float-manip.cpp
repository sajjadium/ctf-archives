#include <iostream>
#include <fstream>
#include <vector>
#include <cstring>
void writeBit(char *data, int bitIndex, bool bit) {
    data[bitIndex / 8] |= (bit << (7 - (bitIndex % 8)));
}
int main() {
    std::ifstream file("flag.txt");
    if (!file.is_open()) {
        std::cerr << "Error opening file flag.txt" << std::endl;
        return 1;
    }

    std::vector<float> vals;
    char c;
    while (file.get(c)) {
        vals.push_back(static_cast<float>(c));
    }

    file.close();

    size_t fSize = vals.size();
    size_t bSize = fSize * 4;
    char* bytes = new char[bSize];

    for (size_t i = 0; i < fSize; ++i) {
        unsigned char* p = reinterpret_cast<unsigned char*>(&vals[i]);
        bytes[i * 4 + 0] = p[3];
        bytes[i * 4 + 1] = p[2];
        bytes[i * 4 + 2] = p[1];
        bytes[i * 4 + 3] = p[0];
    }

    char* encoded = new char[bSize]();
    for (int i = 0; i < fSize; i++) {
        int startingByte = 4 * i;
        writeBit(encoded, i, (bytes[startingByte] & 0x80) != 0); // get first bit
        int base = fSize + i * 8;
        char byte = bytes[startingByte];
        for (int j = 0; j < 7; j++) {
            writeBit(encoded, base + j, (byte & (0x40 >> j)) != 0);
        }
        byte = bytes[startingByte + 1];
        writeBit(encoded, base + 7, (byte & 0x80) != 0);
        base = 9 * fSize + i * 23;
        for (int j = 0; j < 7; j++) {
            writeBit(encoded, base + j, (byte & (0x40 >> j)) != 0);
        }
        base += 7;
        byte = bytes[startingByte + 2];
        for (int j = 0; j < 8; j++) {
            writeBit(encoded, base + j, (byte & (0x80 >> j)) != 0);
        }
        base += 8;
        byte = bytes[startingByte + 3];
        for (int j = 0; j < 8; j++) {
            writeBit(encoded, base + j, (byte & (0x80 >> j)) != 0);
        }
    }

    std::ofstream outFile("encoded.bin", std::ios::binary);
    if (!outFile.is_open()) {
        std::cerr << "Error opening file encoded.bin for writing" << std::endl;
        delete[] bytes;
        delete[] encoded;
        return 1;
    }

    outFile.write(encoded, bSize);
    outFile.close();

    delete[] bytes;
    delete[] encoded;

    return 0;
}
