module challenge::config;

use sui::transfer;
use sui::tx_context::TxContext;

public struct GlobalConfig has key {
    id: UID,
    liquidity_fee_bps: u64,
    withdraw_fee_bps: u64,
    min_effective_liquidity: u64,
    bounty_target: u64,
    rebalance_cap: u64,
}

public fun create(ctx: &mut TxContext): GlobalConfig {
    GlobalConfig {
        id: object::new(ctx),
        liquidity_fee_bps: 0,
        withdraw_fee_bps: 0,
        min_effective_liquidity: 500,
        bounty_target: 500,
        rebalance_cap: 2_000_000,
    }
}

public fun share(cfg: GlobalConfig) {
    transfer::share_object(cfg);
}

public fun liquidity_fee_bps(cfg: &GlobalConfig): u64 { cfg.liquidity_fee_bps }
public fun withdraw_fee_bps(cfg: &GlobalConfig): u64 { cfg.withdraw_fee_bps }
public fun min_effective_liquidity(cfg: &GlobalConfig): u64 { cfg.min_effective_liquidity }
public fun bounty_target(cfg: &GlobalConfig): u64 { cfg.bounty_target }
public fun rebalance_cap(cfg: &GlobalConfig): u64 { cfg.rebalance_cap }

public entry fun set_fees(cfg: &mut GlobalConfig, liquidity_bps: u64, withdraw_bps: u64, _ctx: &TxContext) {
    cfg.liquidity_fee_bps = liquidity_bps;
    cfg.withdraw_fee_bps = withdraw_bps;
}

