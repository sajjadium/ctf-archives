#include <iostream>
#include <cinttypes>
#include <string>
#include <filesystem>
#include <fstream>
#include <sys/stat.h>
#include <vector>
#include <cstring>
using namespace std;
using namespace std::filesystem;

typedef uint8_t Byte;

void make_key(Byte *S, const std::string &key)
{
	for (int i = 0; i < 255; i++)
		S[i] = i;

	Byte j = 0;
	for (int i = 0; i < 255; i++)
	{
		j = (j ^ S[i] ^ key[i % key.length()]) % 256;
		std::swap(S[i], S[j]);
	}
}

Byte S_box[256] = {24, 250, 101, 19, 98, 246, 141, 58, 129, 74, 227, 160, 55, 167, 62, 57, 237, 156, 32, 46, 90, 67, 22, 3, 149, 212, 36, 210, 27, 99, 168, 109, 125, 52, 173, 184, 214, 86, 112, 70, 5, 252, 6, 170, 30, 251, 103, 43, 244, 213, 211, 198, 16, 242, 65, 118, 68, 233, 148, 18, 61, 17, 48, 80, 187, 206, 72, 171, 234, 140, 116, 35, 107, 130, 113, 199, 51, 114, 232, 134, 215, 197, 31, 150, 247, 79, 26, 110, 142, 29, 9, 117, 248, 186, 105, 120, 15, 179, 207, 128, 10, 254, 83, 222, 178, 123, 100, 39, 228, 84, 93, 97, 60, 94, 180, 146, 185, 38, 203, 235, 249, 89, 226, 1, 106, 12, 216, 221, 8, 45, 13, 2, 14, 75, 49, 33, 127, 163, 111, 85, 255, 253, 166, 151, 40, 23, 194, 34, 139, 95, 145, 193, 159, 133, 69, 245, 196, 102, 91, 11, 157, 96, 47, 152, 154, 59, 181, 28, 126, 200, 158, 88, 224, 231, 41, 190, 240, 191, 188, 143, 164, 189, 217, 54, 66, 241, 209, 104, 78, 87, 82, 230, 182, 220, 53, 147, 21, 136, 76, 0, 115, 169, 71, 44, 223, 175, 92, 25, 177, 64, 201, 77, 138, 144, 204, 229, 81, 20, 183, 205, 124, 243, 4, 172, 174, 108, 132, 176, 135, 161, 162, 7, 236, 195, 238, 56, 42, 131, 218, 155, 121, 153, 239, 50, 219, 225, 37, 202, 63, 137, 192, 208, 119, 122, 165, 73};

void enc(Byte *S, Byte *out, int amount)
{
	Byte i = 0;
	Byte j = 0;
	int ctr = 0;
	while (ctr < amount)
	{
		i = (i * j) % 256;
		j = (i + S[j]) % 256;
		// std::swap(S[i],S[j]);
		Byte K = (S[i] & S[j]);
		out[ctr] ^= S_box[K];
		ctr++;
	}
}

Byte key[256];
int main()
{

	std::string path = current_path();

	std::vector<std::string> files;
	for (const auto &file : directory_iterator(path))
		files.push_back(std::string(file.path()));

	for (const auto &file : files)
	{
		std::cout << file << "\n";
		struct stat results;
		std::ifstream in(file);
		std::ofstream out(file + ".enc", std::ofstream::binary);
		if (stat(file.c_str(), &results) == 0)
		{
			uint8_t *buffer = new uint8_t[results.st_size];
			in.read((char *)buffer, results.st_size);

			make_key(key, std::to_string(rand()));
			enc(key, buffer, results.st_size);

			out.write((char *)buffer, results.st_size);
			delete[] buffer;
		}
		in.close();
		out.close();
	}

	return 0;
}
