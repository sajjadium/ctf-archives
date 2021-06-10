program -> statement

statement -> {statement} | if_stat | while_stat | func_decl | return | expression

if_stat = "if" '(' expression ')' statement else_stat

else_stat = E | "else" statement

while_stat = "while" '(' expression ')' statement

func_decl = "func" id '(' ')' statement

expression = var_dec | math_op

var_dec = id "=" type

type = list | string | num | id

list = '[' list_entry ']'

list_entry = type | type ',' list_entry

string = '"' [.]* '"'

num = [0-9][0-9]*

id = [a-zA-Z][a-zA-Z0-9_]*
