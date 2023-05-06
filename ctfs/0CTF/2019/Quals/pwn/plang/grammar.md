```
num -> 0x[0-9a-f]+ | 0[0-9]+ | [0-9]+'.'?[0-9]+
		
string -> '"' [.]* '"'

id -> [a-zA-Z_]+[a-zA-Z_0-9]*

varDef -> 'var'[ \t]+id ('=' exp)?

ifStat -> 'if' '(' exp ')' (block | statements) ('else' block)?

whileStat -> 'while' '(' exp ')' (block | statements)

forStat -> 'for'[ \t]+id[ \t]+'(' exp ')' (block | statements)

breakStat -> 'break'

continueStat -> 'continue'

returnStat -> 'return'[ \t]+ exp

paraList -> id?(,id)*

funDef -> 'fun' id '(' paraList ')' block

subscriptCall -> id[ \t]* '[' exp ']'

getterCall -> id[ \t]* block?

setterCall -> id[ \t]* '='[ \t]* exp

methodCall -> id[ \t]* '(' paraList ')' [ \t]* block?

MethodsCall -> (id[ \t]*.)? (methodCall | setterCall | getterCall)

callStat -> subscriptCall | methodCall

statements -> (ifStat | whileStat | forStat | breakStat | continueStat | returnStat | callStat)*

infixOp = '+' | '-' | '*' | '/' | '%' | '>' | '<' | '==' | '!=' | '>=' | '<=' | '&&' | '||' | '&' | '|' | '~' | '>>' | '<<'

prefixOp = '-' | '!'

infixExp -> exp ([ \t]*infixOp [ \t]*exp)+

prefixExp -> prefixOp [ \t]*exp

exp -> num | string | id | callStat | infixExp | prefixExp

block -> '{' ('|' paraList '|')? statements '}'

instantField -> varDef

staticField -> 'static'[ \t]+ instantField

fieldDef -> (instantField | staticField)*s

methodDef -> 'static'?[ \t]+ id'(' paraList ')' block

getterDef -> 'static'?[ \t]+ id[ \t]+ block

setterDef -> 'static'?[ \t]+ id[ \t]*'='[ \t]*'(' id ')'[ \t]+ block

methodsDef -> (methodDef | getterDef | setterDef)*

classDef -> 'class' id (< id)? '{' fieldDef | methodsDef '}'
```

