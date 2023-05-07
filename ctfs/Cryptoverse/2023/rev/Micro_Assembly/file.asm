main:
   PUSH %BP
   MOV  %SP, %BP
@main_body:
   SUB  %SP, $28, %SP
   MOV  $154, -28(%BP)
   MOV  $16, -24(%BP)
   MOV  $16, -20(%BP)
   MOV  $228, -16(%BP)
   MOV  $66, -12(%BP)
   MOV  $286, -8(%BP)
   MOV  $3, -4(%BP)
@if0:
   DIV  -28(%BP), $2, %0
   CMP  %12, $0
   JNE  @false0
@true0:
   DIV  -28(%BP), $2, %0
   MOV  %0, -28(%BP)
   JMP  @exit0
@false0:
@exit0:
   MUL  -24(%BP), $3, %0
   ADD  %0, $1, %0
   MOV  %0, -24(%BP)
   SHL  -20(%BP), $2, %0
   ADD  %0, $3, %0
   MOV  %0, -20(%BP)
@if1:
   DIV  -16(%BP), $3, %0
   CMP  %12, $1
   JNE  @false1
@true1:
   SUB  -16(%BP), $1, %0
   DIV  %0, $3, %0
   MOV  %0, -16(%BP)
   JMP  @exit1
@false1:
   DIV  -16(%BP), $2, %0
   MOV  %0, -16(%BP)
@exit1:
   SUB  -12(%BP), $2, %0
   MOV  %0, -12(%BP)
@if2:
   DIV  -8(%BP), $3, %0
   CMP  %12, $1
   JNE  @false2
@true2:
   SUB  -8(%BP), $1, %0
   DIV  %0, $3, %0
   MOV  %0, -8(%BP)
   JMP  @exit2
@false2:
   DIV  -8(%BP), $2, %0
   MOV  %0, -8(%BP)
@exit2:
   SHL  $11, -4(%BP), %0
   ADD  %0, $11, %0
   MOV  %0, -4(%BP)
   LEA  -28(%BP), %0
   MOV  %0, %13
   JMP  @main_exit
@main_exit:
   MOV  %BP, %SP
   POP  %BP
   RET 