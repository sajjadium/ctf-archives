#include "sqlite3.h"
#include <stdio.h>

#define MAX_STATEMENTS 10

void prepare(sqlite3 *db, sqlite3_stmt **stmt) {
  if(*stmt != NULL) {
    printf("There is already a prepared statement at this location.\n");
    return;
  }

  char *sql = NULL;
  size_t sql_size = 0;

  printf("Please enter your SQL query in a single line:\n");
  if(getline(&sql, &sql_size, stdin) != -1) {
    if(sqlite3_prepare_v2(db, sql, -1, stmt, NULL) == SQLITE_OK &&
        *stmt != NULL) {
      printf("Done.\n");
    } else {
      printf("Could not prepare SQL.\n");
    }
  } else {
    printf("Could not read SQL.\n");
  }
}

void execute(sqlite3 *db, sqlite3_stmt *stmt) {
  if(stmt == NULL) {
    printf("There is no prepared statement at this location.\n");
    return;
  }

  sqlite3_reset(stmt);

  while(sqlite3_step(stmt) != SQLITE_DONE) {
    int cols = sqlite3_column_count(stmt);

    for(size_t i = 0; i < cols; i++) {
      switch (sqlite3_column_type(stmt, i)) {
        case SQLITE3_TEXT:
          printf("%s ", sqlite3_column_text(stmt, i));
          break;
        case SQLITE_INTEGER:
          printf("%lld ", sqlite3_column_int64(stmt, i));
          break;
        case SQLITE_FLOAT:
          printf("%g ", sqlite3_column_double(stmt, i));
          break;
        case SQLITE_BLOB:
          printf("(blob) ");
          break;
        case SQLITE_NULL:
          printf("NULL ");
        default:
          break;
      }
    }
    printf("\n");
  }
}

void delete(sqlite3_stmt **stmt) {
  if(*stmt == NULL) {
    printf("There is no prepared statement at this location.\n");
    return;
  }

  sqlite3_finalize(*stmt);
  *stmt = NULL;
}

void inscribe(sqlite3_stmt **stmt) {
  if(*stmt == NULL) {
    printf("There is no prepared statement at this location.\n");
    return;
  }

  int amount = *(int *)((void *)*stmt + 0x90);
  unsigned char *tome = *(unsigned char **)((void *)*stmt + 0x88);

  printf("How many characters will you inscribe (up to %d)? ", amount * 24);
  int actual = 0;
  scanf("%d", &actual);
  getchar();
  if(actual <= 0 || actual > amount * 24) {
    printf("Invalid amount.\n");
    return;
  }
  printf("Inscribe your message: ");
  for (size_t i = 0; i < actual; i++) {
    *tome = getchar();
    ++tome;
  }
  printf("\nIt has been done.\n");
}

size_t get_index() {
  size_t choice = 0;
  printf("What index (1-10)? ");
  scanf("%zu", &choice);
  getchar();

  if(choice > 10) {
    printf("Invalid index specified.\n");
    return 0;
  }

  return choice;
}

int main(void) {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  sqlite3 *db = NULL;
  sqlite3_stmt *stmt[MAX_STATEMENTS] = {0};

  if(sqlite3_open_v2("user.db", &db, SQLITE_OPEN_READWRITE | SQLITE_OPEN_MEMORY, NULL) != SQLITE_OK
    || db == NULL) {
    printf("Failed to open database! (Report to admin if this happens on remote)\n");
    return -1;
  }

  printf("Welcome to my SQLite3 demo program!\n\
Make a choice:\n\
\n\
1. Add a SQL query.\n\
2. Execute a SQL query.\n\
3. Delete a SQL query.\n\
4. Exit\n");

  int exit = 1;
  while(exit) {
    size_t choice = 0;
    size_t index = 0;
    printf("Choice: ");
    scanf("%zu", &choice);
    getchar();

    switch (choice) {
      case 1:
        index = get_index();
        prepare(db, &stmt[index]);
        break;
      case 2:
        index = get_index();
        execute(db, stmt[index]);
        break;
      case 3:
        index = get_index();
        delete(&stmt[index]);
        break;
      case 5:
        index = get_index();
        inscribe(&stmt[index]);
        break;
      case 4:
        printf("Bye!\n");
        exit = 0;
        break;
      default:
        printf("I don't know what that means.\n");
        break;
    }
  }

  sqlite3_close(db);

  return 0;
}
