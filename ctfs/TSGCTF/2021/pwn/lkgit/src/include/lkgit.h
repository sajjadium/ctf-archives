#define LKGIT_HASH_OBJECT         0xdead0001
#define LKGIT_AMEND_MESSAGE       0xdead0003
#define LKGIT_GET_OBJECT          0xdead0004

#define LKGIT_ERR_UNIMPLEMENTED   0xdead1000
#define LKGIT_ERR_OBJECT_NOTFOUND 0xdead1001
#define LKGIT_ERR_UNKNOWN         0xdead1100

#define FILE_MAXSZ                0x40
#define MESSAGE_MAXSZ             0x20
#define HISTORY_MAXSZ             0x30

#define HASH_SIZE                 0x10

typedef struct {
  char hash[HASH_SIZE];
  char *content;
  char *message;
} hash_object;

typedef struct {
  char hash[HASH_SIZE];
  char content[FILE_MAXSZ];
  char message[MESSAGE_MAXSZ];
} log_object;
