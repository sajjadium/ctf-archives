       IDENTIFICATION DIVISION.
       PROGRAM-ID. CBLCHALL1.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
      *    SELECT SYSIN ASSIGN TO KEYBOARD ORGANIZATION LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
      *FD SYSIN.

       WORKING-STORAGE SECTION.
       01 itr.
           05 J PIC 9(2).
       01 looping.
           05 opt PIC 9(1).
           88 ENDLOOP VALUE HIGH-VALUES.
           05 rep PIC A(1).
       01 OPT-6.
           05 fname61 PIC X(256).
           05 fname62 PIC X(256).
       01 FILES.
           05 fnm PIC X(256).
           05 fidx PIC 9(1).
           05 foff PIC 9(10) VALUE ZERO BINARY.
           05 fnmp PIC X(256) OCCURS 16 TIMES.
           05 ffd PIC 9(4) USAGE BINARY OCCURS 16 TIMES.
           05 tfd PIC 9(4) USAGE BINARY.
           05 fsz PIC 9(4) USAGE BINARY OCCURS 16 TIMES.
           05 tsz PIC 9(4) USAGE BINARY.
           05 fptr USAGE POINTER OCCURS 16 TIMES.
           05 floop PIC 9(1).



       PROCEDURE DIVISION.
           PERFORM VARYING J FROM 1 BY 1 UNTIL J > 16
               MOVE ZERO TO ffd(J)
               MOVE ZERO TO fsz(J)
           END-PERFORM.

           PERFORM UNTIL ENDLOOP
               DISPLAY "-----------------------"
               DISPLAY "1 - Create file"
               DISPLAY "2 - Open file"
               DISPLAY "3 - Read file"
               DISPLAY "4 - Write file"
               DISPLAY "5 - Close file"
               DISPLAY "6 - Copy file"
               DISPLAY "7 - Exit"
               DISPLAY "> "
               ACCEPT opt

               IF opt IS EQUAL TO 1 THEN
                   DISPLAY "File Name: "
                   ACCEPT fnm
                   DISPLAY "Index: "
                   ACCEPT fidx

                   IF (fidx IS >= 1) AND (fidx IS <= 16) THEN
                       IF fsz(fidx) EQUAL TO 0 THEN
                           DISPLAY "Buf Size: "
                           ACCEPT fsz(fidx)

                           IF (fsz(fidx) IS EQUAL TO 0) OR
      -                        (fsz(fidx) IS >= 4096) THEN
                               SET fsz(fidx) TO 1
                           END-IF

                           CALL "malloc" USING BY VALUE fsz(fidx)
      -                        RETURNING fptr(fidx)

                           IF fptr(fidx) NOT EQUAL TO NULL THEN
                               CALL "CBL_CREATE_FILE"
      -                            USING fnm 3 3 0 ffd(fidx)
                               IF RETURN-CODE NOT EQUAL TO 0 THEN
                                   DISPLAY "failed to create file"
                                   CALL "free" USING BY VALUE fptr(fidx)
                                   SET ffd(fidx) TO 0
                                   SET fsz(fidx) TO 0
                                   SET fptr(fidx) TO NULL
                               END-IF
                           ELSE
                               DISPLAY "Unable to allocate memory!"
                               SET ENDLOOP TO TRUE
                           END-IF

                       ELSE
                           DISPLAY "Not empty"
                       END-IF
                   ELSE
                       DISPLAY "Bad Input"
                   END-IF
               END-IF

               IF opt IS EQUAL TO 2 THEN
                   DISPLAY "File Name: "
                   ACCEPT fnm
                   DISPLAY "Index: "
                   ACCEPT fidx

                   IF (fidx IS >= 1) AND (fidx IS <= 16) THEN
                       IF fsz(fidx) EQUAL TO ZERO THEN
                           DISPLAY "Buf Size: "
                           ACCEPT fsz(fidx)

                           IF (fsz(fidx) IS EQUAL TO 0) OR
      -                        (fsz(fidx) IS >= 4096) THEN
                               SET fsz(fidx) TO 1
                           END-IF

                           CALL "malloc"
      -                    USING BY VALUE fsz(fidx) RETURNING fptr(fidx)

                           IF fptr(fidx) NOT EQUAL TO NULL THEN
                               CALL "CBL_OPEN_FILE"
      -                            USING fnm 3 3 0 ffd(fidx)
                               IF RETURN-CODE NOT EQUAL TO 0 THEN
                                   DISPLAY "failed to open file"
                                   CALL "free" USING BY VALUE fptr(fidx)
                                   SET ffd(fidx) TO 0
                                   SET fsz(fidx) TO 0
                                   SET fptr(fidx) TO NULL
                               END-IF
                           ELSE
                               DISPLAY "Unable to allocate memory!"
                               SET ENDLOOP TO TRUE
                           END-IF

                       ELSE
                           DISPLAY "Not empty"
                       END-IF
                   ELSE
                       DISPLAY "Bad Input"
                   END-IF
               END-IF

               IF opt IS EQUAL TO 3 THEN
                   DISPLAY "Index: "
                   ACCEPT fidx

                   IF (fidx IS >= 1) AND (fidx IS <= 16) AND fsz(fidx)
                       NOT EQUAL TO ZERO THEN
                       SET foff TO ZERO
                       SET floop TO 0
                       PERFORM UNTIL floop IS EQUAL TO 1
      *                    Sketchy code to ensure my fd is right shifted
      *                    by a bytes. TODO: If possible, rewrite this
      *                    with CBL_READ_FILE
                           DIVIDE 256 INTO ffd(fidx) GIVING tfd
                           CALL "read"
      -                      USING BY VALUE tfd fptr(fidx) fsz(fidx)
                             RETURNING foff
                           IF foff IS POSITIVE THEN
                               CALL "write"
                                 USING BY VALUE 1 fptr(fidx) fsz(fidx)
                               END-CALL
                           ELSE
                               SET floop TO 1
                           END-IF
                       END-PERFORM
                   ELSE
                       DISPLAY "Bad Input"
                   END-IF
               END-IF

               IF opt is EQUAL TO 4 THEN
                   DISPLAY "Index:"
                   ACCEPT fidx

                   IF (fidx IS >= 1) AND (fidx IS <= 16) AND fsz(fidx)
                       NOT EQUAL TO ZERO THEN
                       SET foff TO ZERO
                       SET floop TO 0
                       DISPLAY "Input:"
                       PERFORM UNTIL floop IS EQUAL TO 1
                           CALL "read"
      -                      USING BY VALUE 0 fptr(fidx) fsz(fidx)
                             RETURNING foff
                           IF foff IS POSITIVE THEN
                               DIVIDE 256 INTO ffd(fidx) GIVING tfd
                               CALL "write"
                                 USING BY VALUE tfd fptr(fidx) foff
                               END-CALL
                           ELSE
                               SET floop TO 1
                           END-IF

                           DISPLAY "Read More (Y/y for yes)"
                           ACCEPT rep
                           IF rep NOT EQUAL TO "Y" AND
                               rep NOT EQUAL TO "y" THEN
                               SET floop TO 1
                           END-IF
                       END-PERFORM
                   ELSE
                       DISPLAY "Bad Input"
                   END-IF
               END-IF

               IF opt is EQUAL TO 5 THEN
                   DISPLAY "Index: "
                   ACCEPT fidx

                   IF (fidx IS >= 1) AND (fidx IS <= 16) THEN
                       IF ffd(fidx) IS NOT Zero THEN
                           CALL "free" USING BY VALUE fptr(fidx)
                           CALL "CBL_CLOSE_FILE" USING ffd(fidx)

                           SET fsz(fidx) TO 0
                           SET ffd(fidx) TO 0
                           SET fptr(fidx) TO NULL
                       ELSE
                           DISPLAY "Bad Input"
                       END-IF
                   ELSE
                       DISPLAY "Bad Input"
                   END-IF
               END-IF

               IF opt is EQUAL TO 6 THEN
                   DISPLAY "Enter filename1: "
                   ACCEPT fname61
                   DISPLAY "Enter filename2: "
                   ACCEPT fname62
                   call "CBL_COPY_FILE" using fname61 fname62
               END-IF

               IF opt is EQUAL TO 7 THEN
                   DISPLAY "Bye!!"
                   SET ENDLOOP TO TRUE
               END-IF
           END-PERFORM
           STOP RUN.
