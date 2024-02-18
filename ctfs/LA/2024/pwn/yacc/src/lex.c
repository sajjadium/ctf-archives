#include "calc.h"
#include "y.tab.h"

#define NOPEEK -2

char used[26];
char peek = NOPEEK;
char *inp = inpbuf;

void compile()
{
	startelf();
	yyparse();
	endelf();
}

char get()
{
	char c;

	if(peek != NOPEEK) {
		c = peek;
		peek = NOPEEK;
		return c;
	}
	if(inp-inpbuf >= INPSZ)
		yyerror("input too long");
	return *inp++;
}

void unget(char c)
{
	peek = c;
}

int yylex()
{
	long v;
	char c;

	while(isspace(c = get()));
	if(isdigit(c)) {
		v = 0;
		while(isdigit(c)) {
			v = v*10 + c-'0';
			c = get();
		}
		unget(c);
		yylval.num = v;
		return LNUM;
	}
	return c;
}
