#include"guardian.h"

__attribute__((constructor))
void setupSanbox(int argc, char **argv, char **envp) {
  char *value;
  bool mustReset = false;
  ARR *newEnviron = NULL;
  if (getenv("LD_BIND_NOW") != NULL) {
    printError("setup failed");
  }
  if (((value = getenv("LD_BIND_NOT")) == NULL) || strcmp(value, "1")) {
    char *holder = "LD_BIND_NOT=1";
    addString(&newEnviron, &holder);
    mustReset = true;
  }
  if (((value = getenv("LD_AUDIT")) == NULL) || strcmp(value, LIBGUARDIAN)) {
    char *holder = "LD_AUDIT=" LIBGUARDIAN;
    addString(&newEnviron, &holder);
    mustReset = true;
  }
  if (mustReset) {
    if ((setresuid(getuid(), getuid(), getuid()) == -1) ||
        (setresgid(getgid(), getgid(), getgid()) == -1)) {
      printError("setup failed");
    }
    for (; *envp != NULL; envp++) {
      if (strncmp(*envp, "LD_BIND_NOT=", 12) && strncmp(*envp, "LD_AUDIT=", 9)) {
        addString(&newEnviron, envp);
      }
    }
    char *holder = NULL;
    addString(&newEnviron, &holder);
    if (execve((char*)getauxval(AT_EXECFN), argv, (char**)newEnviron->entries) == -1 ) {
      printError("setup failed");
    }
  }
}

unsigned int la_version(unsigned int version) {
  return version;
}

/*
 * Filter loadable libraries
 */
char *la_objsearch(const char *name, uintptr_t *cookie, unsigned int flag) {
  DEBUGPRINTF("objsearch :\t%s\n", name);
  for (char **whitelistEntry = WHITELISTLIB; *whitelistEntry != NULL; whitelistEntry++) {
    char *start = strrchr(*whitelistEntry, '/');
    if ((start != NULL) && (!strcmp(start+1, name))) {
      return (char*)name;
    } else if (!strcmp(*whitelistEntry, name)) {
      return (char*)name;
    }
  }
  return NULL;
}

/*
 * Enable tracing of all loaded libraries
 */
unsigned int la_objopen(struct link_map *map, Lmid_t lmid, uintptr_t *cookie) {
  DEBUGPRINTF("objopen :\t%s %p\n", map->l_name, cookie);
  LIBENTRY newEntry = {
    .cookie = cookie,
    .libname = map->l_name
  };
  getLock(&LOADEDLIBLOCK);
  addLib(&LOADEDLIB, &newEntry);
  dropLock(&LOADEDLIBLOCK);
  return LA_FLG_BINDTO | LA_FLG_BINDFROM;
}

/*
 * Perform checks for critical functions
 */
