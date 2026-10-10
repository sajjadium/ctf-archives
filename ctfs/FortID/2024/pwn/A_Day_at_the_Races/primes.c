#include <stdio.h>

int is_prime(long long n) {
    for (long long i=2; i*i<=n; i++)
        if (n%i == 0)
            return 0;
    return 1;
}

int main() {
    long long n = 1ll<<55;
    while (!is_prime(n))
        n++;
    printf("%lld\n", n); 
    return 0;
}