#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define MASK 0x8000000000000000

// types
enum {NONE, INT, STR, LIST, PTR, FUNC};

// int line;
char *src, *old_src;
int poolsize;
int SOURCE=0;
int opreq=1;
long expr_type=NONE;


// segments
long token, *text, *old_text, token_val, line, *orig;
char *data;

// registers
long *pc, cycles;

// VM instructions
enum { LEA ,IMM ,JMP ,CALL,JZ  ,JNZ ,ENT ,ADJ ,LEV, RET ,LI  ,LC  ,SI  ,SC ,SET,GET,PUSH, GETELEM, SETELEM, ADDELEM,
       OR  ,XOR ,AND ,EQ  ,NE  ,LT  ,GT  ,LE  ,GE  ,SHL ,SHR ,ADD ,SUB ,MUL ,DIV ,MOD ,
       OPEN,READ,CLOSE,PRTF,MALC,MSET,MCMP,EXIT };


// Tokens
enum {
  Num = 128, Sys, Glo, Loc, Id, Func, Else, Enum, If, Return, Sizeof, While,
  Assign, Cond, Lor, Lan, Or, Xor, And, Eq, Ne, Lt, Gt, Le, Ge, Shl, Shr, Add, Sub, Mul, Div, Mod, Inc, Dec, No, Brak
};

char *tokname[] = {"Num", "Fun", "Sys", "Glo", "Loc", "Id",
"Char", "Else", "Enum", "If", "Int", "Lst" , "Return", "Sizeof", "While",
"Assign", "Cond", "Lor", "Lan", "Or", "Xor", "And", "Eq", "Ne", "Lt", "Gt", "Le", "Ge", "Shl", "Shr", "Add", "Sub", "Mul", "Div", "Mod", "Inc", "Dec", "No", "Brak"};


typedef struct val
{
  long type;
  long data;
}val;

val* stack;
val *sp, *bp;
val ax;

typedef struct st
{
  long tok;
  long hash;
  char* name;
  long class;
  val* value;
  struct st* next;
} st;


typedef struct str
{
  long size;
  char data[];
}str;

typedef struct list
{
  long size;
  long capacity;
  val** elements;
}list;

typedef struct func
{
  st* head;
  long* code;
}func;

st *symtab=NULL, *cur=NULL;
st **scope=NULL;

long *call_stack, *cs_sp, *cs_bp;

void die(const char *s) {
  perror(s);
  exit(1);
}

st* newsym()
{
  st* temp=(st*)malloc(sizeof(st));
  memset(temp,0,sizeof(st));
  temp->next=*scope;
  *scope=temp;
  return temp;
}

st* addsym()
{
  st* temp=(st*)malloc(sizeof(st));
  memset(temp,0,sizeof(st));
  return temp;
}

int get_inp(char * buffer, int len)
{
    int retval = read(0, buffer, len-1);
    if ( retval == -1)
        exit(0);
    return 0;
}

int check(char* a, char* b, int size)
{
  if (strlen(a)!=size)
  {
    return -1;
  }
  return memcmp(a,b,size);
}

void cleanup(val* v)
{
  if (v->type == INT)
    return;
  else if (v->type == STR)
  {
    free((long*)v->data);
    return;
  }
}

void typecheck(int type, int tocheck)
{return;
  if (type == tocheck)
   return;
  puts("Invalid operand for operator");
  exit(-1);
}


void view(val* v)
{
  if (v->type == INT)
  {
    printf("%ld",v->data);
  }
  else if (v->type == STR)
  {
    str* tmp = (str*)v->data;
    printf("\"%s\"",tmp->data);
  }
  else if (v->type == LIST)
  {
    printf("[");
    list* lst = (list*)v->data;
    for(int i=0;i<lst->size;i++)
    {
      view(lst->elements[i]);
      if (i<lst->size-1)
        printf(", ");
    }
    printf("]");
  }
}

void disas(long start)
{
  if(1)
  {
    char *a[]={"LEA ","IMM ","JMP ","CALL","JZ  ","JNZ ","ENT ","ADJ ","LEV ","LI  ","LC  ","SI  ","SC ","SET","GET", "PUSH","GETELEM", "SETELEM",
           "OR  ","XOR ","AND ","EQ  ","NE  ","LT  ","GT  ","LE  ","GE  ","SHL ","SHR ","ADD ","SUB ","MUL ","DIV ","MOD ",
           "OPEN","READ","CLOSE","PRTF","MALC","MSET","MCMP","EXIT"};
    // printf("%ld: %.*s\n",line,(int)(src-old_src),old_src);
    // old_src = src;
    while(old_text<=text)
    {

        printf("%-4s %s","",a[*old_text]);
        if (*old_text <= ADJ)
        {
          printf(" %p",(void *)*++old_text);
        }
        puts("");

      ++old_text;
    }
  }
}

char *a1[]={"LEA ","IMM ","JMP ","CALL","JZ  ","JNZ ","ENT ","ADJ ","LEV ","LI  ","LC  ","SI  ","SC ","SET","GET", "PUSH","GETELEM", "SETELEM",
       "OR  ","XOR ","AND ","EQ  ","NE  ","LT  ","GT  ","LE  ","GE  ","SHL ","SHR ","ADD ","SUB ","MUL ","DIV ","MOD ",
       "OPEN","READ","CLOSE","PRTF","MALC","MSET","MCMP","EXIT"};

char welcome_str[] = "\n"
  "   ____     _______________      _  _____ _   _____   ___  _____  ________\n"
  "  /  _/__  / ___/_  __/ __/___  / |/ / _ | | / / _ | / _ \\/  _/ |/ /_  __/\n"
 " _/ // _ \\/ /__  / / / _//___/ /    / __ | |/ / __ |/ , _// //    / / /\n"
"/___/_//_/\\___/ /_/ /_/       /_/|_/_/ |_|___/_/ |_/_/|_/___/_/|_/ /_/\n"
"\n";
