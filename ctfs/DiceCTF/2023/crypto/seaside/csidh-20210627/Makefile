
.PHONY: main bench clean

BITS?=512

ifndef UINT_IMPL
	UINT_IMPL=uint.c
	ifneq ("$(wildcard p${BITS}/uint.s)", "")
		UINT_IMPL=$(wildcard p${BITS}/uint.*)
	endif
endif

ifndef FP_IMPL
	FP_IMPL=fp.c
	ifneq ("$(wildcard p${BITS}/fp.s)", "")
		FP_IMPL=$(wildcard p${BITS}/fp.*)
	endif
	FP_IMPL+=$(wildcard p${BITS}/inv/*.c p${BITS}/inv/*.s)
endif


sources = p${BITS}/constants.c
sources += rng.c
sources += ${UINT_IMPL} ${FP_IMPL}
sources += mont.c
sources += csidh.c

includes = $(wildcard *.h p${BITS}/*.h)

main: libcsidh.so
	@cc \
		-I ./ \
		-I p${BITS}/ \
		-std=c99 -pedantic \
		-Wall -Wextra \
		-march=native -O3 \
		-DNDEBUG \
		./libcsidh.so \
		main.c \
		-o main

libcsidh.so: ${includes} ${sources}
	@cc \
		-shared \
		-fPIC -fvisibility=hidden \
		-I ./ \
		-I p${BITS}/ \
		-std=c99 -pedantic \
		-Wall -Wextra \
		-march=native -O3 \
		-DNDEBUG \
		$(sources) \
		-o libcsidh.so


debug: ${includes} ${sources} main.c
	cc \
		-I ./ \
		-I p${BITS}/ \
		-std=c99 -pedantic \
		-Wall -Wextra \
		-g \
		$(sources) \
		main.c \
		-o debug


bench: ${includes} ${sources} bench.c
	@cc \
		$(if ${BENCH_ITS},-DBENCH_ITS=${BENCH_ITS}) \
		$(if ${BENCH_VERBOSE},-DBENCH_VERBOSE=${BENCH_VERBOSE}) \
		-I ./ \
		-I p${BITS}/ \
		-std=c99 -pedantic \
		-Wall -Wextra \
		-march=native -O3 \
		-DNDEBUG \
		$(sources) \
		bench.c \
		-o bench


clean:
	@rm -f main debug bench libcsidh.so

