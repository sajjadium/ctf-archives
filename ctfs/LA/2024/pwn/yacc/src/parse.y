%{
#include "calc.h"
%}
%union {
	long num;
	Node *node;
}

%type <node> expr uexpr pexpr
%token <num> LNUM

%left '+' '-'
%left '*' '/' '%'
%%
prog:
|	prog stmt

stmt:
	expr ';'
	{
		emit($1);
		freenode($1);
	}

expr:
	uexpr
|	expr '*' expr
	{
		$$ = mknode(OMUL, $1, $3);
	}
|	expr '/' expr
	{
		$$ = mknode(ODIV, $1, $3);
	}
|	expr '%' expr
	{
		$$ = mknode(OREM, $1, $3);
	}
|	expr '+' expr
	{
		$$ = mknode(OADD, $1, $3);
	}
|	expr '-' expr
	{
		$$ = mknode(OSUB, $1, $3);
	}

uexpr:
	pexpr
|	'+' pexpr
	{
		$$ = $2;
	}
|	'-' pexpr
	{
		Node *n = mknode(ONUM, NULL, NULL);
		n->num = 0;
		$$ = mknode(OSUB, n, $2);
	}

pexpr:
	'(' expr ')'
	{
		$$ = $2;
	}
|	LNUM
	{
		$$ = mknode(ONUM, NULL, NULL);
		$$->num = $1;
	}
