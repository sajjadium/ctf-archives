#include <solana_sdk.h>
#include "../shared/test.h"

#define POCKET_CNT 10

typedef struct {
  uint16_t deposit;
  uint16_t withdraw;
} Pocket;

typedef struct {
  Pocket pockets[POCKET_CNT]; 
} Wallet;

typedef enum {
  CREATE,
  DEPOSIT,
  WITHDRAW
} Op;

// [clock]
// [system program account]
// [wallet account]
// [???]
// [payer account]
uint64_t handle_create(SolParameters* params) {
  sol_log("handle_create");

  sol_assert(params->ka_num == 5);
  SolAccountInfo* system_program = &params->ka[1];
  SolAccountInfo* acct = &params->ka[2];
  SolAccountInfo* payer = &params->ka[4];

  uint8_t seed[] = { 'w', 'a', 'l', 'l', 'e', 't', 'x' };
  seed[6] = params->data[4];

  sol_assert(is_system_program(system_program->key));

  const SolSignerSeed seeds[] = {{seed, SOL_ARRAY_SIZE(seed)}};
  const SolSignerSeeds signers_seeds[] = {{seeds, SOL_ARRAY_SIZE(seeds)}};

  SolAccountMeta arguments[] = {
    {payer->key, true, true},
    {acct->key, true, true},
  };
  uint8_t data[4 + sizeof(create_account_sys)];
  sol_memset(data, 0, sizeof(data));
  *(uint16_t *)data = CREATE_ACCOUNT;
  create_account_sys* data_args = (create_account_sys*) (data + 4);
  data_args->lamports = 1;
  data_args->space = sizeof(Wallet);
  sol_memcpy(&data_args->owner, params->program_id, sizeof(SolPubkey));
  const SolInstruction instruction = {system_program->key, arguments,
                                      SOL_ARRAY_SIZE(arguments), data,
                                      SOL_ARRAY_SIZE(data)};
  sol_invoke_signed(&instruction, params->ka, params->ka_num,
                           signers_seeds, SOL_ARRAY_SIZE(signers_seeds));
  return SUCCESS;
}

void check_owner(SolParameters* params, SolAccountInfo* acct) {
  sol_assert(SolPubkey_same(acct->owner, params->program_id));
}

// [clock]
// [system program account]
// [wallet account]
// [payer_account]
// [vault account]
uint64_t handle_deposit(SolParameters* params) {
  sol_log("handle_deposit");

  sol_assert(params->ka_num == 5);
  SolAccountInfo* system_program = &params->ka[1];
  SolAccountInfo* wallet = &params->ka[2];
  SolAccountInfo* payer = &params->ka[3];
  SolAccountInfo* vault = &params->ka[4];

  sol_assert(is_system_program(system_program->key));
  check_owner(params, wallet);

  deposit_args* args;

  sol_assert(payer->is_signer);
  sol_assert(params->data_len - 4 >= sizeof(*args));

  args = (deposit_args*) (params->data + 4);
  sol_assert(args->idx < POCKET_CNT);
  sol_assert(args->amt != 0);

  const SolSignerSeeds signers_seeds[] = {};

  SolAccountMeta arguments[] = {
    {payer->key, true, true},
    {vault->key, true, false},
  };
  uint8_t data[4 + sizeof(transfer_amount_sys)];
  sol_memset(data, 0, sizeof(data));

  *(uint16_t *)data = TRANSFER;
  transfer_amount_sys* data_args = (transfer_amount_sys*) (data + 4);
  data_args->lamports = args->amt;

  const SolInstruction instruction = {system_program->key, arguments,
                                      SOL_ARRAY_SIZE(arguments), data,
                                      SOL_ARRAY_SIZE(data)};
  sol_invoke_signed(&instruction, params->ka, params->ka_num,
                           signers_seeds, SOL_ARRAY_SIZE(signers_seeds));

  Wallet* wallet_obj = (Wallet*) wallet->data;
  wallet_obj->pockets[args->idx].deposit += args->amt;

  return SUCCESS;
}

// [clock]
// [system program account]
// [wallet account]
// [payee account]
// [vault account]
uint64_t handle_withdraw(SolParameters* params) {
  sol_log("handle_withdraw");

  sol_assert(params->ka_num == 5);
  SolAccountInfo* system_program = &params->ka[1];
  SolAccountInfo* wallet = &params->ka[2];
  SolAccountInfo* payee = &params->ka[3];
  SolAccountInfo* vault = &params->ka[4];

  sol_assert(is_system_program(system_program->key));
  check_owner(params, wallet);

  withdraw_args* args;

  sol_assert(payee->is_signer);
  sol_assert(params->data_len - 4 >= sizeof(*args));

  args = (withdraw_args*) (params->data + 4);
  sol_assert(args->idx < POCKET_CNT);
  sol_assert(args->amt != 0);

  uint8_t seed[] = { 'v', 'a', 'u', 'l', 't', 'x' };
  seed[5] = args->bump;

  const SolSignerSeed seeds[] = {{seed, SOL_ARRAY_SIZE(seed)}};
  const SolSignerSeeds signers_seeds[] = {{seeds, SOL_ARRAY_SIZE(seeds)}};

  SolAccountMeta arguments[] = {
    {vault->key, true, true},
    {payee->key, true, false},
  };
  uint8_t data[4 + sizeof(transfer_amount_sys)];
  sol_memset(data, 0, sizeof(data));

  *(uint16_t *)data = TRANSFER;
  transfer_amount_sys* data_args = (transfer_amount_sys*) (data + 4);
  data_args->lamports = args->amt;

  const SolInstruction instruction = {system_program->key, arguments,
                                      SOL_ARRAY_SIZE(arguments), data,
                                      SOL_ARRAY_SIZE(data)};
  sol_invoke_signed(&instruction, params->ka, params->ka_num,
                           signers_seeds, SOL_ARRAY_SIZE(signers_seeds));

  Wallet* wallet_obj = (Wallet*) wallet->data;
  Pocket* pocket = &wallet_obj->pockets[args->idx];
  pocket->withdraw += args->amt;
  sol_assert(pocket->withdraw <= pocket->deposit);

  return SUCCESS;
}

uint64_t leagueOfLamports(SolParameters *params) {
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

  switch (*(int*)params->data) {
    case CREATE:
      handle_create(params);
      break;
    case DEPOSIT:
      handle_deposit(params);
      break;
    case WITHDRAW:
      handle_withdraw(params);
      break;
    default:
      sol_log("invalid op choice");
      log_int(*(int*) params->data, 10);
      return ERROR_INVALID_ARGUMENT;
  }

  return SUCCESS;
}

extern uint64_t entrypoint(const uint8_t *input) {
  sol_log("League of Lamports start");

  SolAccountInfo accounts[10];
  SolParameters params = (SolParameters){.ka = accounts};

  if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(accounts))) {
    return ERROR_INVALID_ARGUMENT;
  }

  return leagueOfLamports(&params);
}
