#ifndef __BABYAUTH_UTILS__
#define __BABYAUTH_UTILS__

void fatal(const char *msg);
void rndstr(unsigned char *name, int len);
int fscmp(const char *authdir, const char *filename, const char *data);
void sandboxify(void);

#endif
