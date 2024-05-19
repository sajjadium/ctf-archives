#include "common.hpp"

int main()
{
	std::cout << "Hello world!\n";

	readflag();

	auto st = std::chrono::high_resolution_clock::now();

	std::vector<std::pair<Word, Word>> pairs;

	for (int i = 0; i < 18; i++)
	{
		Word p = getRand();
		Word c = oracle(p);
		pairs.push_back({ p, c });
	}

	// Redacted cheese pair generation because I want you to be happy

	for (int i = 0; i < 20; i++)
	{
		swap(pairs[getRand() % 20], pairs[getRand() % 20]);
	}

	std::cout << "OUTPUT.TXT STARTS HERE\n\n";

	for (auto& pair : pairs)
	{
		std::cout << "Plaintext, ciphertext: " << pair.first << " " << pair.second << "\n";
	}

	for (int i = 0; i < 20; i++)
	{
		std::cout << "Flag, ciphertext: " << flag[i] << "\n";
	}

	std::cout << "OUTPUT.TXT ENDS HERE\n\n";
	return 1;
}
