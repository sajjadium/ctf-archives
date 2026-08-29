module challenge::pool;

use sui::event;
use sui::transfer;
use sui::tx_context::TxContext;
use challenge::math;
use challenge::config::{Self, GlobalConfig};
use challenge::oracle::{Self, PriceOracle};
use challenge::registry::{Self, RouteRegistry};

public struct RoutePool<phantom Base, phantom Quote> has key {
    id: UID,
    direct_market: vector<u8>,
    canonical_market: vector<u8>,
    reserve_base: u64,
    reserve_quote: u64,
    lp_supply: u64,
    accounted_liquidity: u64,
}

public struct RoutePosition<phantom Base, phantom Quote> has key, store {
    id: UID,
    pool: ID,
    shares: u64,
}

public struct RoutePoolCreated has copy, drop {
    pool: ID,
    direct_market: vector<u8>,
    canonical_market: vector<u8>,
    reserve_base: u64,
    reserve_quote: u64,
}

const EInvalidAmount: u64 = 1;
const EMarketAlreadyRegistered: u64 = 2;
const EPoolNotRebalanceable: u64 = 12;
const EWrongPosition: u64 = 9;
const EInsufficientShares: u64 = 10;

public(package) fun create<Base, Quote>(
    reserve_base: u64,
    reserve_quote: u64,
    ctx: &mut TxContext,
): RoutePool<Base, Quote> {
    RoutePool<Base, Quote> {
        id: object::new(ctx),
        direct_market: registry::direct_market<Base, Quote>(),
        canonical_market: registry::canonical_market<Base, Quote>(),
        reserve_base,
        reserve_quote,
        lp_supply: reserve_base + reserve_quote,
        accounted_liquidity: reserve_base + reserve_quote,
    }
}

public fun share<Base, Quote>(pool: RoutePool<Base, Quote>) {
    transfer::share_object(pool);
}

public entry fun create_route_pool<Base, Quote>(
    registry: &mut RouteRegistry,
    config: &GlobalConfig,
    reserve_base: u64,
    reserve_quote: u64,
    ctx: &mut TxContext,
) {
    assert!(reserve_base > 0 && reserve_quote > 0, EInvalidAmount);

    let cap = config::rebalance_cap(config);
    assert!(reserve_base <= cap && reserve_quote <= cap, EPoolNotRebalanceable);

    let direct = registry::direct_market<Base, Quote>();
    assert!(!registry::has_market(registry, &direct), EMarketAlreadyRegistered);

    if (!registry::is_ordered<Base, Quote>()) {
        registry::normalize_market<Base, Quote>(registry);
    };

    registry::add_market(registry, direct);

    let pool = create<Base, Quote>(reserve_base, reserve_quote, ctx);
    event::emit(RoutePoolCreated {
        pool: object::id(&pool),
        direct_market: registry::direct_market<Base, Quote>(),
        canonical_market: registry::canonical_market<Base, Quote>(),
        reserve_base,
        reserve_quote,
    });
    transfer::share_object(pool);
}

public entry fun open_position<Base, Quote>(
    pool: &RoutePool<Base, Quote>,
    ctx: &mut TxContext,
) {
    transfer::public_transfer(RoutePosition<Base, Quote> {
        id: object::new(ctx),
        pool: object::id(pool),
        shares: 0,
    }, tx_context::sender(ctx));
}

public entry fun add_liquidity<Base, Quote>(
    pool: &mut RoutePool<Base, Quote>,
    position: &mut RoutePosition<Base, Quote>,
    shares: u64,
    config: &GlobalConfig,
) {
    assert!(shares > 0, EInvalidAmount);
    assert!(position.pool == object::id(pool), EWrongPosition);
    let net_shares = math::apply_fee_floor(shares, config::liquidity_fee_bps(config));
    pool.lp_supply = pool.lp_supply + net_shares;
    pool.accounted_liquidity = pool.accounted_liquidity + net_shares;
    position.shares = position.shares + net_shares;
}

public entry fun remove_liquidity<Base, Quote>(
    pool: &mut RoutePool<Base, Quote>,
    position: &mut RoutePosition<Base, Quote>,
    shares: u64,
) {
    assert!(shares > 0, EInvalidAmount);
    assert!(position.pool == object::id(pool), EWrongPosition);
    assert!(position.shares >= shares, EInsufficientShares);
    assert!(pool.lp_supply > shares, EInvalidAmount);
    pool.lp_supply = pool.lp_supply - shares;
    pool.accounted_liquidity = pool.accounted_liquidity - shares;
}

public fun position_pool<Base, Quote>(position: &RoutePosition<Base, Quote>): ID {
    position.pool
}

public fun effective_liquidity<Base, Quote>(
    pool: &RoutePool<Base, Quote>,
    position: &RoutePosition<Base, Quote>,
): u64 {
    position.shares * pool.accounted_liquidity / pool.lp_supply
}

public fun quoted_route_score<Base, Quote>(
    pool: &RoutePool<Base, Quote>,
    oracle: &PriceOracle,
): u64 {
    let raw = pool.reserve_quote / pool.reserve_base;
    let oracle_price = oracle::price_e6(oracle);
    if (raw > oracle_price) { raw } else { oracle_price }
}

public fun reserve_base<Base, Quote>(pool: &RoutePool<Base, Quote>): u64 { pool.reserve_base }
public fun reserve_quote<Base, Quote>(pool: &RoutePool<Base, Quote>): u64 { pool.reserve_quote }
public fun lp_supply<Base, Quote>(pool: &RoutePool<Base, Quote>): u64 { pool.lp_supply }
public fun canonical_market<Base, Quote>(pool: &RoutePool<Base, Quote>): vector<u8> { pool.canonical_market }
