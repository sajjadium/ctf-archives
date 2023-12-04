use revm::primitives::U256;

pub fn u64_to_ru256(n: u64) -> U256 {
    U256::from_limbs([n, 0, 0, 0])
}

pub fn u256_to_u64(value: &U256) -> u64 {
    value.as_limbs()[0]
}

pub fn eaddress_to_raddress(addr: &ethers::types::Address) -> revm::primitives::Address {
    revm::primitives::Address::from(addr.0)
}

pub fn raddress_to_eaddress(addr: &revm::primitives::Address) -> ethers::types::Address {
    ethers::types::Address::from(addr.0.0)
}

pub fn eu256_to_ru256(value: &ethers::types::U256) -> U256 {
    U256::from_limbs(value.0)
}

pub fn ru256_to_eu256(value: &U256) -> ethers::types::U256 {
    ethers::types::U256::from_big_endian(&value.to_be_bytes::<32>())
}