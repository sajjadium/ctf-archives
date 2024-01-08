#include <bits/stdc++.h>
#define ll long long

using namespace std;
ll counter = -1;
ll fibbmod(ll n)
{
    counter++;
    if (n == 0)
        return 2;
    else if (n == 1)
        return 3;
    // cout << counter << " " << n << "\n";
    if (counter % 2)
    {
        return fibbmod(n - 1) - fibbmod(n - 2);
    }
    else
    {
        return fibbmod(n - 1) + 2 * fibbmod(n - 2);
    }
}

int main() // Driver function to see the value of first 30 numbers in the series
{
    for (ll i = 0; i < 30; i++)
    {
        counter = -1;
        ll x = fibbmod(i);
        cout << i << "->" << x << "\n";
    }
    return 0;
}