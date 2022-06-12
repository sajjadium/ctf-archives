#include <solana_sdk.h>
#include "../shared/program.h"

/*
 * this is 3vil smart-contract with one instruction:
 *
 *     3vilInstruction
 *         ????????????????????
 *
 *         Account references
 *         [WRITE]          The destination account
 *         [EXECUTE]        Program
 *         [WRITE]          The source account
 *         [SIGNER]         The source account's owner
 *
 *  The instruction will replace accounts in the pre-defined manner.
 *  It will call the instruction #3 of the program passed as the second account.
 */


uint64_t handle(SolParameters *params) {
    sol_assert(params->ka_num == 4);
    SolAccountInfo* acc0 = &params->ka[0];
    SolAccountInfo* acc1 = &params->ka[1];
    SolAccountInfo* acc2 = &params->ka[2];
    SolAccountInfo* acc3 = &params->ka[3];

    uint8_t data[1 + sizeof(transfer)];
    sol_memset(data, 0, sizeof(data));
    data[0] = 3;
    transfer* data_args = (transfer*)(data + 1);
    data_args->amount = 1;

    SolAccountMeta arguments[] = {
      { .pubkey = acc2->key, .is_writable = true, .is_signer = false },
      { .pubkey = acc0->key, .is_writable = true, .is_signer = false },
      { .pubkey = acc3->key, .is_writable = true, .is_signer = true },
    };

    const SolInstruction init_acc = {
      .program_id = acc1->key,
      .accounts = arguments,
      .account_len = SOL_ARRAY_SIZE(arguments),
      .data = data,
      .data_len = sizeof(data)
    };
    sol_invoke(&init_acc, params->ka, params->ka_num);

    return SUCCESS;
}

extern uint64_t entrypoint(const uint8_t *input) {
    sol_log("solana 3vil smart-contract");

    SolAccountInfo accounts[5];
    SolParameters params = (SolParameters){.ka = accounts};

    if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(accounts))) {
        return ERROR_INVALID_ARGUMENT;
    }

    return handle(&params);
}
