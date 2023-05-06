#include "util.hpp"

#include <cstdio>
#include <chrono>

using util::Random;

void util::readUntilNewline()
{
	char newline = 0;
	while (newline != '\n')
	{
		if (scanf("%c", &newline) == EOF)
		{
			throw 0;
		}
	}
}

Random::Random()
	: engine(std::chrono::system_clock::now().time_since_epoch().count())
{
	// Noting to do
}

Random::result_type Random::in_range(Random::result_type min, Random::result_type max)
{
	std::uniform_int_distribution<result_type> distribution(min, max);
	return distribution(engine);
}

bool Random::bit()
{
	return this->in_range(0, 1) == 1;
}

Random util::random;
