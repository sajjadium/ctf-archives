#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

#define MAX_TOKEN_SIZE 1024
#define next(token) (*(token) = (*(token))->next)

typedef struct token {
  char *str;
  struct token *next;
} Token;

typedef enum { none, number, string, function } Type;

typedef struct number {
  int64_t value;
} Number;

typedef struct string {
  char *str_ptr;
  size_t str_len;
} String;

typedef struct function {
  char *function_name;
} Function;

typedef struct node {
  Type type;
  struct node *child_nodes;
  struct node *next;
  union {
    Number number;
    String string;
    Function func;
  } value;
} Node;

// Cool ascii art from:
// https://github.com/jreeee/dotfiles/blob/master/misc/lain-solid
char logo[] = ""
  "                  .=.\n"
  "                  '='\n"
  "                  ___\n"
  "       .**.   .*MWWWWWM*.   .**.\n"
  "     .MWv\"' *MWW'\"\"\"\"\"'WWM* '\"vWM.\n"
  "   .MW\"´  .WW.´         `.WW.  `\"WM.\n"
  " .MW\"     MW/   .*MWM*.   \\WM     \"MW.\n"
  " MW:     .WW    MWWWWWM    WW.     :WM\n"
  " WW*     'WM    WWWWWWW    MW'     *MW\n"
  "  \"WM.    WW\\   \"*WWW*\"   /WW    .MW\"\n"
  "    ':W*. 'WWM.         .MWW' .*W:'\n"
  "  .=. `\"WW `*WWWv.   .vWWW*´ WW\"´ .=.\n"
  "  '='        `\"*WW   WW*\"´        '='\n"
  "                WW   WW\n"
  "                WW   WW     \n"
  "        oM.    ,WW   WW.    .Mo\n"
  "        `*WM*-*WW'   'WW*-*MW*´\n"
  "           `\"-\"´       `\"-\"´   \n";

_Bool panic = false;

void boot_os(void);
void add_token(const char *token_str, size_t token_len, Token **beg, Token **end);
void destroy_tokens(Token *token);
Token *tokenize(const char *s, size_t len);
Node *create_node(void);
void destroy_nodes(Node *node);
_Bool is_number(const char *s);
char *get_string_literal(char *s, size_t *ret_len);
char *get_function_by_name(char *s);
Node *parse_token(Token **token);
Node *parse_expr(Token **token);
Node *eval_function(Node *node);
Node *eval(Node *node);
Node *plus_fnc(Node *args);
Node *mul_fnc(Node *args);
Node *none_fnc(Node *args);
void print_node(Node *args);
int main();

void boot_os(void) {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  puts(logo);
}

void add_token(const char *token_str, size_t token_len, Token **beg, Token **end) {
  Token *new_token = calloc(1, sizeof (Token));
  if (new_token == NULL) {
    fprintf(stderr, "I just don't know what went wrong...\n");
    exit(-1);
  }
  new_token->next = NULL;
  new_token->str = calloc(1, strlen(token_str) + 1);
  if (new_token->str == NULL) {
    fprintf(stderr, "I just don't know what went wrong...\n");
    exit(-1);
  }
  memcpy(new_token->str, token_str, token_len);
  if (*beg == NULL) {
    *beg = new_token;
    *end = new_token;
  } else {
    (*end)->next = new_token;
    *end = new_token;
  }
}

void destroy_tokens(Token *token) {
  if (token == NULL)
    return;
  destroy_tokens(token->next);
  free(token->str);
  free(token);
}

Token *tokenize(const char *s, size_t len) {
  char token_str[MAX_TOKEN_SIZE + 1];
  size_t token_length = 0;
  Token *beg = NULL;
  Token *end = NULL;
  _Bool inside_string = false;
  for (size_t i = 0; i < len; ++i) {
    char c = s[i];
    if ((c == ' ' || c == '\n' || c == '(' || c == ')') && !inside_string) {
      if (token_length != 0) {
        token_str[token_length] = '\0';
        add_token(token_str, token_length, &beg, &end);
        token_length = 0;
      }
      if (c == '(') {
        add_token("(", 1, &beg, &end);
      } else if (c == ')') {
        add_token(")", 1, &beg, &end);
      }
    } else if (token_length <= MAX_TOKEN_SIZE) {
      token_str[token_length++] = c;
    } else {
      panic = true;
      fprintf(stderr, "Token too long! Aborting...\n");
      return beg;
    }

    if (c == '"') {
      if (inside_string) {
        token_str[token_length] = '\0';
        add_token(token_str, token_length, &beg, &end);
        token_length = 0;
      }
      inside_string = !inside_string;
    }
  }

  return beg;
}

Node *create_node(void) {
  Node *node = malloc(sizeof (Node));
  if (node == NULL) {
    fprintf(stderr, "I just don't know what went wrong...\n");
    exit(-1);
  }
  node->child_nodes = NULL;
  node->next = NULL;
  node->type = none;
  return node;
}

void destroy_nodes(Node *node) {
  if (node == NULL)
    return;
  if (node->child_nodes != NULL)
    destroy_nodes(node->child_nodes);
  if (node->next != NULL)
    destroy_nodes(node->next);
  if (node->type == string)
    free(node->value.string.str_ptr);
  free(node);
}

_Bool is_number(const char *s) {
  while (*s)
    if (!isdigit(*s++))
      return false;
  return true;
}

char *get_string_literal(char *s, size_t *ret_len) {
  if (s == NULL)
    return NULL;
  if (*s != '"') 
    return NULL;
  size_t len = 1;
  while (s[len] != '"')
    ++len;
  char *new_s = calloc(1, len+1);
  memcpy(new_s, s+1, len-1);
  new_s[len] = '\0';
  *ret_len = len-1;
  return new_s;
}

