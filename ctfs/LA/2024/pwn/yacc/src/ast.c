#include "calc.h"

Node *mknode(int op, Node *l, Node *r)
{
	Node *n;

	n = emalloc(sizeof(Node));
	n->op = op;
	n->l = l;
	n->r = r;
	return n;
}

void freenode(Node *n)
{
	if(!n)
		return;
	if(!n->l)
		freenode(n->l);
	if(!n->r)
		freenode(n->r);
	free(n);
}
