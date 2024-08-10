#include <fstream>
#include <iostream>
#include <fstream>

template<typename φ>
struct 非 {};

template<typename φ, typename ψ>
struct 若 {};

template<typename φ>
struct 證 {};

template<typename φ, typename ψ>
using Ⅰ = 證<若<φ,若<ψ,φ>>>;

template<typename φ, typename ψ, typename χ>
using Ⅱ = 證<若<若<φ,若<ψ,χ>>,若<若<φ,ψ>,若<φ,χ>>>>;

template<typename φ, typename ψ>
using Ⅲ = 證<若<若<非<φ>,非<ψ>>,若<ψ,φ>>>;

template<typename... Φ>
struct 古 {};

template<typename φ, typename ψ>
struct 古<證<若<φ,ψ>>,證<φ>> {
    using 攵 = 證<ψ>;
};

template<typename... Φ>
using 故 = typename 古<Φ...>::攵;

template<typename T>
struct 驗 {
    驗() {
        std::cout << "[Nope!]";
    }
};

struct 𝑝 {};

template<>
struct 驗<證<若<𝑝,𝑝>>> {
    驗() {
        std::cout << std::ifstream{"fl.txt"}.rdbuf();
    }
};

template<>
struct 驗<證<若<非<非<𝑝>>,𝑝>>> {
    驗() {
        std::cout << std::ifstream{"ag.txt"}.rdbuf();
    }
};

int main() {
    std::cout << "\n";
}
