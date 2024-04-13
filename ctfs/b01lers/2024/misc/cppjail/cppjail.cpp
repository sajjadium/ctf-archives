#include <type_traits>
#include "flag.h"
#include <cassert>
constexpr char flag[] = FLAG;

template<class b> struct Key {
    short i;
};

template<> struct Key<std::
bool_constant<false>>{
    char i;
};
template<> struct Key<std::
bool_constant<true>> {
    int i;
};
template<char c, int i> struct Lock {
    Key<std::bool_constant<flag[i] == c>>k;
};

template<class, class = void> struct Jail: :: std :: false_type {
    template<char c, int i> using lock=Lock<c, i>;
};
template<class T> class Jail<T, ::std::void_t<decltype(&std::declval<T>())>>: :: std ::true_type{};

class Prisoner {};

#undef FLAG
#define flag

/* you are here */

#include <stdio.h>

int main(void) {
    ::Prisoner prisoner1;
    ::Prisoner prisoner2;
    
    assert((&prisoner1) != (&prisoner2));
    ::printf("Prisoner 2 %p\n", &prisoner1);
    ::printf("Prisoner 1 %p\n", &prisoner1);
}