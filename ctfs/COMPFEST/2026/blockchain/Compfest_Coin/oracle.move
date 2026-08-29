module challenge::oracle;

use sui::tx_context::TxContext;
use sui::transfer;

public struct PriceOracle has key {
    id: UID,
    price: u64,
    admin: address,
}

public fun create(admin: address, ctx: &mut TxContext): PriceOracle {
    PriceOracle {
        id: object::new(ctx),
        price: 1,
        admin,
    }
}

public fun share(oracle: PriceOracle) {
    transfer::share_object(oracle);
}

public fun price_e6(oracle: &PriceOracle): u64 {
    oracle.price
}

public fun admin(oracle: &PriceOracle): address {
    oracle.admin
}

public entry fun set_price(oracle: &mut PriceOracle, price: u64, ctx: &TxContext) {
    assert!(tx_context::sender(ctx) == oracle.admin, 0);
    assert!(price > 0, 1);
    oracle.price = price;
}

public entry fun transfer_admin(oracle: &mut PriceOracle, new_admin: address, ctx: &TxContext) {
    assert!(tx_context::sender(ctx) == oracle.admin, 0);
    oracle.admin = new_admin;
}
