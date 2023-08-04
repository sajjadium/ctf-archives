.LC0:
        .string "Enter The Flag:"
.LC1:
        .string "%s"
.LC2:
        .string "Wrong Flag"
.LC3:
        .string "Correct Flag"
flag_check():
        push    rbp
        mov     rbp, rsp
        sub     rsp, 464
        mov     QWORD PTR [rbp-112], 0
        mov     QWORD PTR [rbp-104], 0
        mov     QWORD PTR [rbp-96], 0
        mov     QWORD PTR [rbp-88], 0
        mov     QWORD PTR [rbp-80], 0
        mov     QWORD PTR [rbp-72], 0
        mov     QWORD PTR [rbp-64], 0
        mov     QWORD PTR [rbp-56], 0
        mov     QWORD PTR [rbp-48], 0
        mov     QWORD PTR [rbp-40], 0
        mov     QWORD PTR [rbp-32], 0
        mov     QWORD PTR [rbp-24], 0
        mov     DWORD PTR [rbp-16], 0
        mov     edi, OFFSET FLAT:.LC0
        call    puts
        lea     rax, [rbp-112]
        mov     rsi, rax
        mov     edi, OFFSET FLAT:.LC1
        mov     eax, 0
        call    __isoc99_scanf
        movabs  rax, -871222578553387942
        movabs  rdx, -3456440840989770153
        mov     QWORD PTR [rbp-368], rax
        mov     QWORD PTR [rbp-360], rdx
        movabs  rax, -6917285895965957581
        movabs  rdx, 2096695603964784419
        mov     QWORD PTR [rbp-352], rax
        mov     QWORD PTR [rbp-344], rdx
        movabs  rax, 4501421280245125089
        movabs  rdx, -5989732096912246845
        mov     QWORD PTR [rbp-336], rax
        mov     QWORD PTR [rbp-328], rdx
        movabs  rax, -7641474145812966946
        movabs  rdx, 5943263215614115999
        mov     QWORD PTR [rbp-320], rax
        mov     QWORD PTR [rbp-312], rdx
        movabs  rax, 3346881274156629838
        movabs  rdx, -4046563652848771978
        mov     QWORD PTR [rbp-304], rax
        mov     QWORD PTR [rbp-296], rdx
        movabs  rax, 1600213061547397258
        movabs  rdx, -7907006450299616387
        mov     QWORD PTR [rbp-288], rax
        mov     QWORD PTR [rbp-280], rdx
        movabs  rax, 2641250925692849876
        movabs  rdx, 5764027888120773659
        mov     QWORD PTR [rbp-272], rax
        mov     QWORD PTR [rbp-264], rdx
        movabs  rax, -2708211178971868809
        movabs  rdx, -1437889653997315907
        mov     QWORD PTR [rbp-256], rax
        mov     QWORD PTR [rbp-248], rdx
        movabs  rax, -1790267167538066993
        movabs  rdx, 6751799815650390725
        mov     QWORD PTR [rbp-240], rax
        mov     QWORD PTR [rbp-232], rdx
        movabs  rax, -7155949167227380485
        movabs  rdx, -240513889820188763
        mov     QWORD PTR [rbp-224], rax
        mov     QWORD PTR [rbp-216], rdx
        movabs  rax, 8430573516374475283
        movabs  rdx, 7014569824855873983
        mov     QWORD PTR [rbp-208], rax
        mov     QWORD PTR [rbp-200], rdx
        movabs  rax, -1194317526320485479
        movabs  rdx, -2635243135622213470
        mov     QWORD PTR [rbp-192], rax
        mov     QWORD PTR [rbp-184], rdx
        movabs  rax, 3816607778456458796
        movabs  rdx, 7739645478794557909
        mov     QWORD PTR [rbp-176], rax
        mov     QWORD PTR [rbp-168], rdx
        movabs  rax, 2239858223738625365
        movabs  rdx, 6262919446888351940
        mov     QWORD PTR [rbp-160], rax
        mov     QWORD PTR [rbp-152], rdx
        movabs  rax, 5359968574739497219
        movabs  rdx, -5945185636638990574
        mov     QWORD PTR [rbp-144], rax
        mov     QWORD PTR [rbp-136], rdx
        movabs  rax, 4289602485438450409
        movabs  rdx, -4136753309120802266
        mov     QWORD PTR [rbp-128], rax
        mov     QWORD PTR [rbp-120], rdx
        movabs  rax, 3689636007142570038
        movabs  rdx, 7149575679097845041
        mov     QWORD PTR [rbp-400], rax
        mov     QWORD PTR [rbp-392], rdx
        movabs  rax, 3544442000607754086
        movabs  rdx, 58494055442021
        mov     QWORD PTR [rbp-390], rax
        mov     QWORD PTR [rbp-382], rdx
        movabs  rax, -6712584965997026559
        movabs  rdx, 5818345077617353901
        mov     QWORD PTR [rbp-464], rax
        mov     QWORD PTR [rbp-456], rdx
        movabs  rax, -1172694937141806812
        movabs  rdx, -4970398359911696349
        mov     QWORD PTR [rbp-448], rax
        mov     QWORD PTR [rbp-440], rdx
        movabs  rax, -7528756344694355204
        movabs  rdx, -880185776627970324
        mov     QWORD PTR [rbp-432], rax
        mov     QWORD PTR [rbp-424], rdx
        mov     WORD PTR [rbp-416], -4294
        mov     BYTE PTR [rbp-1], 0
        mov     BYTE PTR [rbp-2], 0
        mov     BYTE PTR [rbp-9], 0
        mov     DWORD PTR [rbp-8], 0
        jmp     .L2
