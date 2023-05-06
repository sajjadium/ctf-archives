// #include <stdio.h>
// #include "global.h"

void next()
{
  while((token=*src)!=0)
  {
    ++src;
    if (token == '\n')
    {
      ++line;
      if(0)
      {
        char *a[]={"LEA ","IMM ","JMP ","CALL","JZ  ","JNZ ","ENT ","ADJ ","LEV ","LI  ","LC  ","SI  ","SC ","SET","GET","PUSH",
               "OR  ","XOR ","AND ","EQ  ","NE  ","LT  ","GT  ","LE  ","GE  ","SHL ","SHR ","ADD ","SUB ","MUL ","DIV ","MOD ",
               "OPEN","READ","CLOSE","PRTF","MALC","MSET","MCMP","EXIT"};
        printf("%ld: %.*s\n",line,(int)(src-old_src),old_src);
        old_src = src;
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
    // printf("%c\n",(char)token);
    else if (token == ' ' || token == '\t')
    {
      continue;
    }
    else if ( token == '#')
    {
      while (*src != '\n' || *src != 0)
        src++;
    }
    else if ((token >='A' && token<='Z') || (token >='a' && token<='z') || token=='_')
    {
      char* last_pos=src-1;
      long hash = token;
      while ((*src >='A' && *src<='Z') || (*src >='a' && *src<='z') || *src=='_' || (*src >='0' && *src<='9'))
      {
        hash = (hash*0x40) + (*src);
        src++;
      }

      // check symbol table to see if variable already exists
      cur = symtab;
      while (cur != NULL)
      {
        if (!check(cur->name,last_pos,(int)(src-last_pos)))
        {
          // varible exists

          token = cur->tok;
          return;
        }
        cur=cur->next;
      }

      // search in current scope
      if (scope != &symtab)
      {
        cur = *scope;
        while (cur != NULL)
        {
          if (!check(cur->name,last_pos,(int)(src-last_pos)))
          {
            // varible exists

            token = cur->tok;
            return;
          }
          cur=cur->next;
        }
      }
      // varible does not exist. So create new symtab entry
      char* name = (char*)calloc(src-last_pos+1,1);
      memcpy(name,last_pos,src-last_pos);
      cur = newsym();
      cur->name = name;
      cur->hash = hash;
      cur->value = 0;
      token = cur->tok = Id;
      return;
    }
    else if (((token >='0') && (token<='9')))
    {
      token_val = token-'0';
      if (token == '0' && (*src == 'x' || *src == 'X'))
      {
        // hex no.
        token=*(++src);
        while (((token >='0') && (token<='9')) || ((token >='a') && (token<='f')) || ((token >='A') && (token<='F')))
        {
          token_val=token_val*16 + (token & 0x0f) + (token >= 'A' ? 9 : 0);
          token = *(++src);
        }
      }
      else
      {
        while (*src>='0' && *src<='9')
        {
          token_val=token_val*10 + (*src - '0');
          src++;
        }
      }
      token=Num;
      return;
    }
    else if (token == '"' || token == '\'')
    {
      char* last_pos = data;
      while (*src!=0 && *src!=token)
      {
        token_val = *src++;
        if (token_val == '\\')
        {
          token_val = *src++;
          if (token_val == 'n') token_val = '\n';
        }
        if (token == '"') *data++ = (char)token_val;
      }
      src++;
      if (token == '"') token_val = (long)last_pos;
      else token = Num;
      return;
    }
    else if (token == '/')
    {
      if (*src=='/')
      {
        // comment
        while (*src !=0 && *src != '\n')
          src++;
      }
      else
      {
        token = Div;
        return;
      }
    }
    else if (token == '*')
    {
      token = Mul;
      return;
    }
    else if (token == '^')
    {
      token = Xor;
      return;
    }
    else if (token == '%')
    {
      token = Mod;
      return;
    }
    else if (token == '[')
    {
      token = Brak;
      return;
    }
    else if (token == '?')
    {
      token = Cond;
      return;
    }
    else if (token == '+')
    {
      // + or ++
      if (*src == '+') {token = Inc; src++;}
      else token = Add;
      return;
    }
    else if (token == '-')
    {
      // - or --
      if (*src == '-') {token = Dec; src++;}
      else token = Sub;
      return;
    }
    else if (token == '!')
    {
      // ! or !=
      if (*src == '=') {token = Ne; src++;}
      else token = No;
      return;
    }
    else if (token == '|')
    {
      // | or ||
      if (*src == '|') {token = Lor; src++;}
      else token = Or;
      return;
    }
    else if (token == '&')
    {
      // & or &&
      if (*src == '&') {token = Lan; src++;}
      else token = And;
      return;
    }
    else if (token == '=')
    {
      // = or ==
      if (*src == '=') {token = Eq; src++;}
      else token = Assign;
      return;
    }
    else if (token == '<')
    {
      // < or <= or <<
      if (*src == '<') {token = Shl; src++;}
      else if (*src == '=') {token = Le; src++;}
      else token = Lt;
      return;
    }
    else if (token == '>')
    {
      // > or >= or >>
      if (*src == '>') {token = Shr; src++;}
      else if (*src == '=') {token = Ge; src++;}
      else token = Gt;
      return;
    }
    else if (token == '~' || token == ']' || token == '(' || token == ')' || token == '{' || token == '}' || token == ',' || token == ';' || token == ':')
      return;

    else
    {
      printf("invalid symbol %d",(char)token);
    }
  }
  // printf("Token = %s\n", tokname[token]);
  return;
}
