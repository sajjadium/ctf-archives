#include <solana_sdk.h>
#include "../shared/test.h"

void check_owner(SolParameters* params, SolAccountInfo* acct) {
  sol_assert(SolPubkey_same(acct->owner, params->program_id));
}

// [clock]
// [system program account]
// [spl_token account]
// [item mint]
// [item token account]
// [item_1337 mint]
// [item_1337 token account]
// [authority]
// [payer]
// [sanity account]
// [weapons account]
uint64_t handle_initialize(SolParameters* params) {
  sol_log("Initialize");

  sol_assert(params->ka_num == 11);
  SolAccountInfo* system = &params->ka[1];
  SolAccountInfo* token = &params->ka[2];
  SolAccountInfo* mint = &params->ka[3];
  SolAccountInfo* item = &params->ka[4];
  SolAccountInfo* mint_1337 = &params->ka[5];
  SolAccountInfo* item_1337 = &params->ka[6];
  SolAccountInfo* authority = &params->ka[7];
  SolAccountInfo* payer = &params->ka[8];
  SolAccountInfo* sanity_acc = &params->ka[9];
  SolAccountInfo* weapons = &params->ka[10];

  sol_assert(is_system_program(system->key));
  sol_assert(is_system_program(payer->owner));
  sol_assert(payer->is_signer);
  sol_assert(item->is_signer);
  sol_assert(item_1337->is_signer);
  sol_assert(weapons->data_len == 0);
  sol_assert(sanity_acc->data_len == 0);

  create_weapons_account(params, payer, weapons);

  mint_to(params, mint, item, authority, 100);
  mint_to(params, mint_1337, item_1337, authority, 1);
  Weapons* weapons_list = (Weapons*)weapons->data;
  weapons_list->weapons[0] = (Weapon){ .mint = *mint->key, .price = 1, .attack = 1 };
  weapons_list->weapons[1] = (Weapon){ .mint = *mint_1337->key, .price = 0x1337, .attack = 0x1337 };
  
  create_sanity_account(params, payer, sanity_acc);
  Sanity* temp = (Sanity*) sanity_acc->data;
  sol_memcpy(&temp->token, token->key, sizeof(SolPubkey));

  return SUCCESS;
}

// [clock]
// [system program account]
// [spl_token account]
// [item mint]
// [item token account]
// [solve item token account]
// [authority]
// [payer]
// [sanity account]
// [vault]
// [player account]
// [weapons account]
uint64_t handle_buy(SolParameters* params) {
  sol_log("Buy Item");

  sol_assert(params->ka_num == 12);
  SolAccountInfo* system_program = &params->ka[1];
  SolAccountInfo* token = &params->ka[2];
  SolAccountInfo* mint = &params->ka[3];
  SolAccountInfo* item = &params->ka[4];
  SolAccountInfo* solve_item = &params->ka[5];
  SolAccountInfo* authority = &params->ka[6];
  SolAccountInfo* payer = &params->ka[7];
  SolAccountInfo* sanity_acc = &params->ka[8];
  SolAccountInfo* vault = &params->ka[9];
  SolAccountInfo* player_acc = &params->ka[10];
  SolAccountInfo* weapons = &params->ka[11];

  Account* account = (Account*)item->data;
  Account* payer_account = (Account*)solve_item->data;

  sol_assert(is_system_program(system_program->key));
  sol_assert(is_system_program(authority->owner));
  sol_assert(payer->is_signer);
  check_owner(params, weapons);
  check_owner(params, sanity_acc);
  check_owner(params, player_acc);
  sol_assert(SolPubkey_same(token->key, &((Sanity*)sanity_acc->data)->token));
  sol_assert(SolPubkey_same(&account->mint, &payer_account->mint));
  sol_assert(SolPubkey_same(&account->owner, authority->key));
  sol_assert(SolPubkey_same(&payer_account->owner, authority->key));
  sol_assert(weapons->data_len == sizeof(Weapons));
  sol_assert(sanity_acc->data_len == sizeof(Sanity));
  sol_assert(player_acc->data_len == sizeof(Player));

  BuyInstr* buy_instr = (BuyInstr*)(params->data + 4);

  uint8_t seed[10] = { 'a', 'u', 't', 'h', 'o', 'r', 'i', 't', 'y', 'x' };
  seed[9] = buy_instr->authority_seed;
  const SolSignerSeed seeds[] = {{ .addr = seed, .len = SOL_ARRAY_SIZE(seed) }};
  const SolSignerSeeds signers_seeds[] = {{ .addr = seeds, .len = SOL_ARRAY_SIZE(seeds) }};

  uint64_t amount = buy_instr->amount;
  Weapon weapon;
  Weapons* weapons_list = (Weapons*)weapons->data;
  if (SolPubkey_same(&account->mint, &weapons_list->weapons[1].mint)) {
      weapon = weapons_list->weapons[1];
  } else {
      weapon = weapons_list->weapons[0];
  }
  sol_assert(*payer->lamports >= weapon.price * amount);

  uint8_t data[1 + sizeof(transfer_checked)];
  sol_memset(data, 0, sizeof(data));
  *(uint8_t *)data = TRANSFER_TOKEN_CHECKED;
  transfer_checked* data_args = (transfer_checked*) (data + 1);
  data_args->amount = amount;
  data_args->decimals = 9;
  SolAccountMeta arguments[] = {
    { .pubkey = item->key, .is_writable = true, .is_signer = false },
    { .pubkey = mint->key, .is_writable = false, .is_signer = false },
    { .pubkey = solve_item->key, .is_writable = true, .is_signer = false },
    { .pubkey = authority->key, .is_writable = true, .is_signer = true },
  };
  SolPubkey token_pubkey = ((Sanity*)sanity_acc->data)->token;
  const SolInstruction init_acc = {
    .program_id = &token_pubkey,
    .accounts = arguments,
    .account_len = SOL_ARRAY_SIZE(arguments),
    .data = data,
    .data_len = SOL_ARRAY_SIZE(data)
  };
  sol_invoke_signed(&init_acc, params->ka, params->ka_num, signers_seeds, SOL_ARRAY_SIZE(signers_seeds));

  transfer(params, payer, vault, weapon.price * amount);

  return SUCCESS;
}

