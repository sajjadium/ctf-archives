%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.starknet.common.syscalls import get_caller_address
from starkware.cairo.common.uint256 import Uint256, uint256_check, uint256_le, uint256_sub, uint256_add
from starkware.cairo.common.bool import TRUE, FALSE

@storage_var
func owner() -> (owner : felt):
end

@storage_var
func balances(account : felt) -> (balance : Uint256):
end

@storage_var
func initialized() -> (result : felt):
end

@external
func initialize{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
    }(owner_account : felt, initial_supply : Uint256) -> ():

    let (is_initialized) = initialized.read()
    if is_initialized != 0:
        return ()
    end
    initialized.write(1)
    uint256_check(initial_supply)

    owner.write(value=owner_account)

    balances.write(account=owner_account, value=initial_supply)
    return()
end

@view
func balanceOf{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
    }(account : felt) -> (balance : Uint256):
    let (balance) = balances.read(account=account)
    return (balance)
end

@external
func transfer{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
    }(recipient : felt, amount : Uint256):
    alloc_locals 

    uint256_check(amount)

    let (caller) = get_caller_address()

    let (caller_balance) = balances.read(account=caller)
    let (enough_balance) = uint256_le(amount, caller_balance)
    assert enough_balance = TRUE
    let (new_caller_balance) =  uint256_sub(caller_balance, amount)
    balances.write(account=caller, value=new_caller_balance)

    let (recipient_balance) = balances.read(account=recipient)
    let (new_recipient_balance, overflow) = uint256_add(recipient_balance, amount)
    assert overflow = FALSE
    balances.write(account=recipient, value=new_recipient_balance)

    return()
end

@external
func mint{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
    }(recipient : felt, amount : Uint256):
    only_owner()
    uint256_check(amount)

    let (recipient_balance) = balances.read(account=recipient)
    let (new_recipient_balance, overflow) = uint256_add(recipient_balance, amount)

    assert overflow = FALSE

    balances.write(account=recipient, value=new_recipient_balance)

    return()
end

@external
func burn{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
    }(account : felt, amount : Uint256):
    alloc_locals

    uint256_check(amount)
    let (account_balance) = balances.read(account=account)

    let (enough_balance) = uint256_le(account_balance, amount)
    assert enough_balance = TRUE

    let (new_account_balance) = uint256_sub(account_balance, amount)

    balances.write(account=account, value=new_account_balance)

    return()
end

func only_owner{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
    }():
    let (caller) = get_caller_address()
    let (owner_account) = owner.read()

    assert caller = owner_account

    return ()
end
