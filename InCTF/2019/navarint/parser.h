// #include <stdarg.h>
// #include "global.h"
// #include "tokens.h"
#include <stdarg.h>
// #include <string.h>
#include "vm.h"


void global_declaration();
void type();
void idf();
void defn();
void name();
void parameters();
void block();
void vardec();
void statement();
void expression(int);

long basetype;


void emit(int size, ...)
{
  va_list ap;
  va_start(ap, size);
  for (int i = 0; i < size; i++)
  {
    ++text;
    *text=va_arg(ap, long);
  }
  va_end(ap);
}

void match(long tk)
{
  if (token == tk) {next();} //printf("Token = %d\n", token);
  else
  {
    if (tk <128)
    {
      printf("Expected token: %c got %d",(char)tk, (int)token);
    }
    else
    {
      char* tn = tokname[tk];
      printf("Expected token: %s",tn);

    }
    exit(-1);

    printf("Unexpected token: %ld",tk);
  }
}

void program()
{
  while(1)
  {
    if (!(old_text=text=(long*)malloc(poolsize)))
    {
      die("malloc");
    }
    orig=text+1;
    long* itext=text;
    // text=text;
    old_text += 1;
    if (!(old_src=src=(char*)malloc(poolsize)))
    {
      die("malloc");
    }
    char* isrc=src;
    opreq =1;
    memset(text,0,poolsize);
    memset(src,0,poolsize);
    printf("In [%ld]: ",line+1);
    get_inp(src, poolsize-1);
    next();
    global_declaration();
    emit(1,EXIT);
    eval();
    puts("");
    free(itext);
    free(isrc);
  }
}

void global_declaration()
{
  statement();
}

void expression(int level)
{
  st* temp=NULL;
  int isArrRef=0;

  /* Parse Integers */
  if (token == Num)
  {
    emit(3, IMM, INT, token_val);
    match(Num);
    expr_type = INT;
  }

  /* Parse identifiers */
  else if(token == Id)
  {
    temp = cur;
    match(Id);
    if (!temp->value)
    {
      temp->value = (val*)malloc(sizeof(val));
      temp->value->type = NONE;
      temp->value->data = 0;
    }
    if (temp->value->type == FUNC)
    {
      if (token == '(')
      {
        match('(');
        match(')');
        emit(2,CALL,temp->value->data);
      }
    }
    else
    {
      emit(3, IMM, PTR, temp);
      emit(1,GET);
    }
  }

  /* Parse strings */
  else if(token == '"')
  {
    str* s = (str*)calloc(sizeof(str)+(size_t)(data-token_val+1),1);
    s->size = (long)(data-token_val);
    strncpy((char*)&s->data, (char*)token_val,s->size);

    emit(3, IMM, STR, s);
    match('"');
  }

  /* Parse List */
  if(token == Brak)
  {
    if (temp!=NULL)
    {
      /* Array reference */
      *text=PUSH;
      match(Brak);
      expression(Assign);
      emit(1,GETELEM);
      match(']');
      isArrRef = 1;
    }
    else
    {
      /* List declaration */
      match(Brak);

      list* lst = (list*)calloc(sizeof(list),1);

      while (token != ']')
      {
        emit(3,IMM,LIST,lst);
        emit(1,PUSH);
        expression(Assign);
        if (token == ',')
          match(',');
        emit(1,ADDELEM);
      }

      emit(3, IMM, LIST, lst);
      match(']');
    }
  }

  // else {puts("");puts("\t\tInvalid Syntax");}

  while (token >= level)
  {
    if (token == Assign)
    {
      long tmp = expr_type;
      if (*text!=GET && *text!=GETELEM)
      {
        die("bad lvalue");
      }
      *text = PUSH;
      match(Assign);
      expression(Assign);
      if (isArrRef) emit(1,SETELEM);
      else emit(1,SET);
      opreq = 0;
    }
    else if(token == Eq)
    {
      emit(1,PUSH);
      match(Eq);
      expression(Shl);
      emit(1,EQ);
    }
    else if(token == Ne)
    {
      emit(1,PUSH);
      match(Ne);
      expression(Shl);
      emit(1,NE);
    }
    else if(token == Lt)
    {
      emit(1,PUSH);
      match(Lt);
      expression(Shl);
      emit(1,LT);
    }
    else if(token == Gt)
    {
      emit(1,PUSH);
      match(Gt);
      expression(Shl);
      emit(1,GT);
    }
    else if(token == Shl)
    {
      emit(1,PUSH);
      match(Shl);
      expression(Add);
      emit(1,SHL);
    }
    else if(token == Shr)
    {
      emit(1,PUSH);
      match(Shr);
      expression(Add);
      emit(1,SHR);
    }
    else if(token == Add)
    {
      emit(1,PUSH);
      match(Add);
      expression(Mul);
      emit(1,ADD);
    }
    else if(token == Sub)
    {
      emit(1,PUSH);
      match(Sub);
      expression(Mul);
      emit(1,SUB);
    }
    else if(token == Mul)
    {
      emit(1,PUSH);
      match(Mul);
      expression(Inc);
      emit(1,MUL);
    }
    else if(token == Div)
    {
      emit(1,PUSH);
      match(Div);
      expression(Inc);
      emit(1,DIV);
    }
    // else if (token == Brak)
    // {
    //   if (temp!=NULL)
    //   {
    //     /* Array reference */
    //     *text=PUSH;
    //     match(Brak);
    //     expression(Assign);
    //     emit(1,GETELEM);
    //     match(']');
    //     isArrRef = 1;
    //   }
    //   else
    //   {
    //     /* List declaration */
    //   }
    // }

  }
}

