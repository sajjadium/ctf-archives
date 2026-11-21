#ifndef _ELFPP_TO_HEX_HH_
#define _ELFPP_TO_HEX_HH_

#include <string>
#include <type_traits>

template<typename T>
std::string
to_hex(T v)
{
        static_assert(std::is_integral<T>::value,
                "to_hex applied to non-integral type");
        if (v == 0)
                return std::string("0");
        char buf[sizeof(T)*2 + 1];
        char *pos = &buf[sizeof(buf)-1];
        *pos-- = '\0';
        while (v && pos >= buf) {
                int digit = v & 0xf;
                if (digit < 10)
                        *pos = '0' + digit;
                else
                        *pos = 'a' + (digit - 10);
                pos--;
                v >>= 4;
        }
        return std::string(pos + 1);
}

#endif // _ELFPP_TO_HEX_HH_
