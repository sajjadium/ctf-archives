/**
 * @brief C-based Helloworld BPF program
 */
#include <solana_sdk.h>

#include "../shared/test.h"

typedef struct {
  uint64_t liab;  // withdrawn
  uint64_t collat;  // deposited
} Market;

typedef struct {
  uint64_t date;
  uint64_t nights_booked;
  uint64_t nights_slept;
} HotelRoom;

#define MARKET_CNT 10

typedef struct {
  Market markets[MARKET_CNT];
} LendingData;

typedef struct {
  HotelRoom rooms[MARKET_CNT];
} RoomsData;


typedef enum {
  CREATE,
  DEPOSIT,
  WITHDRAW,
  BOOKROOM,
  SLEEP
} Op;

// [clock]
// [system program account]
// [target_addr]
// [program_id]
// [payer]
uint64_t handle_create(SolParameters* params) {
  sol_log("handle_create");

  sol_assert(params->ka_num == 5);
  SolAccountInfo* system_program = &params->ka[1];
  SolAccountInfo* acct = &params->ka[2];
  SolAccountInfo* payer = &params->ka[4];

  uint8_t seed[1];
  seed[0] = params->data[4];

  sol_assert(is_system_program(system_program->key));

  const SolSignerSeed seeds[] = {{seed, SOL_ARRAY_SIZE(seed)}};
  const SolSignerSeeds signers_seeds[] = {{seeds, SOL_ARRAY_SIZE(seeds)}};


  SolAccountMeta arguments[] = {
    {payer->key, true, true},
    {acct->key, true, true},
  };
  uint8_t data[4 + sizeof(create_account_sys)];            // Enough room for the Allocate instruction
  sol_memset(data, 0, sizeof(data));
  *(uint16_t *)data = CREATE_ACCOUNT;
  create_account_sys* data_args = (create_account_sys*) (data + 4);
  data_args->lamports = 1;
  data_args->space = sizeof(LendingData);
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
// [system program]
// [lending_data_account]
// [payer_account]
// [program account]

uint64_t handle_deposit(SolParameters* params) {
  sol_log("handle_deposit");

  sol_assert(params->ka_num == 5);
  SolAccountInfo* system_program = &params->ka[1];
  SolAccountInfo* ld_acct = &params->ka[2];
  SolAccountInfo* payer = &params->ka[3];
  SolAccountInfo* vault = &params->ka[4];

  sol_assert(is_system_program(system_program->key));
  check_owner(params, ld_acct);

  deposit_args* args;

  sol_assert(payer->is_signer);
  sol_assert(params->data_len - 4 >= sizeof(*args));

  args = (deposit_args*) (params->data + 4);
  sol_assert(args->idx < MARKET_CNT);
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

  LendingData* ld_obj = (LendingData*) ld_acct->data;
  ld_obj->markets[args->idx].collat += args->amt;

  return SUCCESS;
}

// [clock]
// [system program]
// [lending_data_account]
// [payee account]
// [vault account]
uint64_t handle_withdraw(SolParameters* params) {
  sol_log("handle_withdraw");

  sol_assert(params->ka_num == 5);
  SolAccountInfo* system_program = &params->ka[1];
  SolAccountInfo* ld_acct = &params->ka[2];
  SolAccountInfo* payee = &params->ka[3];
  SolAccountInfo* vault = &params->ka[4];

  sol_assert(is_system_program(system_program->key));
  check_owner(params, ld_acct);

  withdraw_args* args;

  sol_assert(payee->is_signer);
  sol_assert(params->data_len - 4 >= sizeof(*args));

  args = (withdraw_args*) (params->data + 4);
  sol_assert(args->idx < MARKET_CNT);
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

  LendingData* ld_obj = (LendingData*) ld_acct->data;
  Market* market = &ld_obj->markets[args->idx];
  market->liab += args->amt;
  sol_assert(market->liab <= market->collat);

  return SUCCESS;
}


// [clock]
// [lending_data_account]
uint64_t handle_book(SolParameters* params){
  sol_log("handle_book");

  sol_assert(params->ka_num == 2);
  SolAccountInfo* clock = &params->ka[0];
  SolAccountInfo* ld_acct = &params->ka[1];

  Clock* clk = (Clock*) clock->data;

  check_owner(params, ld_acct);

  book_args* args = (book_args *)(params->data + 4);
  sol_assert(args->idx < MARKET_CNT);
  // sol_log_64_(args->nights, 0,0,0,0);
  sol_assert(args->nights > 0 && args->nights < 7);

  RoomsData* ld_obj = (RoomsData*) ld_acct->data;

  HotelRoom* room = (HotelRoom *) &ld_obj->rooms[args->idx];

  sol_assert(room->date == 0);

  room->date = clk->unix_timestamp;
  room->nights_booked = args->nights;
  room->nights_slept = 0;


  LendingData* a = (LendingData*) ld_acct->data;
  // sol_log_64_(a->markets[0].liab, a->markets[0].collat, a->markets[1].liab, a->markets[1].collat, 0);

  // sol_log_64_(a->markets[0].liab, a->markets[0].collat, a->markets[1].liab, a->markets[1].collat, 0);

  return SUCCESS;
}

// [clock]
// [lending_data_account]
uint64_t handle_sleep(SolParameters* params){
  sol_log("handle_sleep");

  sol_assert(params->ka_num == 2);
  SolAccountInfo* clock = &params->ka[0];
  SolAccountInfo* ld_acct = &params->ka[1];

  check_owner(params, ld_acct);

  sleep_args* args = (sleep_args *)(params->data + 4);
  sol_assert(args->idx < MARKET_CNT);

  RoomsData* ld_obj = (RoomsData*) ld_acct->data;

  HotelRoom* room = (HotelRoom *) &ld_obj->rooms[args->idx];

  sol_assert(room->date != 0);
  room->nights_slept++;

  return SUCCESS;
}

uint64_t beachside(SolParameters *params) {
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
  if (clk->unix_timestamp <= 1647360000) {
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
    case BOOKROOM:
      handle_book(params);
      break;
    case SLEEP:
      handle_sleep(params);
      break;
    default:
      sol_log("invalid op choice");
      log_int(*(int*) params->data, 10);
      return ERROR_INVALID_ARGUMENT;
  }

  return SUCCESS;
}

extern uint64_t entrypoint(const uint8_t *input) {
  sol_log("Beachside start");

  SolAccountInfo accounts[10];
  SolParameters params = (SolParameters){.ka = accounts};

  if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(accounts))) {
    return ERROR_INVALID_ARGUMENT;
  }

  return beachside(&params);
}