Elf64_Addr la_x86_64_gnu_pltenter(
  Elf64_Sym *sym,
  unsigned int ndx,
  uintptr_t *refcook,
  uintptr_t *defcook,
  La_x86_64_regs *regs,
  unsigned int *flags,
  const char *symname,
  long *framesizep
) {
  LIBENTRY targetEntry = {
    .cookie = refcook,
    .libname = NULL,
  };
  getLock(&LOADEDLIBLOCK);
  LIBENTRY *foundEntry = searchLib(LOADEDLIB, &targetEntry);
  dropLock(&LOADEDLIBLOCK);
  if (foundEntry == NULL) {
    printError("pltenter failed");
  }
  if (foundEntry->libname[0] != '\x00') {
    // We don't really care about libraries calling each other,
    // Since loading a malicious library would be game over anyway
    return sym->st_value;
  }
  // Reaching here means we're calling from the executable
  // Filters are designed to allow minimal set of functions required by bash / ls / cat
  // Other dangerous functions that are not used / seldom used are blocked below 
  if (!strcmp(symname, "execve")) {
    DEBUGPRINTF("pltenter exe : %s\n", symname);
    for (char **exe = WHITELISTEXE; *exe != NULL; exe++) {
      if (!strcmp((char*)regs->lr_rdi, *exe)) {
        // This is a slight abuse of framesize field. Since we have to filter envp here
        // The easiest way is to reconstruct the entire env array, but that would require
        // some memory allocations, and would lead to mem leak if execve fails. The way to
        // handle this is do some cleanup in pltexit, which would only be called if framesize
        // is set to value != -1
        *framesizep = 0;
        ARR *newEnviron = NULL;
        if (regs->lr_rdx != 0) {
          char **origEnv = (char**)regs->lr_rdx;
          char *ldDebug = NULL;
          char *ldDebugOutput = NULL;
          char *ldProfile = NULL;
          char *ldProfileOutput = NULL;
          for (char **origEnv = (char**)regs->lr_rdx; *origEnv != NULL; origEnv++) {
            if (!strncmp(*origEnv, "LD_DEBUG=", 9)) {
              ldDebug = *origEnv;
            } else if (!strncmp(*origEnv, "LD_DEBUG_OUTPUT=", 16)) {
              ldDebugOutput = *origEnv;
            } else if (!strncmp(*origEnv, "LD_PROFILE=", 11)) {
              ldProfile = *origEnv;
            } else if (!strncmp(*origEnv, "LD_PROFILE_OUTPUT=", 18)) {
              ldProfileOutput = *origEnv;
            } else if (strncmp(*origEnv, "LD_AUDIT=", 9) &&
                       strncmp(*origEnv, "LD_LIBRARY_PATH=", 16) &&
                       strncmp(*origEnv, "LD_BIND_NOT=", 12) &&
                       strncmp(*origEnv, "LD_BIND_NOW=", 12)) {
              // LD_AUDIT / LD_LIBRARY_PATH could bypass the library load check, block here 
              addString(&newEnviron, origEnv);
            }
          }
          if ((ldDebug != NULL) && (ldDebugOutput != NULL)) {
            // Allow debugging with LD_DEBUG, but must check write path
            char *resolvedPath = resolvePath(&ldDebugOutput[16], false);
            if (!strncmp(resolvedPath, "/tmp/", 5)) {
              addString(&newEnviron, &ldDebug);
              addString(&newEnviron, &ldDebugOutput);
            }
            free(resolvedPath);
          }
          if ((ldProfile != NULL) && (ldProfileOutput != NULL)) {
            // Allow profiling with LD_PROFILE, but must check write path
            char *resolvedPath = resolvePath(&ldProfileOutput[18], true);
            if (!strncmp(resolvedPath, "/tmp/", 5)) {
              addString(&newEnviron, &ldProfile);
              addString(&newEnviron, &ldProfileOutput);
            }
            free(resolvedPath);
          }
        }
        char *holder = "LD_AUDIT="LIBGUARDIAN;
        addString(&newEnviron, &holder);
        holder = "LD_BIND_NOT=1";
        addString(&newEnviron, &holder);
        holder = NULL;
        addString(&newEnviron, &holder);
        regs->lr_rdx = (unsigned long long int)newEnviron->entries;
        free(newEnviron);
        return sym->st_value;
      }
    }
    return (Elf64_Addr)intFail;
  } else if (!strcmp(symname, "open")) {
    DEBUGPRINTF("pltenter exe : %s\n", symname);
    char *resolvedPath = resolvePath((char*)regs->lr_rdi, ((char*)regs->lr_rdi)[strlen((char*)regs->lr_rdi) - 1] == '/');
    if (!strncmp("/tmp/", resolvedPath, 5)) {
      *framesizep = 0;
      regs->lr_rdi = (unsigned long long int)resolvedPath;
      return sym->st_value;
    } else {
      return (Elf64_Addr)intFail;
    }
  } else if (!strcmp(symname, "opendir")) {
    DEBUGPRINTF("pltenter exe : %s\n", symname);
    return sym->st_value;
  } else if (strstr(symname, "exec")     || strstr(symname, "system")  || strstr(symname, "wordexp")  ||
             strstr(symname, "spawn")    || strstr(symname, "open")    || strstr(symname, "link")     ||
             strstr(symname, "creat")    || strstr(symname, "chown")   || strstr(symname, "chmod")    ||
             strstr(symname, "mkdir")    || strstr(symname, "rmdir")   || strstr(symname, "mknod")    ||
             strstr(symname, "mkstemp")  || strstr(symname, "mkdtemp") || strstr(symname, "truncate") ||
             strstr(symname, "mkfifo")   || strstr(symname, "connect") || strstr(symname, "tmpfile")  ||
             strstr(symname, "mkostemp") || strstr(symname, "rename")  || strstr(symname, "kill")) {
    // To avoid unrelated fluff / reduce code complexity, I'm just gonna block all these functions
    // some functions might cause issues for certain /bin/bash functions, but doesn't affect challenge solvability
    DEBUGPRINTF("pltenter exe : %s\n", symname);
    printError("sanitizeFunction failed");
  }
  // Safe functions are allowed
  return sym->st_value;
}

/*
 * Cleanup after pltenter
 */
unsigned int la_x86_64_gnu_pltexit(
  Elf64_Sym *sym,
  unsigned int ndx,
  uintptr_t *refcook,
  uintptr_t *defcook,
  const La_x86_64_regs *inregs,
  La_x86_64_retval *outregs,
  const char *symname
) {
  if (!strcmp(symname, "execve")) {
    free((char**)inregs->lr_rdx);
  } else if (!strcmp(symname, "open")) {
    free((char*)inregs->lr_rdi);
  } else {
    printError("pltexit failed");
  }
  return 0;
}


int intFail() {
  return -1;
}

void libEntryCopy(void *dst, void *src, size_t cnt) {
  assert(cnt == 1);
  ((LIBENTRY*)dst)->cookie = ((LIBENTRY*)src)->cookie;
  ((LIBENTRY*)dst)->libname = strdup(((LIBENTRY*)src)->libname);
  if (((LIBENTRY*)dst)->libname == NULL) {
    printError("libEntryCopy failed");
  }
  return;
}

bool libEntryEq(void *e1, void *e2) {
  return ((LIBENTRY*)e1)->cookie == ((LIBENTRY*)e2)->cookie;
}

void charPointerCopy(void *dst, void *src, size_t cnt) {
  assert(cnt == 1);
  *(char**)dst = *(char**)src;
  return;
}
