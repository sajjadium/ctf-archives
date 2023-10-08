#include"pathlib.h"

void initializePathIterator(PATHITERATOR *iter, char *origPath) {
  iter->start = origPath;
  iter->end = origPath + strlen(origPath);
  iter->cursor = iter->start;
  iter->hasRoot = iter->cursor[0] == '/';
  iter->includeCurDir = ((iter->start < iter->end) && (iter->start[0] == '.') &&
                         (((iter->start + 1) == iter->end) || (iter->start[1] == '/')));
  iter->state = StartDir;
  return;
}

void initializePathIteratorBack(PATHITERATOR *iter, char *origPath) {
  iter->start = origPath;
  iter->end = origPath + strlen(origPath);
  iter->cursor = iter->end;
  iter->hasRoot = iter->cursor[0] == '/';
  iter->includeCurDir = ((iter->start < iter->end) && (iter->start[0] == '.') &&
                         (((iter->start + 1) == iter->end) || (iter->start[1] == '/')));
  iter->state = Body;
  return;
}

void pathIteratorNext(PATHITERATOR *iter, PATHCOMPONENT *c) {
  c->type = None;
  while ((iter->cursor < iter->end) && (iter->state != Done)) {
    switch (iter->state) {
      case StartDir:
        iter->state = Body;
        if (iter->hasRoot) {
          iter->cursor++;
          c->type = RootDir;
          c->start = "/";
          c->length = 1;
          return;
        } else if (iter->includeCurDir) {
          iter->cursor += 2;
          c->type = CurDir;
          return;
        }
        //fallthrough
      case Body:
        if (iter->cursor < iter->end) {
          c->start = iter->cursor;
          size_t length = 0;
          iter->cursor = strchr(iter->cursor, '/');
          if (iter->cursor == NULL) {
            iter->cursor = iter->end;
            c->length = iter->cursor - c->start;
          } else {
            c->length = iter->cursor - c->start;
            iter->cursor++;
          }
          if ((c->length == 0) || ((c->length == 1) && (c->start[0] == '.'))) {
            continue;
          } else if ((c->length == 2) && (!strncmp(c->start, "..", 2))) {
            c->type = ParentDir;
          } else {
            c->type = Normal;
          }
          return;
        } else {
          iter->state = Done;
        }
        break;
      default:
        printError("pathIteratorNext failed");
    }
  }
  return;
}

void pathIteratorNextBack(PATHITERATOR *iter, PATHCOMPONENT *c) {
  c->type = None;
  while ((iter->cursor > iter->start) && (iter->state != Done)) {
    switch (iter->state) {
      case StartDir:
        iter->state = Done;
        if (iter->hasRoot) {
          iter->cursor--;
          c->type = RootDir;
          c->start = "/";
          c->length = 1;
          return;
        } else if (iter->includeCurDir) {
          iter->cursor--;
          c->type = CurDir;
          return;
        }
        return;
      case Body:
        size_t lenBeforeBody = iter->hasRoot ? 1 : iter->includeCurDir ? 2 : 0;
        if ((iter->start + lenBeforeBody) < iter->cursor) {
          char *end = iter->cursor - 1;
          while ((end >= (iter->start + lenBeforeBody)) && *end != '/') {
            end--;
          }
          c->start = end + 1;
          c->length = iter->cursor - c->start;
          iter->cursor = end;
          if ((c->length == 0) || ((c->length == 1) && (c->start[0] == '.'))) {
            continue;
          } else if ((c->length == 2) && (!strncmp(c->start, "..", 2))) {
            c->type = ParentDir;
          } else {
            c->type = Normal;
          }
          return;
        } else {
          iter->state = StartDir;
        }
        break;
      default:
        printError("pathIteratorNextBack failed");
    }
  }
  return; 
}

void pushComponent(ARR *p, PATHCOMPONENT *c) {
  if (c->start[0] == '/') {
    p->cnt = 0;
  } else if ((p->cnt > 0) && (getPath(p, p->cnt - 1) != '/')) {
    pushPath(&p, "/", 1);
  }
  pushPath(&p, c->start, c->length);
  nullTerminatePath(p);
  return;
}

void popComponent(ARR *p) {
  PATHITERATOR iter;
  PATHCOMPONENT c;
  initializePathIteratorBack(&iter, (char*)p->entries);
  pathIteratorNextBack(&iter, &c);
  if (c.type == Normal) {
    popPath(p, c.length);
    if ((p->cnt != 1) || (((char*)p->entries)[0] != '/')) {
      popPath(p, 1);
    }
    nullTerminatePath(p);
  }
  return;
}

char *normalizePath(char *origPath, bool isDir) {
  assert(origPath != NULL);
  ARR *normalized = NULL;
  PATHITERATOR iter;
  PATHCOMPONENT c;
  nullTerminatePath(normalized);
  initializePathIterator(&iter, origPath);
  while ((pathIteratorNext(&iter, &c), (c.type != None))) {
    switch (c.type) {
      case RootDir:
        pushComponent(normalized, &c);
        break;
      case CurDir:
        break;
      case ParentDir:
        popComponent(normalized);
        break;
      case Normal:
        pushComponent(normalized, &c);
        break;
      default:
        printError("normalizePath failed");
    }
  }
  if (isDir && (getPath(normalized, normalized->cnt - 1) != '/')) {
    pushPath(&normalized, "/", 1);
    nullTerminatePath(normalized);
  }
  char *result = (char*)normalized->entries;
  free(normalized);
  return result;
}

char *resolvePath(char *origPath, bool isDir) {
  char *normalizedPath = normalizePath(origPath, isDir);
  if (normalizedPath[0] == '/') {
    return normalizedPath;
  }
  char cwd[PATH_MAX];
  if (getcwd(cwd, PATH_MAX) == NULL) {
    printError("resolvePath failed");
  }
  ARR *resolved = NULL;
  pushPath(&resolved, cwd, strlen(cwd));
  pushPath(&resolved, "/", 1);
  pushPath(&resolved, normalizedPath, strlen(normalizedPath));
  nullTerminatePath(resolved);
  char *result = (char*)resolved->entries;
  free(normalizedPath);
  free(resolved);
  return result;
}
