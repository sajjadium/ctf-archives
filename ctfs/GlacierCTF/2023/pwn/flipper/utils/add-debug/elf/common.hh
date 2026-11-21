#ifndef _ELFPP_COMMON_HH_
#define _ELFPP_COMMON_HH_

#define ELFPP_BEGIN_NAMESPACE namespace elf {
#define ELFPP_END_NAMESPACE   }

#include <cstdint>

ELFPP_BEGIN_NAMESPACE

/**
 * A byte ordering.
 */
enum class byte_order
{
        native,
        lsb,
        msb
};

/**
 * Return either byte_order::lsb or byte_order::msb.  If the argument
 * is byte_order::native, it will be resolved to whatever the native
 * byte order is.
 */
static inline byte_order
resolve_order(byte_order o)
{
        static const union
        {
                int i;
                char c[sizeof(int)];
        } test = {1};

        if (o == byte_order::native)
                return test.c[0] == 1 ? byte_order::lsb : byte_order::msb;
        return o;
}

/**
 * Return v converted from one byte order to another.
 */
template<typename T>
T
swizzle(T v, byte_order from, byte_order to)
{
        static_assert(sizeof(T) == 1 ||
                      sizeof(T) == 2 ||
                      sizeof(T) == 4 ||
                      sizeof(T) == 8,
                      "cannot swizzle type");

        from = resolve_order(from);
        to = resolve_order(to);

        if (from == to)
                return v;

        switch (sizeof(T)) {
        case 1:
                return v;
        case 2: {
                std::uint16_t x = (std::uint16_t)v;
                return (T)(((x&0xFF) << 8) | (x >> 8));
        }
        case 4:
                return (T)__builtin_bswap32((std::uint32_t)v);
        case 8:
                return (T)__builtin_bswap64((std::uint64_t)v);
        }
}

ELFPP_END_NAMESPACE

#endif
