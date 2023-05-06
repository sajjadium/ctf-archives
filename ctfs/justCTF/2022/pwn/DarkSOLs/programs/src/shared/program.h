#define CREATE_ACCOUNT 0
#define INITIALIZE_ACCOUNT 1
#define TRANSFER 2
#define MINT_TO 7
#define TRANSFER_TOKEN_CHECKED 12

#define AUTHORITY_SEED_INIT 4
#define SANITY_SEED_INIT 5
#define WEAPON_SEED_INIT 6

#define VAULT_SEED 4
#define AUTHORITY_SEED 5
#define ITEM_TOKEN_SEED 7
#define ITEM_1337_TOKEN_SEED 8

#define MINIMUM_BALANCE 2039814

typedef struct {
  uint8_t vault_seed;
  uint8_t authority_seed;
  uint8_t player_seed;
  uint8_t solve_item_seed;
  uint8_t solve_item_1337_seed;
  uint8_t name[31];
} CreatePlayerInstr;

typedef struct {
  uint8_t vault_seed;
  uint8_t authority_seed;
  uint8_t amount;
} BuyInstr;

typedef struct {
  uint8_t vault_seed;
  uint8_t authority_seed;
  uint8_t amount;
} SellInstr;

typedef struct {
  uint8_t vault_seed;
  uint8_t number;
  uint8_t monster;
} FightInstr;

typedef struct {
  uint64_t lamports;
  uint64_t space;
  SolPubkey owner;
} create_account_sys;

typedef struct {
  uint64_t amount;
} transfer_generic;

typedef struct {
  uint64_t amount;
  uint8_t decimals;
} transfer_checked;

typedef struct {
  SolPubkey token;
} Sanity;

typedef enum {
  INITIALIZE,
  SELL,
  BUY,
  CREATE_PLAYER,
  FIGHT
} Op;

typedef enum {
  Uninitialized,
  Initialized,
  Frozen
} AccountState;

typedef struct {
  SolPubkey mint;
  SolPubkey owner;
  uint64_t amount;
  SolPubkey delegate;
  AccountState state;
  uint64_t is_native;
  uint64_t delegated_amount;
  SolPubkey close_authority;
} Account;

typedef struct {
  SolPubkey mint_authority;
  uint64_t supply;
  uint8_t type;
  uint8_t is_initialized;
  SolPubkey freeze_authority;
} Mint;

typedef struct {
  uint8_t health;
  uint8_t mana;
  char name[30];
} Player;

typedef struct {
  SolPubkey mint;
  uint16_t attack;
  uint16_t price;
} Weapon;

typedef struct {
  Weapon weapons[2];
} Weapons;

typedef struct {
  uint16_t attack;
  uint16_t reward;
} Monster;

void create_account(
  SolParameters* params,
  SolAccountInfo* payer,
  SolAccountInfo* acct,
  const SolPubkey* owner,
  uint8_t* seed,
  uint8_t seed_len,
  uint64_t space,
  uint64_t lamports
) {
  SolAccountInfo* system_program = &params->ka[1];

  const SolSignerSeed seeds[] = {{ .addr = seed, .len = seed_len }};
  const SolSignerSeeds signers_seeds[] = {{ .addr = seeds, .len = SOL_ARRAY_SIZE(seeds) }};

  SolAccountMeta arguments[] = {
    { .pubkey = payer->key, .is_writable = true, .is_signer = true },
    { .pubkey = acct->key, .is_writable = true, .is_signer = true },
  };
  uint8_t data[4 + sizeof(create_account_sys)];
  sol_memset(data, 0, sizeof(data));
  *(uint32_t *)data = CREATE_ACCOUNT;
  create_account_sys* data_args = (create_account_sys*) (data + 4);
  data_args->lamports = lamports;
  data_args->space = space;
  sol_memcpy(&data_args->owner, owner, sizeof(SolPubkey));
  const SolInstruction instruction = {
      .program_id = system_program->key,
      .accounts = arguments,
      .account_len = SOL_ARRAY_SIZE(arguments),
      .data = data,
      .data_len = SOL_ARRAY_SIZE(data)
  };
  sol_invoke_signed(&instruction, params->ka, params->ka_num,
                           signers_seeds, SOL_ARRAY_SIZE(signers_seeds));
}

void create_sanity_account(SolParameters* params, SolAccountInfo* payer, SolAccountInfo* acct) {
  uint8_t acct_seed[7] = { 's', 'a', 'n', 'i', 't', 'y', 'x' };
  acct_seed[6] = params->data[SANITY_SEED_INIT];
  create_account(params, payer, acct, params->program_id, acct_seed, SOL_ARRAY_SIZE(acct_seed), sizeof(Sanity), 1);
}

void create_player_account(SolParameters* params, SolAccountInfo* payer, SolAccountInfo* acct) {
  uint8_t acct_seed[7] = { 'p', 'l', 'a', 'y', 'e', 'r', 'x' }; 
  acct_seed[6] = ((CreatePlayerInstr*)(params->data + 4))->player_seed;
  create_account(params, payer, acct, params->program_id, acct_seed, SOL_ARRAY_SIZE(acct_seed), sizeof(Player), 1);
}

