
PROGRAM puncher
  IMPLICIT NONE
  CHARACTER(len=64) :: X
  INTEGER(2) :: A,B, C
  A = 0
  B = 0
  write(*,*) 'How many lines do you want to read?'
  CALL readInt(B)
  IF (A==0) THEN
    A=64
  END IF
  DO C=1,B
    write(*,*) 'Reading line ', C
    CALL readString(X, A)
    CALL punch(X,A)
  END DO
END PROGRAM

SUBROUTINE readstring(S,L)
  INTEGER(2)	:: L
  CHARACTER(len=L) :: S
  read(*,"(A)") S
END SUBROUTINE

SUBROUTINE readInt(I)
  read(*,*) I
END SUBROUTINE

SUBROUTINE append(arr, app, D)
  IMPLICIT NONE
  TYPE string
    CHARACTER(len=64) :: s
  END TYPE
  INTEGER(2) :: C, D
  TYPE(string) :: arr(12)
  CHARACTER(len=12) :: app
  DO C=1,12
    arr(C)%s(D:D)=app(C:C)
  END DO
END SUBROUTINE

SUBROUTINE to_upper(strIn)
  IMPLICIT NONE
  CHARACTER(len=64) ::strIn
  INTEGER :: i,j
  DO i=1, 64
    j=IACHAR(strIn(i:i))
    IF (j>= IACHAR("a") .AND. j<=IACHAR("z") ) THEN
      strIn(i:i)=ACHAR(IACHAR(strIn(i:i))-32)
    END IF
  END DO
END SUBROUTINE

SUBROUTINE print_card(card, line)
  IMPLICIT NONE
  TYPE string
    CHARACTER(len=64) :: s
  END TYPE
  TYPE(string) :: card(12)
  CHARACTER(len=64) :: line
  INTEGER(4) :: C
  write(*,"(A)") '  _______________________________________________________________'
  write(*,"(A)") ' /                                                                \'
  write(*,"(A)",advance="no") '| '
  write(*,"(A)",advance="no") line
  write(*,"(A)") ' |'
  DO C=1, 12
    write(*,"(A)",advance="no") '| '
    write(*,"(A)", advance="no")card(C)%s
    write(*,"(A)") ' |'
  END DO
  write(*,"(A)") ' \________________________________________________________________/'
END SUBROUTINE

SUBROUTINE punch(S, A)
  IMPLICIT NONE
  TYPE string
    CHARACTER(len=64) :: s
  END TYPE
  CHARACTER(len=*) :: S
  INTEGER(4) :: C, D, tmp
  TYPE(string) :: L(12)
  CHARACTER(len=12) :: app
  INTEGER(4) :: current
  INTEGER(2) :: A
  DO D=1, 12
    L(D)%s=""
  END DO
  D=1
  CALL to_upper(S)
  DO C=1, A
    app="  0123456789"
    current=IACHAR(S(C:C))
    IF (current>=IACHAR("0") .AND. current<=IACHAR("9")) THEN
      tmp=current-IACHAR("0")+1
      app(tmp+3:tmp+3)="X"
    ELSE IF (current>=IACHAR("A") .AND. current<=IACHAR("I")) THEN
      tmp=current-IACHAR("A")+1
      app(1:1)="X"
      app(tmp+3:tmp+3)="X"
    ELSE IF (current>=IACHAR("J") .AND. current<=IACHAR("P")) THEN
      tmp=current-IACHAR("J")+1
      app(2:2)="X"
      app(tmp+3:tmp+3)="X"
    ELSE IF (current>=IACHAR("Q") .AND. current<=IACHAR("Z")) THEN
      tmp=current-IACHAR("Q")+1
      app(3:3)="X"
      app(tmp+3:tmp+3)="X"
    ELSE IF (current==IACHAR("&")) THEN
      app(1:1)="X"
    ELSE IF (current==IACHAR(".")) THEN
      app(1:1)="X"
      app(6:6)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("<")) THEN
      app(1:1)="X"
      app(7:7)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("(")) THEN
      app(1:1)="X"
      app(8:8)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("+")) THEN
      app(1:1)="X"
      app(9:9)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("|")) THEN
      app(1:1)="X"
      app(10:10)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("-")) THEN
      app(2:2)="X"
    ELSE IF (current==IACHAR("!")) THEN
      app(2:2)="X"
      app(5:5)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("$")) THEN
      app(2:2)="X"
      app(6:6)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("*")) THEN
      app(2:2)="X"
      app(7:7)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR(")")) THEN
      app(2:2)="X"
      app(8:8)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR(";")) THEN
      app(2:2)="X"
      app(9:9)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("/")) THEN
      app(3:3)="X"
      app(4:4)="X"
    ELSE IF (current==IACHAR(",")) THEN
      app(3:3)="X"
      app(6:6)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("%")) THEN
      app(3:3)="X"
      app(7:7)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("_")) THEN
      app(3:3)="X"
      app(8:8)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR(">")) THEN
      app(3:3)="X"
      app(9:9)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("?")) THEN
      app(3:3)="X"
      app(10:10)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR(":")) THEN
      app(5:5)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("'")) THEN
      app(8:8)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR("=")) THEN
      app(9:9)="X"
      app(11:11)="X"
    ELSE IF (current==IACHAR('"')) THEN
      app(10:10)="X"
      app(11:11)="X"
    END IF
    CALL append(L, app, D)
    D=D+1
  END DO
  CALL print_card(L, S)
END SUBROUTINE
