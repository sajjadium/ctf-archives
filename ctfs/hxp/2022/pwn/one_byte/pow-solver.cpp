/*
small tool to solve hxp CTF's proof-of-works

# apt install libssl-dev
$ g++ -O3 -march=native pow-solver.cpp -lcrypto -pthread -o pow-solver

Example:
please give S such that sha256(unhex("541ca361107f4a2a" + S)) ends with 5 zero bits.

$ ./pow-solver 5 541ca361107f4a2a
000000000000003f
*/


#include <array>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <vector>
#include <algorithm>
#include <thread>
#include <atomic>
#include <openssl/sha.h>
#include <openssl/evp.h>

unsigned const num_threads = std::max(1u, std::thread::hardware_concurrency());
typedef std::basic_string<uint8_t> ustring;

static void brute(std::atomic<bool>& found, unsigned bits, ustring const& prefix,
                  std::vector<ustring> const& infixes, size_t suffix_len)
{

    EVP_MD_CTX *ctx, *cur_ctx;
    if (!(ctx = EVP_MD_CTX_create())) throw;
    if (!(cur_ctx = EVP_MD_CTX_create())) throw;

    if (!EVP_DigestInit_ex(ctx, EVP_sha256(), NULL)) throw;
    if (!EVP_DigestUpdate(ctx, prefix.data(), prefix.length())) throw;

    std::array<uint8_t, SHA256_DIGEST_LENGTH> hash;
    if (!suffix_len || bits > 8 * hash.size()) throw;

    for (auto const& infix: infixes) {
        std::vector<uint8_t> proof(infix.size() + suffix_len);
        std::copy(infix.begin(), infix.end(), proof.begin());
        std::fill(proof.begin() + infix.length(), proof.end(), 0);
        while (true) {
next:
            for (size_t i = proof.size() - 1; i >= infix.length(); --i) {
                if (++proof[i])
                    break;
                else if (i == infix.length())
                    goto next_prefix;
                proof[i] = 0;
            }

            if (found)
                goto done;

            if (!EVP_MD_CTX_copy_ex(cur_ctx, ctx)) throw;
            if (!EVP_DigestUpdate(cur_ctx, proof.data(), proof.size())) throw;
            if (!EVP_DigestFinal_ex(cur_ctx, hash.data(), NULL)) throw;

            for (size_t i = 0; i < bits / 8; ++i)
                if (hash[hash.size() - 1 - i]) goto next;
            for (size_t k = bits / 8, i = 0; i < bits % 8; ++i)
                if (hash[hash.size() - 1 - k] & 1 << i) goto next;

            if (found.exchange(true))
                goto done;
            std::cout << std::hex << std::setfill('0');
            for (unsigned b: proof)
                std::cout << std::setw(2) << b;
            std::cout << std::endl;
            goto done;
        }
next_prefix:;
    }

done:
    EVP_MD_CTX_destroy(ctx);
    EVP_MD_CTX_destroy(cur_ctx);
}

ustring unhex(std::string const& s)
{
    ustring r;
    for (size_t i = 0; i < s.length(); i += 2)
        r.push_back(strtoul(s.substr(i, 2).c_str(), NULL, 16));
    return r;
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        std::cerr << "arguments: $bits $prefix" << std::endl;
        return -1;
    }

    size_t bits; std::istringstream(argv[1]) >> bits;
    ustring prefix = unhex(argv[2]);

    std::atomic<bool> found {false};
    std::vector<std::thread> threads;

    for (unsigned i = 0; i < num_threads; ++i) {
        std::vector<ustring> infixes;
        for (unsigned b = i; b < 0x100; b += num_threads)
            infixes.push_back(ustring(1, b));
        threads.push_back(std::thread(brute, std::ref(found),
                    bits, prefix, infixes, prefix.length() - 1));
    }

    for (auto& t: threads)
        t.join();

    if (!found) {
        std::cerr << "\x1b[31moops\x1b[0m" << std::endl;
        return 1;
    }
}

