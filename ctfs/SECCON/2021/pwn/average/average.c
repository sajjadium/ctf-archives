#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    long long n, i;
    long long A[16];
    long long sum, average;

    alarm(60);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf("n: ");
    if (scanf("%lld", &n)!=1)
        exit(0);
    for (i=0; i<n; i++)
    {
        printf("A[%lld]: ", i);
        if (scanf("%lld", &A[i])!=1)
            exit(0);
        //  prevent integer overflow in summation
        if (A[i]<-123456789LL || 123456789LL<A[i])
        {
            printf("too large\n");
            exit(0);
        }
    }

    sum = 0;
    for (i=0; i<n; i++)
        sum += A[i];
    average = (sum+n/2)/n;
    printf("Average = %lld\n", average);
}