// [clock]
// [system program account]
// [spl_token account]
// [item mint]
// [item token account]
// [solve item token account]
// [authority]
// [payee]
// [sanity account]
// [vault]
// [player account]
// [weapons]
uint64_t handle_sell(SolParameters* params) {
  sol_log("Sell Item");

  sol_assert(params->ka_num == 12);
  SolAccountInfo* system_program = &params->ka[1];
  SolAccountInfo* token = &params->ka[2];
  SolAccountInfo* mint = &params->ka[3];
  SolAccountInfo* item = &params->ka[4];
  SolAccountInfo* solve_item = &params->ka[5];
  SolAccountInfo* authority = &params->ka[6];
  SolAccountInfo* payee = &params->ka[7];
  SolAccountInfo* sanity_acc = &params->ka[8];
  SolAccountInfo* vault = &params->ka[9];
  SolAccountInfo* player_acc = &params->ka[10];
  SolAccountInfo* weapons = &params->ka[11];

  Account* account = (Account*)item->data;
  Account* payee_account = (Account*)solve_item->data;

  sol_assert(is_system_program(system_program->key));
  sol_assert(is_system_program(authority->owner));
  check_owner(params, weapons);
  check_owner(params, sanity_acc);
  check_owner(params, player_acc);
  sol_assert(SolPubkey_same(token->key, &((Sanity*)sanity_acc->data)->token));
  sol_assert(SolPubkey_same(&account->mint, &payee_account->mint));
  sol_assert(SolPubkey_same(&account->owner, authority->key));
  sol_assert(SolPubkey_same(&payee_account->owner, authority->key));
  sol_assert(weapons->data_len == sizeof(Weapons));
  sol_assert(sanity_acc->data_len == sizeof(Sanity));
  sol_assert(player_acc->data_len == sizeof(Player));

  SellInstr* sell_instr = (SellInstr*)(params->data + 4);

  uint8_t seed[10] = { 'a', 'u', 't', 'h', 'o', 'r', 'i', 't', 'y', 'x' };
  seed[9] = sell_instr->authority_seed;
  const SolSignerSeed seeds[] = {{ .addr = seed, .len = SOL_ARRAY_SIZE(seed) }};
  const SolSignerSeeds signers_seeds[] = {{ .addr = seeds, .len = SOL_ARRAY_SIZE(seeds) }};

  uint64_t amount = sell_instr->amount;
  Weapon weapon;
  Weapons* weapons_list = (Weapons*)weapons->data;
  if (SolPubkey_same(&account->mint, &weapons_list->weapons[1].mint)) {
      weapon = weapons_list->weapons[1];
  } else {
      weapon = weapons_list->weapons[0];
  }
  sol_assert(*vault->lamports >= weapon.price * amount);
  uint8_t data[1 + sizeof(transfer_checked)];
  sol_memset(data, 0, sizeof(data));
  *(uint8_t *)data = TRANSFER_TOKEN_CHECKED;
  transfer_checked* data_args = (transfer_checked*) (data + 1);
  data_args->amount = amount;
  data_args->decimals = 9;
  SolAccountMeta arguments[] = {
    { .pubkey = solve_item->key, .is_writable = true, .is_signer = false },
    { .pubkey = mint->key, .is_writable = false, .is_signer = false },
    { .pubkey = item->key, .is_writable = true, .is_signer = false },
    { .pubkey = authority->key, .is_writable = true, .is_signer = true },
  };
  SolPubkey token_pubkey = ((Sanity*)sanity_acc->data)->token;
  const SolInstruction init_acc = {
    .program_id = &token_pubkey,
    .accounts = arguments,
    .account_len = SOL_ARRAY_SIZE(arguments),
    .data = data,
    .data_len = SOL_ARRAY_SIZE(data)
  };
  sol_invoke_signed(&init_acc, params->ka, params->ka_num, signers_seeds, SOL_ARRAY_SIZE(signers_seeds));

  transfer(params, vault, payee, weapon.price * amount);

  return SUCCESS;
}