char *get_function_by_name(char *s) {
  if (strcmp(s, "+") == 0) {
    return "+";
  } else if (strcmp(s, "*") == 0) {
    return "*";
  } else {
    return NULL;
  }
}

Node *parse_token(Token **token) {
  Node *node = create_node();
  char *str = NULL;
  size_t len;
  if (is_number((*token)->str)) {
    node->type = number;
    node->value.number.value = strtoll((*token)->str, NULL, 10);
  } else if ((str = get_string_literal((*token)->str, &len))) {
    node->type = string;
    node->value.string.str_ptr = str;
    node->value.string.str_len = strlen(str);
  } else {
    node->type = function;
    char *function_name = (*token)->str;
    node->value.func.function_name = get_function_by_name(function_name);
  }
  next(token);
  return node;
}

Node *parse_expr(Token **token) {
  if (token == NULL) {
    panic = true;
    return NULL;
  }
  
  Node *node = NULL;
  if (strcmp((*token)->str, "(") == 0) {
    next(token);
    node = parse_expr(token);
    if (node == NULL || node->type != function) {
      panic = true;
      return NULL;
    }
    while (strcmp((*token)->str, ")")) {
      Node *child_node = parse_expr(token);
      child_node->next = node->child_nodes;
      node->child_nodes = child_node;
    }
    next(token);
  } else if (strcmp((*token)->str, ")") == 0) {
    panic = true;
    return NULL;
  } else {
    node = parse_token(token);
  }

  return node;
}

Node *plus_fnc(Node *args) {
  Node *node = create_node();
  
  if (args->type == number) {
    node->type = number;
    node->value.number.value = 0;
    while (args != NULL) {
      node->value.number.value += args->value.number.value;
      args = args->next;
    }
  } else if (args->type == string) {
    node->type = string;
    size_t new_size = 1;
    for (Node *arg = args; arg != NULL; arg = arg->next)
      new_size += strlen(arg->value.string.str_ptr);
    char *new_str = calloc(1, new_size);
    if (new_str == NULL) {
      fprintf(stderr, "I just don't know what went wrong...\n");
      exit(-1);
    }
    size_t offset = 0;
    for (Node *arg = args; arg != NULL; arg = arg->next) {
      size_t arg_len = arg->value.string.str_len;
      memcpy(new_str+offset, arg->value.string.str_ptr, arg_len);
      offset += arg_len;
    }
    node->value.string.str_ptr = new_str;
    node->value.string.str_len = new_size;
  }
  
  return node;
}

Node *mul_fnc(Node *args) {
  Node *node = create_node();
  
  node->type = number;
  node->value.number.value = 1;
  while (args != NULL) {
    node->value.number.value *= args->value.number.value;
    args = args->next;
  }

  return node;
}

Node *none_fnc(Node *args) {
  Node *ret = create_node();
  ret->type = none;
  return ret;
}

Node *eval_function(Node *node) {
  Node *args = NULL;
  for (Node *child_node = node->child_nodes;
       child_node != NULL;
       child_node = child_node->next) {
    Node *evaled_node = eval(child_node);
    evaled_node->next = args;
    args = evaled_node;
  }

  char *function_name = node->value.func.function_name;
  Node *ret_node = NULL;
  if (function_name == NULL) {
    ret_node = none_fnc(args);
  } else if (strcmp(function_name, "+") == 0) {
    ret_node = plus_fnc(args);
  } else if (strcmp(function_name, "*") == 0) {
    ret_node = mul_fnc(args);
  } else {
    ret_node = none_fnc(args);
  }
  
  destroy_nodes(args);
  return ret_node;
}

Node *eval(Node *node) {
  Node *ret_node = NULL;
  switch (node->type) {
  case number:
    ret_node = create_node();
    ret_node->type = number;
    ret_node->value.number = node->value.number;
    break;
  case string:
    ret_node = create_node();
    ret_node->type = string;
    ret_node->value.string.str_len = node->value.string.str_len;
    char *str_cpy = malloc(node->value.string.str_len+1);
    if (str_cpy == NULL) {
      fprintf(stderr, "I just don't know what went wrong...\n");
      exit(-1);
    }
    memcpy(str_cpy, node->value.string.str_ptr, node->value.string.str_len+1);
    ret_node->value.string.str_ptr = str_cpy;
    break;
  case function:
    ret_node = eval_function(node);
    break;
  default:
    break;
  }
  return ret_node;
}

void print_node(Node *args) {
  for (Node *node = args; node != NULL; node = node->next) {
    switch (node->type) {
    case number:
      printf("%ld ", node->value.number.value);
      break;
    case string:
      printf("%s ", node->value.string.str_ptr);
      break;
    default:
      break;
    }
  }
  puts("");
}

void you_should_be_able_to_solve_this(void) {
  // :-)
  system("/bin/sh");
}

int main() {
  boot_os();
  _Bool quit = false;
  while (!quit) {
    char line[10000+1];
    size_t line_len = 0;
    Token *root_token = NULL;
    Node *ast = NULL;
    Node *final = NULL;
    
    printf("CoplandOS <<< ");

    line_len = read(STDIN_FILENO, line, 10000);
    line[line_len] = 0;
    if (strncmp(line, "quit", 4) == 0) {
      quit = true;
      goto cleanup;
    }
    
    root_token = tokenize(line, line_len);
    if (panic)
      goto cleanup;
    Token *tokens = root_token;
    ast = parse_expr(&tokens);
    if (panic)
      goto cleanup;
    final = eval(ast);
    if (panic)
      goto cleanup;
    print_node(final);

  cleanup:
    panic = false;
    destroy_nodes(final);
    destroy_nodes(ast);
    destroy_tokens(root_token);
  }
  
  return 0;
}
