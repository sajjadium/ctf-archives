#ifndef __UTIL_HPP__
#define __UTIL_HPP__

#include <random>

namespace util
{
	void readUntilNewline();

	class Random
	{
	private:
		std::default_random_engine engine;
	public:
		typedef std::default_random_engine::result_type result_type;
		Random();
		result_type in_range(result_type min, result_type max);
		bool bit();
	};

	extern Random random;
}

#endif