void statement()
{
  if (token == If)
  {
    match(If);
    match('(');
    expression(Assign);
    match(')');

    emit(1,JZ);
    long *b = ++text;

    statement();

    if (token == Else)
    {
      match(Else);
      emit(1,JMP);
      *b = (long)(text+2);
      b=++text;
      statement();
    }

    *b=(long)(text+1);
  }
  else if (token == While)
  {
    long *a=NULL;
    long *b=text+1;
    match(While);
    match('(');
    expression(Assign);
    match(')');
    emit(1,JZ);
    a=++text;
    statement();
    emit(1,JMP);
    emit(1,(long)b);
    *a=(long)(text+1);
  }

  else if (token == Func)
  {
    match(Func);
    if (token != Id)
    {
      puts("ERROR: Invalid Syntax.");
      exit(-1);
    }
    cur->value = (val*)malloc(sizeof(val));
    cur->value->type = FUNC;
    cur->value->data = (long)malloc(sizeof(func));
    func* tmp = (func*)cur->value->data;
    tmp->head = NULL;
    tmp->code = (long*)malloc(poolsize);

    long* save = text;
    text = tmp->code;
    // scope = tmp->param;
    scope = &tmp->head;

    match(Id);
    match('(');
    // parameters();

    match(')');
    statement();

    if (*text != RET) emit(1,RET);

    text = save;
    scope = &symtab;
    tmp->code++;
  }

  else if (token == '{')
  {
    match('{');
    while (token != '}')
      statement();
    match('}');
  }
  else if (token == Return)
  {

    if (scope == &symtab)
    {
      puts("Invalid return!");
      exit(-1);
    }
    match(Return);
    expression(Assign);
    emit(1,RET);
  }

  else if (token == '\0')
  {
    opreq=0;
    return;
  }
  else
  {
    expr_type=-1;
    expression(Assign);
    if (token == ';')
      match(';');
  }
}

void parameters()
{
  if (token == Id)
  {
    match(Id);
    if (token == ',')
    {
      match(',');
      parameters();
    }
  }
  return;
}

void block()
{
  return;
}
