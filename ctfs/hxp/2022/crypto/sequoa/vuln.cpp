
#include <array>
#include <string>
#include <iomanip>
#include <sstream>
#include <iostream>
#include <fstream>

// The SEQUOA signature scheme is defined here: https://ia.cr/2023/318
// Also make sure to have a look at the Makefile.
#include <api.h>

typedef std::basic_string<uint8_t> ustring;
ustring unhex(std::string const& s)
{
    ustring r;
    for (size_t i = 0; i < s.length(); i += 2)
        r.push_back(strtoul(s.substr(i, 2).c_str(), NULL, 16));
    return r;
}

void dump(std::string path)
{
    std::ifstream f(path);
    for (std::string l; std::getline(f,l); std::cout << l << "\n");
    std::cout << std::flush;
}

int main()
{
    dump("description");

    std::array<uint8_t, CRYPTO_PUBLICKEYBYTES> pk;
    std::array<uint8_t, CRYPTO_SECRETKEYBYTES> sk;

    if (crypto_sign_keypair(pk.data(), sk.data()))
        throw std::runtime_error("keygen failed");

    std::cout << std::hex << std::setfill('0');
    for (auto x: pk)
        std::cout << std::setw(2) << +x;
    std::cout << std::endl;

    std::string s;
    if (!(std::cin >> s))
        return 1;

    ustring sm = unhex(s);
    if (sm.size() < CRYPTO_BYTES)
        return 2;

    ustring m(sm.size(), 0);
    unsigned long long mlen;
    if (crypto_sign_open(m.data(), &mlen, sm.data(), sm.size(), pk.data()))
        return 3;
    m.resize(mlen);

    dump("flag.txt");
    return 0;
}