// [clock]
// [system program account]
// [spl_token account]
// [solve item token account]
// [authority]
// [payee]
// [sanity account]
// [vault]
// [player account]
// [weapons]
uint64_t handle_fight(SolParameters* params){
  sol_log("Fight a MONSTER!");

  sol_assert(params->ka_num == 10);
  SolAccountInfo* system_program = &params->ka[1];
  SolAccountInfo* token = &params->ka[2];
  SolAccountInfo* solve_item = &params->ka[3];
  SolAccountInfo* authority = &params->ka[4];
  SolAccountInfo* payee = &params->ka[5];
  SolAccountInfo* sanity_acc = &params->ka[6];
  SolAccountInfo* vault = &params->ka[7];
  SolAccountInfo* player_acc = &params->ka[8];
  SolAccountInfo* weapons = &params->ka[9];

  Player* player = (Player*)player_acc->data;
  Account* account = (Account*)solve_item->data;

  sol_assert(is_system_program(system_program->key));
  sol_assert(is_system_program(authority->owner));
  check_owner(params, weapons);
  check_owner(params, sanity_acc);
  check_owner(params, player_acc);
  sol_assert(SolPubkey_same(token->key, &((Sanity*)sanity_acc->data)->token));
  sol_assert(SolPubkey_same(&account->owner, authority->key));
  sol_assert(weapons->data_len == sizeof(Weapons));
  sol_assert(sanity_acc->data_len == sizeof(Sanity));
  sol_assert(player_acc->data_len == sizeof(Player));

  Weapon weapon;
  Weapons* weapons_list = (Weapons*)weapons->data;
  if (SolPubkey_same(&account->mint, &weapons_list->weapons[1].mint)) {
      weapon = weapons_list->weapons[1];
  } else if (SolPubkey_same(&account->mint, &weapons_list->weapons[0].mint)) {
      weapon = weapons_list->weapons[0];
  } else {
      return ERROR_INVALID_INSTRUCTION_DATA;
  }
  uint64_t player_attack = account->amount * weapon.attack;

  Monster monsters[9] = {
    { .attack = 1,      .reward = 1 },
    { .attack = 2,      .reward = 1 },
    { .attack = 4,      .reward = 2 },
    { .attack = 8,      .reward = 2 },
    { .attack = 16,     .reward = 3 },
    { .attack = 32,     .reward = 3 },
    { .attack = 64,     .reward = 4 },
    { .attack = 128,    .reward = 4 },
    { .attack = 0x1337, .reward = 0xd337 }
  };

  FightInstr* fight_instr = (FightInstr*)(params->data + 4);
  Monster monster = monsters[fight_instr->monster];
  uint64_t needed_health = 0;
  if (monster.attack > player_attack) {
    needed_health = (monster.attack - player_attack) * fight_instr->number;
  }
  uint64_t needed_mana = fight_instr->number;
  sol_assert(player->health >= needed_health);
  sol_assert(player->mana >= needed_mana);
  player->health -= needed_health;
  player->mana -= needed_mana;

  transfer(params, vault, payee, monster.reward * fight_instr->number);

  return SUCCESS;
}

