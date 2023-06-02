#include <bits/stdc++.h>
using namespace std;

int64_t manipulate(const string &input)
{
    const int32_t SZ = input.size(), B1 = 131, B2 = 13, K = 1e9 + 7;
    int64_t fh[SZ], fs[SZ], pw1[SZ], pw2[SZ];
    for (int i = 0; i < SZ; ++i) fh[i] = fs[i] = 0;
    pw1[0] = pw2[0] = 1;
    for (int _ = 1; _ <= SZ; ++_)
    {
        pw1[_] = pw1[_-1] * B1 % K;
        pw2[_] = pw2[_-1] * B2 % K;

        fh[_] = (fh[_-1] * B1 + input[_-1]) % K;
        fs[_] = (fs[_-1] * B2 + input[_-1]) % K;
    }

    int64_t f = (fh[SZ] - fh[0] * pw1[SZ] % K + K) % K;
    int64_t s = (fs[SZ] - fs[0] * pw2[SZ] % K + K) % K;

    return (f << 31) ^ s;
}

int main()
{
    while (true)
    {
        printf("Error. Login Required.\n");
        printf("Please enter the corresponding passcodes to proceed.\n");

        int64_t a, b, c, d;

        printf("Enter \'a\'\n");
        cin >> a;

        printf("Enter \'b\'\n");
        cin >> b;

        printf("Enter \'c\'\n");
        cin >> c;

        printf("Enter \'d\'\n");
        cin >> d;

        int64_t x = manipulate(to_string(a));
        int64_t y = manipulate(to_string(b));
        int64_t z = manipulate(to_string(c));
        int64_t w = manipulate(to_string(d));

        int64_t token = manipulate(to_string(x + y + z + w));
        cout << "ctf{" << to_string(token) << "}\n";
    }
}