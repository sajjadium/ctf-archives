#include "calc.h"

#define MAXNUMS 32

char elfhdr[] = {127, 69, 76, 70, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 62, 0, 1, 0, 0, 0, 120, 112, 51, 49, 0, 0, 0, 0, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64, 0, 56, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 112, 51, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 184, 60, 0, 0, 0};

char elfend[] = {15, 5};

int numcnt;

void startelf(void)
{
	fwrite(elfhdr, 1, sizeof(elfhdr), outfile);
}

void endelf()
{
	putcode(elfend, sizeof(elfend));
	fwrite(code.buf, 1, code.len, outfile);
}

void putcode(char *buf, int sz)
{
	if(code.len + sz >= CODESZ)
		yyerror("code is too long");
	for(int i = 0; i < sz; i++)
		code.buf[code.len++] = buf[i];
}

char cadd[] = {94, 95, 72, 1, 247, 87};
char csub[] = {94, 95, 72, 41, 247, 87};
char cdiv[] = {94, 95, 72, 137, 248, 72, 49, 210, 72, 247, 246, 72, 137, 199, 87};
char cmul[] = {94, 95, 72, 137, 248, 72, 247, 230, 72, 137, 199, 87};
char crem[] = {94, 95, 72, 137, 248, 72, 49, 210, 72, 247, 246, 72, 137, 215, 87};
char cnum[] = {72, 191, 0, 0, 0, 0, 0, 0, 0, 0, 87};

void emit(Node *n)
{
	switch(n->op) {
	case OADD:
		emit(n->l);
		emit(n->r);
		putcode(cadd, sizeof(cadd));
		break;
	case OSUB:
		emit(n->l);
		emit(n->r);
		putcode(csub, sizeof(csub));
		break;
	case ODIV:
		emit(n->l);
		emit(n->r);
		putcode(cdiv, sizeof(cdiv));
		break;
	case OMUL:
		emit(n->l);
		emit(n->r);
		putcode(cmul, sizeof(cmul));
		break;
	case OREM:
		emit(n->l);
		emit(n->r);
		putcode(crem, sizeof(crem));
		break;
	case ONUM:
		if(numcnt++ >= MAXNUMS)
			yyerror("too many numbers, i hate math");
		for(int i = 2; i < 10; i++)
			cnum[i] = (n->num >> (i-2)*8) & 0xff;
		putcode(cnum, sizeof(cnum));
		break;
	}
}
