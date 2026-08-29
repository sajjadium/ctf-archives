module challenge::registry;

use std::type_name;
use sui::event;
use sui::table::{Self, Table};
use sui::transfer;
use sui::tx_context::TxContext;
use challenge::assets::{SUIX, USDC};
use challenge::math;

public struct RouteRegistry has key {
    id: UID,
    listed_markets: vector<vector<u8>>,
    strategies: Table<vector<u8>, vector<u8>>,
}

public struct RouteStrategy<phantom Strategy> has key, store {
    id: UID,
    market: vector<u8>,
    strategy_type: vector<u8>,
}

public struct StrategyRegistered has copy, drop {
    strategy: ID,
    market: vector<u8>,
    strategy_type: vector<u8>,
}

const EMarketAlreadyRegistered: u64 = 2;
const EStrategyAlreadyRegistered: u64 = 6;

public(package) fun create(ctx: &mut TxContext): RouteRegistry {
    let mut registry = RouteRegistry {
        id: object::new(ctx),
        listed_markets: vector[],
        strategies: table::new(ctx),
    };
    registry.listed_markets.push_back(direct_market<SUIX, USDC>());
    registry
}

public fun share(registry: RouteRegistry) {
    transfer::share_object(registry);
}

public entry fun register_route_strategy<Base, Quote, Strategy: drop>(
    registry: &mut RouteRegistry,
    _witness: Strategy,
    ctx: &mut TxContext,
) {
    let market = canonical_market<Base, Quote>();
    let strategy_type = type_bytes<Strategy>();
    assert!(!table::contains(&registry.strategies, strategy_type), EStrategyAlreadyRegistered);
    table::add(&mut registry.strategies, strategy_type, market);

    let strategy = RouteStrategy<Strategy> {
        id: object::new(ctx),
        market: canonical_market<Base, Quote>(),
        strategy_type: type_bytes<Strategy>(),
    };
    event::emit(StrategyRegistered {
        strategy: object::id(&strategy),
        market: canonical_market<Base, Quote>(),
        strategy_type: type_bytes<Strategy>(),
    });
    transfer::public_transfer(strategy, tx_context::sender(ctx));
}

public fun market<Strategy>(strategy: &RouteStrategy<Strategy>): &vector<u8> {
    &strategy.market
}

public fun has_market(registry: &RouteRegistry, market: &vector<u8>): bool {
    let mut i = 0;
    let len = registry.listed_markets.length();
    while (i < len) {
        if (&registry.listed_markets[i] == market) {
            return true
        };
        i = i + 1;
    };
    false
}

public fun add_market(registry: &mut RouteRegistry, market: vector<u8>) {
    registry.listed_markets.push_back(market);
}

public fun normalize_market<Base, Quote>(registry: &mut RouteRegistry) {
    let canonical = canonical_market<Base, Quote>();
    if (!has_market(registry, &canonical)) {
        registry.listed_markets.push_back(canonical);
    };
}

public fun canonical_market<A, B>(): vector<u8> {
    let left = type_bytes<A>();
    let right = type_bytes<B>();
    if (math::bytes_lt(&right, &left)) {
        math::join_key(right, left)
    } else {
        math::join_key(left, right)
    }
}

public fun direct_market<A, B>(): vector<u8> {
    math::join_key(type_bytes<A>(), type_bytes<B>())
}

public fun type_bytes<T>(): vector<u8> {
    type_name::with_original_ids<T>().into_string().into_bytes()
}

public fun is_ordered<A, B>(): bool {
    !math::bytes_lt(&type_bytes<B>(), &type_bytes<A>())
}
