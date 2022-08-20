# SPDX-License-Identifier: MIT
# OpenZeppelin Cairo Contracts v0.1.0 (security/safemath.cairo)

%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin, SignatureBuiltin
from starkware.cairo.common.math import assert_not_zero
from starkware.cairo.common.uint256 import (
    Uint256, uint256_check, uint256_add, uint256_sub, uint256_mul, 
    uint256_unsigned_div_rem, uint256_le, uint256_lt, uint256_eq
)
from openzeppelin.utils.constants import TRUE, FALSE

# Adds two integers. 
# Reverts if the sum overflows.
func uint256_checked_add{
        syscall_ptr: felt*, 
        pedersen_ptr: HashBuiltin*, 
        range_check_ptr
    } (a: Uint256, b: Uint256) -> (c: Uint256):
    uint256_check(a)
    uint256_check(b)
    let (c: Uint256, is_overflow) = uint256_add(a, b)
    with_attr error_message("Safemath: addition overflow"):
        assert is_overflow = FALSE
    end
    return (c)
end

# Subtracts two integers.
# Reverts if minuend (`b`) is greater than subtrahend (`a`).
func uint256_checked_sub_le{
        syscall_ptr: felt*, 
        pedersen_ptr: HashBuiltin*, 
        range_check_ptr
    } (a: Uint256, b: Uint256) -> (c: Uint256):
    alloc_locals
    uint256_check(a)
    uint256_check(b)
    let (is_le) = uint256_le(b, a)
    with_attr error_message("Safemath: subtraction overflow"):
        assert is_le = TRUE
    end
    let (c: Uint256) = uint256_sub(a, b)
    return (c)
end

# Subtracts two integers.
# Reverts if minuend (`b`) is greater than or equal to subtrahend (`a`).
func uint256_checked_sub_lt{
        syscall_ptr: felt*, 
        pedersen_ptr: HashBuiltin*, 
        range_check_ptr
    } (a: Uint256, b: Uint256) -> (c: Uint256):
    alloc_locals
    uint256_check(a)
    uint256_check(b)

    let (is_lt) = uint256_lt(b, a)
    with_attr error_message("Safemath: subtraction overflow or the difference equals zero"):
        assert is_lt = TRUE
    end
    let (c: Uint256) = uint256_sub(a, b)
    return (c)
end

# Multiplies two integers.
# Reverts if product is greater than 2^256.
func uint256_checked_mul{
        syscall_ptr: felt*, 
        pedersen_ptr: HashBuiltin*, 
        range_check_ptr
    } (a: Uint256, b: Uint256) -> (c: Uint256):
    alloc_locals
    uint256_check(a)
    uint256_check(b)
    let (a_zero) = uint256_eq(a, Uint256(0, 0))
    if a_zero == TRUE:
        return (a)
    end

    let (b_zero) = uint256_eq(b, Uint256(0, 0))
    if b_zero == TRUE:
        return (b)
    end

    let (c: Uint256, overflow: Uint256) = uint256_mul(a, b)
    with_attr error_message("Safemath: multiplication overflow"):
        assert overflow = Uint256(0, 0)
    end
    return (c)
end

# Integer division of two numbers. Returns uint256 quotient and remainder.
# Reverts if divisor is zero as per OpenZeppelin's Solidity implementation.
# Cairo's `uint256_unsigned_div_rem` already checks:
#    remainder < divisor
#    quotient * divisor + remainder == dividend
func uint256_checked_div_rem{
        syscall_ptr: felt*, 
        pedersen_ptr: HashBuiltin*, 
        range_check_ptr
    } (a: Uint256, b: Uint256) -> (c: Uint256, rem: Uint256):
    alloc_locals
    uint256_check(a)
    uint256_check(b)
    
    let (is_zero) = uint256_eq(b, Uint256(0, 0))
    with_attr error_message("Safemath: divisor cannot be zero"):
        assert is_zero = FALSE
    end

    let (c: Uint256, rem: Uint256) = uint256_unsigned_div_rem(a, b)
    return (c, rem)
end