.L7:
        mov     eax, DWORD PTR [rbp-8]
        cdqe
        movzx   eax, BYTE PTR [rbp-112+rax]
        mov     BYTE PTR [rbp-9], al
        movzx   eax, BYTE PTR [rbp-9]
        cdqe
        movzx   eax, BYTE PTR [rbp-368+rax]
        mov     BYTE PTR [rbp-1], al
        mov     ecx, DWORD PTR [rbp-8]
        movsx   rax, ecx
        imul    rax, rax, 715827883
        shr     rax, 32
        mov     edx, eax
        sar     edx, 2
        mov     eax, ecx
        sar     eax, 31
        sub     edx, eax
        mov     eax, edx
        add     eax, eax
        add     eax, edx
        sal     eax, 3
        sub     ecx, eax
        mov     edx, ecx
        movsx   rax, edx
        movzx   eax, BYTE PTR [rbp-400+rax]
        mov     BYTE PTR [rbp-2], al
        mov     ecx, DWORD PTR [rbp-8]
        movsx   rax, ecx
        imul    rax, rax, 715827883
        shr     rax, 32
        mov     edx, eax
        sar     edx, 2
        mov     eax, ecx
        sar     eax, 31
        sub     edx, eax
        mov     eax, edx
        add     eax, eax
        add     eax, edx
        sal     eax, 3
        sub     ecx, eax
        mov     edx, ecx
        mov     eax, edx
        and     eax, 1
        test    eax, eax
        je      .L3
        not     BYTE PTR [rbp-2]
.L3:
        movzx   eax, BYTE PTR [rbp-2]
        xor     BYTE PTR [rbp-1], al
        movzx   eax, BYTE PTR [rbp-1]
        cdqe
        movzx   eax, BYTE PTR [rbp-368+rax]
        mov     BYTE PTR [rbp-1], al
        movzx   eax, BYTE PTR [rbp-1]
        and     eax, 1
        test    eax, eax
        je      .L4
        xor     BYTE PTR [rbp-1], 66
.L4:
        not     BYTE PTR [rbp-1]
        mov     eax, DWORD PTR [rbp-8]
        cdqe
        movzx   eax, BYTE PTR [rbp-464+rax]
        cmp     BYTE PTR [rbp-1], al
        je      .L5
        mov     edi, OFFSET FLAT:.LC2
        mov     eax, 0
        call    printf
        mov     eax, 1
        jmp     .L8
.L5:
        add     DWORD PTR [rbp-8], 1
.L2:
        cmp     DWORD PTR [rbp-8], 49
        jle     .L7
        mov     edi, OFFSET FLAT:.LC3
        mov     eax, 0
        call    printf
        mov     eax, 0
.L8:
        leave
        ret