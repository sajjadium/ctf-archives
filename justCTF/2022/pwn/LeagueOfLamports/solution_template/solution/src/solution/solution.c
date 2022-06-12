#include <solana_sdk.h>
#include "../shared/test.h"

uint64_t solution(SolParameters *params) {
  return SUCCESS;
}

extern uint64_t entrypoint(const uint8_t *input) {
  sol_log("solution start");

  SolAccountInfo accounts[10];
  SolParameters params = (SolParameters){.ka = accounts};

  if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(accounts))) {
    return ERROR_INVALID_ARGUMENT;
  }

  return solution(&params);
}
