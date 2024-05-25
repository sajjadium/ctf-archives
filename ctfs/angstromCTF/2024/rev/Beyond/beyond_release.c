#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

float stack[65536];
int sp = 0;

int f2b(float val) { return (isfinite(val) == 0) | ((signbit(val) != 0) << 1); }
float b2f(int val) {
  if (val == 0)
    return 0.0;
  if (val == 1)
    return INFINITY;
  if (val == 2)
    return -0.0;
  if (val == 3)
    return -INFINITY;
}
void c2f(float *out, unsigned char byte) {
  out[3] = b2f(byte & 3);
  out[2] = b2f((byte >> 2) & 3);
  out[1] = b2f((byte >> 4) & 3);
  out[0] = b2f((byte >> 6) & 3);
}

float pop() { return stack[--sp]; }
unsigned char cpop() {
  float f1, f2, f3, f4;
  f1 = pop();
  f2 = pop();
  f3 = pop();
  f4 = pop();
  unsigned char byte =
      f2b(f1) + (f2b(f2) << 2) + (f2b(f3) << 4) + (f2b(f4) << 6);
  return byte;
}
void push(float f) { stack[sp++] = f; }
float vars[256];
int nfs = 0;
char *fnames[256];
char *fdatas[256];

int ins(char **code, char delimit, float args[8]) {
  char opcode = *((*code)++);
  if (opcode == delimit)
    return 1;
  if (isalnum(opcode) && opcode != 'm' && opcode != 'M' && opcode != 'A' &&
      opcode != '0' && opcode != '1') {
    char eq = *((*code)++);
    if (eq != '=') {
      (*code)--;
      if (!isalpha(opcode)) {
        push(args[opcode - '2']);
      } else {
        push(vars[opcode]);
      }
    } else {
      while (!ins(code, ';', args))
        ;
      vars[opcode] = pop();
    }
    return 0;
  }
  if (opcode == ':') {
    int funcid = nfs++;
    fnames[funcid] = *code;
    while (**code != ':') {
      (*code)++;
    }
    **code = 0;
    (*code)++;
    fdatas[funcid] = *code;
    int nest = 1;
    while (nest) {
      char ch = *((*code)++);
      if (ch == '=')
        nest++;
      if (ch == ';')
        nest--;
    }
    return 0;
  }
  if (opcode == '^') {
    for (int i = 0; i < nfs; i++) {
      if (strstr(*code, fnames[i]) == *code) {
        char *fcode = fdatas[i];
        float newargs[8];
        for (int j = 0; j < 8; j++) {
          if (j < sp) {
            newargs[j] = stack[sp - j - 1];
          }
        }
        while (!ins(&fcode, ';', newargs))
          ;
        *code += strlen(fnames[i]);
        return 0;
      }
    }
  }
  switch (opcode) {
  case '+':
    push(pop() + pop());
    break;
  case '-':
    push(pop() - pop());
    break;
  case '*':
    push(pop() * pop());
    break;
  case '/':
    push(pop() / pop());
    break;
  case 'm':
    push(fmin(pop(), pop()));
    break;
  case 'M':
    push(fmax(pop(), pop()));
    break;
  case '0':
    push(0);
    break;
  case '1':
    push(INFINITY);
    break;
  case '\'':
    push(1 / (pop()));
    break;
  case '!':
    push(-pop());
    break;
  case '.':
    pop();
    break;
  }
  return 0;
}
char code[] =
    ":i:...033**03'3'**m4-3'1!M3'1m-31!M31m-+'2-m;"
    ":n00:'1-;:n10:'1+;:n01:1-;:n11:1+;"
    ":g1:..10*2^n103^n10m1^i2^n103^n11m1^i2^n113^n10m1^i2^n013^n01m0!^"
    "i2^n113^n01m0!^i2^n013^n11m0!^i2^n113^n11m0^i1!M;"
    ":g2:^g1'!;"
    ":g3:..2'!3'!^g1;"
    ":g4:..23^g323^g1^g2;"
    ":x1:^g4^g4;"
    ":x2:...23^g44^g223^g2^g3;"
    ":sg:.021+2'1++1^i;"
    ":x3:...22*33*4^x1;"
    ":x4:...02^sg3^sg22*33*4^x2^x10*0!^i;"
    ":x5:...2^sg3^sg22*33*4^x2^x2;"
    ":x6:...432^x3432^x4^g3;"
    ":xb:........026^x537^x548^x559^x6026^x537^x548^x6026^"
    "x537^x6026^x6;"
    ":gb4:........59^g448^g437^g426^g4;:gb2:........59^g248^g237^g226^"
    "g2;:gb3:........59^g348^g337^g326^g3;"
    ":nb:23451!1!1!1!^gb40001^xb;:o1r:.12^n000^i;:fnz:.1!20^i1!20^i1!20^"
    "i1!20^i;:ftz:^g3^g3^g3^o1r^n01^fnz;:l:........9876^ftz5432^gb2^"
    "gb398761!1!1!1!^xb;:al:....0000543210!1!1^l1!1!1!1^l100!1!^l11!0!0^"
    "l10!11^l1!0!01^l0!1!1!1^l110!0^l0!0!11!^l011!0!^l1!10!0^l0!000!^"
    "l00!01!^l0011!^l00!00!^l1!0!1!1^l1000^l0!0!1!1!^l0!1!0!0!^l1!01!1!"
    "^l10!0!0!^l00!11!^l0!11!1!^l11!11!^l0!0!1!1^l1!00!1!^l00!1!1^l0!0!"
    "0!1!^l111!1!^l00!1!0!^l0!00!0!^l00!10!^l1!000!^l11!0!1^l1!101!^"
    "l00!0!1^l1!0!0!1!^l0!101^l100!0!^l0!10!0^l00!10^l1!100!^l1011!^"
    "l1!010!^l11!1!0!^l0!00!0^l010!0^l011!1^l1!1!01!^l0000!^l0101!^l0!"
    "010!^l01!01!^l1!1!1!0^l101!0^l0!110!^l0!11!0^l1010^l010!0!^l0!01!"
    "0^l1!1!11!^l0!0!01!^l0!11!1^l0!011^l110!1^l000!0!^l01!1!0!^l0!0!1!"
    "0^l1!01!0!^l01!0!0!^l1!100^l1!0!00!^l0!1!0!0^l0!11!0!^l1010!^"
    "l0000^l01!0!1!^l101!0!^l1!1!0!0!^l1!111^l00!1!0^l000!1!^l0!1!11^"
    "l0!00!1!^l1!0!00^l0!011!^l11!01!^l01!1!1^l11!01^l001!1^l00!11^"
    "l10!1!1!^l10!1!0^l01!1!0^l10!0!1^l101!1^l11!11^l0!01!1!^l0!10!0!^"
    "l1!011^l10!0!1!^l01!11^l0!001!^l1!0!1!0!^l1!110^l0001^l1111!^l10!"
    "01^l00!0!0!^l0!00!1^l1!00!0!^l0!1!0!1!^l0100^l1!01!0^l0!100^l0!1!"
    "10!^l1!00!1^l1101^l101!1!^l11!00^l1!1!00^l1101!^l0!111!^l011!1!^"
    "l0!1!11!^l011!0^l0!1!0!1^l0!01!0!^l0!0!00!^l1110!^l1!0!1!0^l1110^"
    "l00!00^l0!1!00!^l1!111!^l01!00^l1!1!10!^l10!00^l11!00!^l0111!^l1!"
    "010^l1!10!1^l0!000^l10!10^l0!0!11^l000!0^l11!1!0^l0111^l0!010^"
    "l10!00!^l11!0!1!^l1!000^l0100!^l1!001^l1000!^l10!11!^l1!1!00!^l0!"
    "1!10^l01!10^l0!0!01^l010!1!^l1!1!10^l1100!^l1!11!1!^l01!1!1!^l0!0!"
    "00^l1!0!0!1^l0!001^l0!1!01^l00!0!1!^l11!10!^l1!011!^l10!01!^l1!1!"
    "1!0!^l00!01^l00!0!0^l1!0!01!^l11!10^l1!0!11!^l1!110!^l0!1!1!0^l0!"
    "1!1!1!^l0!10!1^l11!1!1^l0010^l000!1^l1001!^l0!0!10!^l1!10!0!^l10!"
    "10!^l111!0!^l0!111^l0!101!^l0!0!1!0!^l01!01^l1!1!0!1^l11!0!0!^l01!"
    "0!1^l1001^l1!11!0^l1!0!10!^l1!11!1^l01!00!^l100!1^l0!0!0!1^l110!1!"
    "^l01!10!^l10!1!0!^l111!1^l111!0^l10!0!0^l0!0!10^l0010!^l0!110^l1!"
    "10!1!^l1!1!1!1!^l1!0!0!0^l001!0!^l1011^l100!0^l0!100!^l1!1!11^"
    "l0011^l0110^l0!1!00^l0!10!1!^l001!1!^l00!1!1!^l0001!^l1!1!01^l0!"
    "1!01!^l1!1!0!1!^l0110!^l0!01!1^l1!0!0!0!^l001!0^l01!0!0^l1!11!0!^"
    "l010!1^l1!0!11^l1!01!1^l1100^l1!101^l11!1!1!^l0!0!0!0^l0!0!0!0!^"
    "l1!1!0!0^l1!00!0^l0101^l1!0!1!1!^l0!1!1!0!^l1!0!10^l1!001!^l1111^"
    "l110!0!^l01!11!^l....;;";
