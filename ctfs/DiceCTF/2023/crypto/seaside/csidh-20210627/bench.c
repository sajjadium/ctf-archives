
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <assert.h>
#include <inttypes.h>

#include "rng.h"
#include "csidh.h"

static __inline__ uint64_t rdtsc(void)
{
    uint32_t hi, lo;
    __asm__ __volatile__ ("rdtsc" : "=a"(lo), "=d"(hi));
    return lo | (uint64_t) hi << 32;
}


/* defaults */

#ifndef BENCH_ITS
    #define BENCH_ITS 1000
#endif

const unsigned long its = BENCH_ITS;


const size_t stacksz = 0x8000;  /* 32k */

/* csidh.c */
bool csidh(public_key *out, public_key const *in, private_key const *priv);

int cmp_uint64_t(const void *x, const void *y) { return * (uint64_t *) x - * (uint64_t *) y; }

extern uint64_t *fp_mul_counter;
extern uint64_t *fp_sq_counter;
extern uint64_t *fp_inv_counter;
extern uint64_t *fp_sqt_counter;
extern uint64_t *xmul_counters;
extern uint64_t *isog_counters;
extern uint64_t xmul_counters_granularity;
extern uint64_t isog_counters_granularity;

uint64_t median(uint64_t *vals)
{
    qsort(vals, its, sizeof(*vals), cmp_uint64_t);
    return vals[its / 2];
}

double mean(uint64_t *vals)
{
    uint64_t sum = 0;
    for (size_t i = 0; i < its; ++i)
        sum += vals[i];
    return sum / (double) its;
}

int main()
{
    bool ret; (void) ret;
    clock_t t0, t1;
    uint64_t c0, c1;
    size_t bytes = 0;
    unsigned char *stack;

    uint64_t *cycless = calloc(its, sizeof(uint64_t)),
             *times = calloc(its, sizeof(uint64_t)),
             *mulss = calloc(its, sizeof(uint64_t)),
             *sqss = calloc(its, sizeof(uint64_t)),
             *invss = calloc(its, sizeof(uint64_t)),
             *sqtss = calloc(its, sizeof(uint64_t));

#ifdef BENCH_VERBOSE
    size_t xmuls_sz = pbits + 1;
    size_t isogs_sz = primes[NUM_PRIMES-1] + 1;

    uint64_t *xmuls = calloc(xmuls_sz, sizeof(uint64_t)),
             *isogs = calloc(isogs_sz, sizeof(uint64_t));
#endif

    private_key priv;
    public_key pub = base;

    __asm__ __volatile__ ("mov %%rsp, %0" : "=m"(stack));
    stack -= stacksz;

    for (unsigned long i = 0; i < its; ++i) {

        if (its < 100 || i % (its / 100) == 0) {
            printf("%2lu%%", 100 * i / its);
            fflush(stdout);
            printf("\r\x1b[K");
        }

        csidh_private(&priv);

        /* spray stack */
        unsigned char canary;
        randombytes(&canary, 1);
        for (size_t j = 0; j < stacksz; ++j)
            stack[j] = canary;

        fp_mul_counter = &mulss[i];
        fp_sq_counter = &sqss[i];
        fp_inv_counter = &invss[i];
        fp_sqt_counter = &sqtss[i];
#ifdef BENCH_VERBOSE
        xmul_counters = xmuls;
        isog_counters = isogs;
#endif

        t0 = clock();   /* uses stack, but not too much */
        c0 = rdtsc();

        /**************************************/

        ret = csidh(&pub, &pub, &priv);
        assert(ret);

        /**************************************/

        c1 = rdtsc();
        t1 = clock();

        fp_mul_counter = NULL;
        fp_sq_counter = NULL;
        fp_inv_counter = NULL;
        fp_sqt_counter = NULL;
#ifdef BENCH_VERBOSE
        xmul_counters = NULL;
        isog_counters = NULL;
#endif

        cycless[i] = c1 - c0;
        times[i] = t1 - t0;

        /* check stack */
        if (*stack != canary) { /* make sure we sprayed enough */
            fprintf(stderr, "\x1b[31moops!\x1b[0m used more stack than expected.\n");
            exit(1);
        }
        for (size_t j = 0; j < stacksz - bytes; ++j)
            if (stack[j] != canary)
                bytes = stacksz - j;
    }

#ifdef BENCH_VERBOSE
    printf("\nscalar multiplications (mean #):\n");
    uint64_t max_xmuls = *xmuls;
    for (size_t i = 1; i < xmuls_sz; ++i)
        if (xmuls[i] > max_xmuls) max_xmuls = xmuls[i];
    for (size_t i = 0; i < xmuls_sz; ++i) {
        if (!xmuls[i]) continue;
        printf("  length %4lu:  %6.2lf", i, 1. * xmuls[i] / its);
        printf("   |");
        for (size_t j = 48 * xmuls[i] / max_xmuls; j --> 0; ) printf("-");
        printf("\n");
    }

    printf("\nisogeny computations (mean #):\n");
    uint64_t max_isogs = *isogs;
    for (size_t i = 1; i < isogs_sz; ++i)
        if (isogs[i] > max_isogs) max_isogs = isogs[i];
    for (size_t i = 0; i < isogs_sz; ++i) {
        if (!isogs[i]) continue;
        printf("  degree %4lu:  %6.2lf", i, 1. * isogs[i] / its);
        printf("   |");
        for (size_t j = 48 * isogs[i] / max_isogs; j --> 0; ) printf("-");
        printf("\n");
    }
#endif

    printf("\niterations: %lu\n\n", its);

    printf("median clock cycles:    %8" PRIu64 "   (\x1b[36m%.1lf*10^6\x1b[0m)\n", median(cycless), 1e-6 * median(cycless));
    printf("mean clock cycles:      %10.1lf (%.1lf*10^6)\n\n", mean(cycless), 1e-6 * mean(cycless));

    printf("median wall-clock time: \x1b[34m%6.3lf ms\x1b[0m\n", 1000. * median(times) / CLOCKS_PER_SEC);
    printf("mean wall-clock time:   %6.3lf ms\n\n", 1000. * mean(times) / CLOCKS_PER_SEC);

    printf("maximum stack usage:    %6lu b\n\n", bytes);

    printf("median multiplications: %8" PRIu64 "\n", median(mulss));
    printf("mean multiplications:   %10.1lf\n", mean(mulss));

    printf("median squarings:       %8" PRIu64 "\n", median(sqss));
    printf("mean squarings:         %10.1lf\n", mean(sqss));

    printf("median inversions:      %8" PRIu64 "\n", median(invss));
    printf("mean inversions:        %10.1lf\n", mean(invss));

    printf("median square tests:    %8" PRIu64 "\n", median(sqtss));
    printf("mean square tests:      %10.1lf\n", mean(sqtss));

    printf("\n");
}

