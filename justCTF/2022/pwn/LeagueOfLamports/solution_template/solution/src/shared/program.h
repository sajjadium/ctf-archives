typedef struct {
  uint16_t idx;
  uint16_t amt;
} deposit_args;

typedef struct {
  uint16_t idx;
  uint16_t amt;
  uint8_t bump;
} withdraw_args;

typedef struct {
  uint64_t lamports;
  uint64_t space;
  SolPubkey owner;
} create_account_sys;

typedef struct {
  uint64_t lamports;
} transfer_amount_sys;

#define CREATE_ACCOUNT 0
#define TRANSFER 2
