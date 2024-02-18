#include "calc.h"

void yyerror(char *s)
{
	fprintf(stderr, "error: %s\n", s);
	exit(1);
}

void *emalloc(int n)
{
	void *p;

	p = malloc(n);
	if(!p)
		yyerror("out of memory");
	return p;
}
