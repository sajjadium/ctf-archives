module challenge::setup;

use sui::transfer;
use sui::tx_context::TxContext;
use challenge::assets::{CFX, SUIX, USDC};
use challenge::config;
use challenge::oracle;
use challenge::registry;
use challenge::pool;
use challenge::vault;

const ENotQualified: u64 = 0;

public struct Setup has key {
    id: UID,
    solved: bool,
}

public struct AdminCap has key, store {
    id: UID,
}

fun init(ctx: &mut TxContext) {
    transfer::public_transfer(AdminCap { id: object::new(ctx) }, ctx.sender());
}

public fun mint_cap(_: &AdminCap, to: address, ctx: &mut TxContext) {
    transfer::public_transfer(AdminCap { id: object::new(ctx) }, to);
}

public fun initialize(_: &AdminCap, player: address, ctx: &mut TxContext) {
    transfer::share_object(Setup { id: object::new(ctx), solved: false });

    let registry_obj = registry::create(ctx);
    registry::share(registry_obj);

    let vault_obj = vault::create(ctx);
    vault::share(vault_obj);

    let pool_obj = pool::create<SUIX, USDC>(1_000_000, 1_000_000, ctx);
    pool::share(pool_obj);

    let operator = vault::create_operator(player, ctx);
    vault::transfer_operator(operator, player);

    let cfg = config::create(ctx);
    config::share(cfg);

    let oracle_obj = oracle::create(ctx.sender(), ctx);
    oracle::share(oracle_obj);
}

public entry fun solve(setup: &mut Setup, account: &vault::OperatorAccount<CFX>, config: &config::GlobalConfig) {
    assert!(vault::is_qualified(account, config), ENotQualified);
    setup.solved = true;
}

public fun is_solved(setup: &Setup): bool {
    setup.solved
}

#[test_only]
public fun init_for_testing(ctx: &mut TxContext) {
    init(ctx);
}
