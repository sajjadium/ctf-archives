#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>

#ifndef EXTERN
#define EXTERN extern
#endif

#define INPSZ 4096
#define CODESZ 4096

typedef struct Node Node;
struct Node {
	int op;
	Node *l;
	Node *r;
	long num;
};

enum {
	OADD,
	OSUB,
	ODIV,
	OMUL,
	OREM,
	ONUM,
};

/*
*	util.c
*/
void yyerror(char *);
void *emalloc(int);

/*
*	lex.c
*/
void compile();
char get();
void unget(char);
int yylex();

/*
*	ast.c
*/
Node *mknode(int, Node *, Node *);
void freenode(Node *);

/*
*	gen.c
*/
void startelf(void);
void endelf(void);
void putcode(char *, int);
void emit(Node *);

EXTERN char inpbuf[INPSZ];
EXTERN FILE	*outfile;
EXTERN struct {
	int len;
	char buf[CODESZ];
} code;
