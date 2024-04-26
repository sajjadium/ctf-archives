CC = gcc
CFLAGS = -x c -w

ifeq ($(findstring .,$(quizz)),)
	override quizz:=$(quizz).c
endif

run: build
	@./run "$(username)"

build:
	@$(CC) $(CFLAGS) "$(quizz)" -o run

