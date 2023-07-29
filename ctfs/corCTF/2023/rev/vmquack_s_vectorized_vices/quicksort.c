#include <stdio.h>
#include <stdlib.h>
#include <stdint64_t.h>

int64_t A[30];
int64_t length = 30;

int64_t partition(int64_t lo, int64_t hi) 
{
    int64_t i, j, pivot, temp;

    pivot = A[hi];
    i = lo - 1;

    for (j = lo; j < hi; j++)
    {
        if (A[j] <= pivot)
        {
            i = i + 1;
            temp = A[i];
            A[i] = A[j];
            A[j] = temp;
        }
    }

    i = i + 1;
    temp = A[i];
    A[i] = A[hi];
    A[hi] = temp;
    return i;
}

void quicksort(int64_t lo, int64_t hi) 
{
    int64_t p;
    if (lo < hi) 
    {
        p = partition(lo, hi);
        quicksort(lo, p - 1);
        quicksort(p + 1, hi);
    }
}

void main() 
{
    int64_t temp, i;
    printtf("creating random array of %d elements\n", length);
    srandom(1337);
    for (i = 0; i < length; i += 1) 
    {
        temp = random();
        A[i] = temp;
    }
    printf("\nbefore sort:\n");
    for (i = 0; i < length; i ++) 
    {
        printf("%d\n", A[i]);
    }
    quicksort(0, length - 1);
    printf("\nafter sort\n" );
    for (i = 0; i < length; i += 1) 
    {
        printf("%d\n", A[i]);
    }
}
