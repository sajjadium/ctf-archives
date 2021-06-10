unsigned __int64 __fastcall sub_28FE(__int64 a1)
{
  size_t v1; // rax
  __int64 v2; // rax
  __int64 v3; // rax
  __int64 v4; // rax
  const char *v5; // rsi
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  char v10; // [rsp+1Dh] [rbp-A3h]
  char v11; // [rsp+1Eh] [rbp-A2h]
  char v12; // [rsp+1Fh] [rbp-A1h]
  unsigned __int8 v13; // [rsp+20h] [rbp-A0h]
  unsigned __int8 v14; // [rsp+21h] [rbp-9Fh]
  int i; // [rsp+28h] [rbp-98h]
  int v16; // [rsp+2Ch] [rbp-94h]
  __int64 j; // [rsp+30h] [rbp-90h]
  __int64 v18; // [rsp+40h] [rbp-80h]
  __int64 v19; // [rsp+50h] [rbp-70h]
  char *dest; // [rsp+58h] [rbp-68h]
  char v21; // [rsp+60h] [rbp-60h]
  char v22; // [rsp+80h] [rbp-40h]
  unsigned __int64 v23; // [rsp+A8h] [rbp-18h]

  v23 = __readfsqword(0x28u);
  printf("Before I start cooking your pizzas, do you have anything to declare? Please explain: ");
  read_string((__int64)byte_20C480, 300);
  v1 = strlen(byte_20C480);
  *(_QWORD *)(a1 + 32) = malloc(v1 + 1);
  strcpy(*(char **)(a1 + 32), byte_20C480);
  v16 = sub_339C(a1 + 8, byte_20C480);
  v13 = 0;
  v14 = 0;
  dest = (char *)malloc(0x190uLL);
  for ( i = 0; i < v16; ++i )
  {
    printf("-------- COOKING PIZZA #%d --------\n", (unsigned int)(i + 1));
    v2 = sub_33D4(a1 + 8, i);
    sub_33FE(&v21, v2);
    *dest = 0;
    for ( j = sub_34C0(&v21); ; sub_3590(&j) )
    {
      v18 = sub_3508(&v21);
      if ( !(unsigned __int8)sub_3554(&j, &v18) )
        break;
      v3 = sub_35B0(&j);
      std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v22, v3);
      v4 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::c_str(&v22);
      printf("Adding ingredient: %s\n", v4);
      v5 = (const char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::c_str(&v22);
      strcat(dest, v5);
      std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v22, v5);
    }
    if ( sub_35C2(&v21) == 0 )
    {
      puts("This pizza has no ingredients. Not valid");
    }
    else
    {
      v14 = 16 * (((v14 >> 4) + 1) & 0xF) | v14 & 0xF;
      v10 = 0;
      v11 = 0;
      v12 = 0;
      if ( strstr(dest, &byte_75E1) )
        v10 = 1;
      else
        v11 = 1;
      if ( strstr(dest, &needle) )
      {
        v12 = 1;
      }
      else if ( strstr(dest, &byte_75E6) || strstr(dest, &byte_75EB) || strstr(dest, &byte_75F0) )
      {
        v11 = 1;
      }
      if ( v11 || v12 )
        v10 = 0;
      if ( v10 )
        v13 = ((v13 & 0xF) + 1) & 0xF | v13 & 0xF0;
      if ( v11 )
        v13 = 16 * (((v13 >> 4) + 1) & 0xF) | v13 & 0xF;
      if ( v12 )
        v14 = ((v14 & 0xF) + 1) & 0xF | v14 & 0xF0;
      if ( v10 )
      {
        v6 = operator new(0x38uLL);
        sub_2546(v6, dest);
        v19 = v6;
      }
      else if ( v11 )
      {
        v7 = operator new(0x38uLL);
        sub_257E(v7, dest);
        v19 = v7;
      }
      else
      {
        if ( !v12 )
          _assert_fail("false", "customer.h", 0xB5u, "void Customer::cook_pizzas()");
        v8 = operator new(0x38uLL);
        sub_25B6(v8, dest);
        v19 = v8;
      }
      puts("Cooked new pizza:");
      (*(void (__fastcall **)(__int64))(*(_QWORD *)v19 + 8LL))(v19);
      if ( v12 )
      {
        printf("HOW IS IT POSSIBLE??? %s here?? How could this order get here? this pizza is criminal.\n", &needle);
        printf("And this is the only thing you could say about your order: %s\n", *(_QWORD *)(a1 + 32));
        puts("are you serious?");
        is_upset = (_QWORD *)a1;
      }
      sub_35E8(a1 + 40, &v19);
    }
    sub_323E(&v21);
  }
  if ( v14 & 0xF0 )
  {
    if ( v14 >> 4 == (v13 & 0xF) )
    {
      puts("Molto bene, all cooked!");
      if ( !(v14 & 0xF) )
        free(*(void **)(a1 + 32));
    }
    else
    {
      puts("found non-approved pizzas. come on.");
    }
  }
  else
  {
    puts("found no valid pizzas. You losing my time fratello.");
  }
  return __readfsqword(0x28u) ^ v23;

