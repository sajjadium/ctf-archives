#ifndef __BABYAUTH_AUTH__
#define __BABYAUTH_AUTH__

#include "ipc.h"

typedef int  (*AUTH_VALIDATOR)(const char*, IPC*);
typedef void (*AUTH_READER)(IPC*);

int  username_validator(const char *authdir, IPC *ipc);
void username_reader(IPC *ipc);
int  password_validator(const char *authdir, IPC *ipc);
void password_reader(IPC *ipc);
int  token_validator(const char *authdir, IPC *ipc);
void token_reader(IPC *ipc);

int authenticator(const char *authdir,
                  AUTH_VALIDATOR validator, AUTH_READER reader);

#endif