char algo[] = "aqpb2345^xbhijg6789^xbfeno5432^xbcdlk9876^xbabcd"
              "6789^gb42345nopq^gb4^xbijkl2345^gb4efgh6789^gb4^xb2345^"
              "al;";

int encrypt_byte(char *flagbyte, unsigned int chain, int idx,
                 unsigned char *cs) {
  float inargs[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  c2f(inargs + 4, *flagbyte);
  c2f(inargs, *(flagbyte + 1));
  float temp[4];
  char vname = 'a';
  for (int i = 0; i < 4; i++) {
    c2f(temp, chain & 0xff);
    for (int j = 0; j < 4; j++) {
      vars[vname++] = temp[j];
      if (vname == 'm')
        vname++;
    }
    chain >>= 8;
  }

  char *codep = algo;

  while (!ins(&codep, ';', inargs))
    ;
  *cs = cpop();
  *(flagbyte + 1) = cpop();
  *(flagbyte) = cpop();
  chain = cpop();
  chain = (chain << 8) | cpop();
  chain = (chain << 8) | cpop();
  chain = (chain << 8) | cpop();
  return chain;
}

int main() {
  char *codep = code;
  float inargs[8];
  while (!ins(&codep, ';', inargs))
    ;

  char flag[] = "***REDACTED***";
  int chainstart = 0x5f3759df;
  int flag_len = strlen(flag) + 1;
  unsigned char *chksum = malloc(flag_len >> 1);
  for (int i = 0; i < (flag_len >> 1); i++) {
    chainstart = encrypt_byte(flag + (i << 1), chainstart, i << 1, &chksum[i]);
  }
  for (int i = 0; i < flag_len; i++) {
    printf("%02x", (unsigned char)flag[i]);
  }
  for (int i = 0; i < (flag_len >> 1); i++) {
    printf("%02x", chksum[i]);
  }
  // Encrypted flag:
  // fa8c3453029e0e236800c26cc9d1748d
  // de9e98c1e24804cb9602b68a4fd424fc
  // 7d7dca9fb3b4f6102ce5d3fb70cf4af0
  // d1204c1df031fb0ec583c5108fca9790
  // 4d35b6b60183cac9b6183e4e4dc94d4d
  // 8fc9356d
  // good luck!
  printf("\n");
}