void create_weapons_account(SolParameters* params, SolAccountInfo* payer, SolAccountInfo* weapons) {
  uint8_t acct_seed[7] = { 'w', 'e', 'a', 'p', 'o', 'n', 'x' }; 
  acct_seed[6] = params->data[WEAPON_SEED_INIT];
  create_account(params, payer, weapons, params->program_id, acct_seed, SOL_ARRAY_SIZE(acct_seed), sizeof(Weapons), 1);
}

void create_player_token_account(
  SolParameters* params,
  SolAccountInfo* payer,
  SolAccountInfo* acct,
  const SolPubkey* owner,
  uint8_t acct_seed[6],
  uint8_t seed_idx
) {
  acct_seed[5] = params->data[seed_idx];
  create_account(params, payer, acct, owner, acct_seed, 6, 165, 1);
}

void transfer(SolParameters* params, SolAccountInfo* payer, SolAccountInfo* payee, uint64_t lamports) {
  SolAccountInfo* system_program = &params->ka[1];

  uint8_t seed[] = { 'v', 'a', 'u', 'l', 't', 'x' };
  seed[5] = params->data[VAULT_SEED];

  const SolSignerSeed seeds[] = {{ .addr = seed, .len = SOL_ARRAY_SIZE(seed) }};
  const SolSignerSeeds signers_seeds[] = {{ .addr = seeds, .len = SOL_ARRAY_SIZE(seeds) }};

  SolAccountMeta arguments[] = {
    { .pubkey = payer->key, .is_writable = true, .is_signer = true },
    { .pubkey = payee->key, .is_writable = true, .is_signer = false },
  };
  uint8_t data[4 + sizeof(transfer_generic)];
  sol_memset(data, 0, sizeof(data));

  *(uint32_t *)data = TRANSFER;
  transfer_generic* data_args = (transfer_generic*) (data + 4);
  data_args->amount = lamports;

  const SolInstruction instruction = {
      .program_id = system_program->key,
      .accounts = arguments,
      .account_len = SOL_ARRAY_SIZE(arguments),
      .data = data,
      .data_len = SOL_ARRAY_SIZE(data)
  };
  sol_invoke_signed(&instruction, params->ka, params->ka_num,
                            signers_seeds, SOL_ARRAY_SIZE(signers_seeds));
}

void mint_to(SolParameters* params, SolAccountInfo* mint, SolAccountInfo* item, SolAccountInfo* authority, uint64_t amount) {
  SolAccountInfo* token = &params->ka[2];

  uint8_t seed[10] = { 'a', 'u', 't', 'h', 'o', 'r', 'i', 't', 'y', 'x' };
  seed[9] = params->data[AUTHORITY_SEED_INIT];
  const SolSignerSeed seeds[] = {{ .addr = seed, .len = SOL_ARRAY_SIZE(seed) }};
  const SolSignerSeeds signers_seeds[] = {{ .addr = seeds, .len = SOL_ARRAY_SIZE(seeds) }};

  uint8_t data[1 + sizeof(transfer_generic)];
  sol_memset(data, 0, sizeof(data));
  *(uint8_t *)data = MINT_TO;
  transfer_generic* data_args = (transfer_generic*) (data + 1);
  data_args->amount = amount;
  SolAccountMeta arguments[] = {
    { .pubkey = mint->key, .is_writable = true, .is_signer = false },
    { .pubkey = item->key, .is_writable = true, .is_signer = false },
    { .pubkey = authority->key, .is_writable = true, .is_signer = true },
  };
  const SolInstruction init_acc = {
    .program_id = token->key,
    .accounts = arguments,
    .account_len = SOL_ARRAY_SIZE(arguments),
    .data = data,
    .data_len = SOL_ARRAY_SIZE(data)
  };
  sol_invoke_signed(&init_acc, params->ka, params->ka_num, signers_seeds, SOL_ARRAY_SIZE(signers_seeds));
}

void initialize_account(SolParameters* params, SolAccountInfo* mint, SolAccountInfo* item, SolAccountInfo* authority) {
  SolAccountInfo* token = &params->ka[2];
  SolAccountInfo* rent = &params->ka[10];

  uint8_t seed[10] = { 'a', 'u', 't', 'h', 'o', 'r', 'i', 't', 'y', 'x' };
  seed[9] = params->data[AUTHORITY_SEED];
  const SolSignerSeed seeds[] = {{ .addr = seed, .len = SOL_ARRAY_SIZE(seed) }};
  const SolSignerSeeds signers_seeds[] = {{ .addr = seeds, .len = SOL_ARRAY_SIZE(seeds) }};

  uint8_t data[1];
  sol_memset(data, 0, sizeof(data));
  *(uint8_t *)data = INITIALIZE_ACCOUNT;
  SolAccountMeta arguments[] = {
    { .pubkey = item->key, .is_writable = true, .is_signer = false },
    { .pubkey = mint->key, .is_writable = false, .is_signer = false },
    { .pubkey = authority->key, .is_writable = false, .is_signer = false },
    { .pubkey = rent->key, .is_writable = false, .is_signer = false },
  };
  const SolInstruction init_acc = {
    .program_id = token->key,
    .accounts = arguments,
    .account_len = SOL_ARRAY_SIZE(arguments),
    .data = data,
    .data_len = SOL_ARRAY_SIZE(data)
  };
  sol_invoke_signed(&init_acc, params->ka, params->ka_num, signers_seeds, SOL_ARRAY_SIZE(signers_seeds));
}