// [clock]
// [system program account]
// [spl_token account]
// [item mint]
// [solve item token account]
// [item_1337 mint]
// [solve item_1337 token account]
// [authority]
// [payer]
// [sanity account]
// [rent]
// [player account]
// [vault]
uint64_t handle_create_player(SolParameters* params){
  sol_log("Create Player!");

  sol_assert(params->ka_num == 14);
  SolAccountInfo* token = &params->ka[2];
  SolAccountInfo* mint = &params->ka[3];
  SolAccountInfo* solve_item = &params->ka[4];
  SolAccountInfo* mint_1337 = &params->ka[5];
  SolAccountInfo* solve_item_1337 = &params->ka[6];
  SolAccountInfo* authority = &params->ka[7];
  SolAccountInfo* payer = &params->ka[8];
  SolAccountInfo* sanity_acc = &params->ka[9];
  SolAccountInfo* player_acc = &params->ka[11];
  SolAccountInfo* vault = &params->ka[12];
  SolAccountInfo* weapons = &params->ka[13];

  check_owner(params, weapons);
  check_owner(params, sanity_acc);
  sol_assert(is_system_program(authority->owner));
  sol_assert(SolPubkey_same(token->key, &((Sanity*)sanity_acc->data)->token));
  sol_assert(weapons->data_len == sizeof(Weapons));
  sol_assert(sanity_acc->data_len == sizeof(Sanity));
  sol_assert(player_acc->data_len == 0);

  Weapons* weapons_list = (Weapons*)weapons->data; 

  sol_assert(SolPubkey_same(mint->key, &weapons_list->weapons[0].mint));
  sol_assert(SolPubkey_same(mint_1337->key, &weapons_list->weapons[1].mint));

  create_player_account(params, payer, player_acc);
  Player* player = (Player*)player_acc->data;
  player->health = 0xff;
  player->mana = 0xff;
  const char* name = (const char*)(params->data + 9);
  sol_memcpy(player->name, name, 30);

  uint8_t acct_seed[6] = { 't', 'o', 'k', 'e', 'n', 'x' }; 
  create_player_token_account(params, payer, solve_item, token->key, acct_seed, ITEM_TOKEN_SEED);
  uint8_t acct_seed_1337[6] = { '1', '3', '3', '3', '7', 'x' }; 
  create_player_token_account(params, payer, solve_item_1337, token->key, acct_seed_1337, ITEM_1337_TOKEN_SEED);

  transfer(params, vault, solve_item, MINIMUM_BALANCE);
  transfer(params, vault, solve_item_1337, MINIMUM_BALANCE);

  initialize_account(params, mint, solve_item, authority);
  initialize_account(params, mint_1337, solve_item_1337, authority);

  return SUCCESS;
}

uint64_t dark_sols(SolParameters *params) {
  SolAccountInfo* clock = &params->ka[0];

  sol_assert(clock->data_len > 0);

  char x[100];
  size_t x_size = SOL_ARRAY_SIZE(x);
  b58enc(x, &x_size, clock->key, SOL_ARRAY_SIZE(clock->key->x));
  if (!str_contains(x, "C1ock")) {
    sol_log("bad C1ock account");
    return ERROR_INVALID_ARGUMENT;
  }

  Clock* clk = (Clock*) clock->data;
  if (clk->unix_timestamp <= 1654927200) {
    sol_log("Your clock is broken.");
    return ERROR_INVALID_ARGUMENT;
  }

  sol_assert(params->data_len >= sizeof(int));

  switch (*(uint32_t*)params->data) {
    case INITIALIZE:
      handle_initialize(params);
      break;
    case SELL:
      handle_sell(params);
      break;
    case BUY:
      handle_buy(params);
      break;
    case CREATE_PLAYER:
      handle_create_player(params);
      break;
    case FIGHT:
      handle_fight(params);
      break;
    default:
      sol_log("invalid op choice");
      log_int(*(int*) params->data, 10);
      return ERROR_INVALID_ARGUMENT;
  }

  return SUCCESS;
}

extern uint64_t entrypoint(const uint8_t *input) {
  sol_log("Dark SOLs start");

  SolAccountInfo accounts[20];
  SolParameters params = (SolParameters){.ka = accounts};

  if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(accounts))) {
    return ERROR_INVALID_ARGUMENT;
  }

  return dark_sols(&params);
}
