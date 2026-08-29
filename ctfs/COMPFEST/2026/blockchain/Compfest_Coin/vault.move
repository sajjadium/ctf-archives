module challenge::vault;

use sui::event;
use sui::table::{Self, Table};
use sui::transfer;
use sui::tx_context::TxContext;
use challenge::assets::CFX;
use challenge::math;
use challenge::config::{Self, GlobalConfig};
use challenge::oracle::PriceOracle;
use challenge::pool::{Self, RoutePool, RoutePosition};
use challenge::registry::{Self, RouteStrategy};

public struct IncentiveVault<phantom Reward> has key {
    id: UID,
    market: vector<u8>,
    balance: u64,
    claimed: Table<address, bool>,
}

public struct OperatorAccount<phantom Reward> has key, store {
    id: UID,
    earned: u64,
}

public struct IncentivesClaimed has copy, drop {
    operator: address,
    amount: u64,
}

const EAlreadyClaimed: u64 = 4;
const EWrongMarket: u64 = 3;
const EStrategyNotRegistered: u64 = 7;
const EInsufficientCfx: u64 = 5;

public(package) fun create(ctx: &mut TxContext): IncentiveVault<CFX> {
    let canonical = registry::canonical_market<challenge::assets::SUIX, challenge::assets::USDC>();
    IncentiveVault<CFX> {
        id: object::new(ctx),
        market: canonical,
        balance: 1000,
        claimed: table::new(ctx),
    }
}

public fun share(vault: IncentiveVault<CFX>) {
    transfer::share_object(vault);
}

public(package) fun create_operator(operator: address, ctx: &mut TxContext): OperatorAccount<CFX> {
    OperatorAccount<CFX> {
        id: object::new(ctx),
        earned: 0,
    }
}

public fun transfer_operator(account: OperatorAccount<CFX>, to: address) {
    transfer::public_transfer(account, to);
}

public entry fun claim_route_incentives<Base, Quote, Strategy>(
    vault: &mut IncentiveVault<CFX>,
    pool: &mut RoutePool<Base, Quote>,
    strategy: &RouteStrategy<Strategy>,
    position: &RoutePosition<Base, Quote>,
    account: &mut OperatorAccount<CFX>,
    oracle: &PriceOracle,
    config: &GlobalConfig,
    ctx: &TxContext,
) {
    let operator = tx_context::sender(ctx);
    assert!(!table::contains(&vault.claimed, operator), EAlreadyClaimed);
    assert!(math::same_bytes(&vault.market, &pool::canonical_market(pool)), EWrongMarket);
    assert!(math::same_bytes(&vault.market, registry::market(strategy)), EStrategyNotRegistered);
    assert!(pool::position_pool(position) == object::id(pool), 9);
    assert!(pool::effective_liquidity(pool, position) >= config::min_effective_liquidity(config), EInsufficientCfx);

    let claim = pool::quoted_route_score(pool, oracle);
    let amount = math::min(claim, vault.balance);
    vault.balance = vault.balance - amount;
    account.earned = account.earned + amount;
    table::add(&mut vault.claimed, operator, true);
    event::emit(IncentivesClaimed { operator, amount });
}

public entry fun donate_to_vault(vault: &mut IncentiveVault<CFX>, amount: u64) {
    assert!(amount > 0, 0);
    vault.balance = vault.balance + amount;
}

public fun earned(account: &OperatorAccount<CFX>): u64 {
    account.earned
}

public fun is_qualified(account: &OperatorAccount<CFX>, config: &GlobalConfig): bool {
    account.earned >= config::bounty_target(config)
}

public fun vault_balance(vault: &IncentiveVault<CFX>): u64 {
    vault.balance
}
