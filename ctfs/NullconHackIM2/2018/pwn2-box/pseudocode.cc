void handler()
{
    getpid();
    exit(1);
}

int64_t func_1(unsigned int a1)
{
    return a1;
}

ssize_t func_2(int a1)
{
    ssize_t result; // rax
    int buf; // [rsp+1Ch] [rbp-74h]
    char s; // [rsp+20h] [rbp-70h]

    buf = 0;
    result = read(a1, &buf, 4uLL);
    if ( result > 0 )
    {
        memset(&s, 0, 0x64uLL);
        result = read(a1, &s, buf);
    }
    return result;
}

int64_t func_3(unsigned int a1, char a2)
{
    int64_t result; // rax

    result = (unsigned int)a2;
    switch ( (int)result )
    {
    case 1:
        func_1(a2);
        goto LABEL_3;
    case 2:
LABEL_3:
        func_1(a2);
        goto LABEL_4;
    case 3:
LABEL_4:
        func_1(a2);
        goto LABEL_5;
    case 4:
LABEL_5:
        func_1(a2);
        goto LABEL_6;
    case 5:
LABEL_6:
        result = func_1(a2);
        break;
    case 0xA:
        result = func_2(a1);
        break;
    default:
        return result;
    }
    return result;
}

void func_4(unsigned int a1)
{
    char buf; // [rsp+17h] [rbp-9h]
    int v2; // [rsp+18h] [rbp-8h]
    int v3; // [rsp+1Ch] [rbp-4h]

    v3 = 0;
    while ( ++v3 )
    {
        v2 = read(a1, &buf, 1uLL);
        if ( v2 <= 0 )
            break;
        func_3(a1, buf);
    }
}

int64_t main(int64_t a1, char **a2, char **a3)
{
    int64_t v3; // rsi
    int64_t v4; // rdi
    int pipedes[2]; // [rsp+10h] [rbp-30h]
    int buf; // [rsp+1Ch] [rbp-24h]
    void *v8; // [rsp+20h] [rbp-20h]
    int64_t v9; // [rsp+28h] [rbp-18h]
    char *v10; // [rsp+30h] [rbp-10h]
    int v11; // [rsp+38h] [rbp-8h]
    int v12; // [rsp+3Ch] [rbp-4h]

    v11 = pipe(pipedes);
    if ( v11 )
        __assert_fail("ret == 0", "sandbox.c", 0x75u, "main");
    if ( !fork() )
    {
        getpid();
        signal(14, handler);
        alarm(5u);
        func_4(pipedes[0]);
        exit(0);
    }
    signal(17, 1);
    signal(11, handler);
    signal(5, handler);
    signal(14, handler);
    alarm(5u);
    buf = 0;
    if ( read(0, &buf, 4uLL) > 0 && buf <= 0x100000 )
    {
        v3 = buf;
        v10 = (char *)mmap(0LL, buf, 7, 34, -1, 0LL);
        if ( !v10 )
            __assert_fail("psc != NULL", "sandbox.c", 0x94u, "main");
        v12 = 0;
        while ( buf )
        {
            v3 = (int64_t)&v10[v12];
            v11 = read(0, (void *)v3, buf);
            if ( v11 < 0 )
                break;
            v12 += v11;
            buf -= v11;
        }
        if ( !buf )
        {
            v9 = seccomp_init(0LL, v3);
            if ( v9 )
            {
                v11 = seccomp_rule_add(v9, 2147418112LL, 1LL, 0LL);
                if ( v11 >= 0 )
                {
                    v11 = seccomp_rule_add(v9, 2147418112LL, 60LL, 0LL);
                    if ( v11 >= 0 )
                    {
                        v11 = seccomp_rule_add(v9, 2147418112LL, 231LL, 0LL);
                        if ( v11 >= 0 )
                        {
                            v4 = v9;
                            v11 = seccomp_load(v9);
                            if ( v11 >= 0 )
                            {
                                v8 = v10;
                                ((void (*)(int64_t, int64_t))v10)(v4, 2147418112LL);
                            }
                        }
                    }
                }
            }
        }
    }
    perror("error");
    return 0LL;
}
