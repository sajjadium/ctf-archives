%lang starknet
%builtins pedersen range_check

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.uint256 import Uint256, uint256_le, uint256_lt, uint256_sub, uint256_add
from starkware.cairo.common.math import assert_lt, assert_not_zero
from starkware.starknet.common.syscalls import get_caller_address, get_contract_address, get_block_timestamp
from openzeppelin.token.erc20.interfaces.IERC20 import IERC20


const TRUE = 1
const FALSE = 0
const DELAY  = 10000

@storage_var
func _owner() -> (owner_address : felt):
end

@storage_var
func _token() -> (token_address : felt):
end

@storage_var
func _auctions_nonce() -> (_auctions_nonce : felt):
end

@storage_var
func _balances(account : felt) -> (balance : Uint256):
end

@storage_var
func _lockedBalancesOf(account : felt) -> (balances : Uint256):
end

@storage_var
func _auctionBalances(auction_id : felt, account : felt) -> (balance : Uint256):
end

@storage_var
func _current_winner(auction_id : felt) -> (current_winner : felt):
end

@storage_var
func _winning_bid(auction_id : felt) -> (winning_bid: Uint256):
end

@storage_var
func _end_time(auction_id : felt) -> (end_time : felt):
end

@constructor
func constructor{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(token_address : felt, owner : felt):

    _owner.write(value=owner)
    _token.write(value=token_address)

    return()
end

@view
func balanceOf{
    syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(account : felt) -> (balance: Uint256):
    let (balance) = _balances.read(account)
    return (balance)
end

@view
func auctionBalanceOf{
    syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(auction_id : felt, account : felt) -> (balance: Uint256):
    let (balance) = _auctionBalances.read(auction_id, account)
    return (balance)
end

@view
func token{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }() -> (token_address : felt):
    let (token_address) = _token.read()
    return (token_address)
end

@view
func current_winner{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(auction_id : felt) -> (current_winner: felt):
    let (winner) = _current_winner.read(auction_id)
    return (winner)
end

@view
func end_time{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(auction_id : felt) -> (end_time: felt):
    let (end_time_) = _end_time.read(auction_id)
    return (end_time_)
end

@external
func start_auction{
    syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }():
    only_owner()
    
    let (current_nonce) = _auctions_nonce.read()

    let new_auction_id = current_nonce + 1

    let (current_time) = get_block_timestamp()
    let end_time = current_time + DELAY

    _end_time.write(new_auction_id, end_time)
    _auctions_nonce.write(new_auction_id)

    return()
end

@external
func increase_credit{
    syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(amount : Uint256):

    let (caller) = get_caller_address()
    let (this) = get_contract_address()

    let (token_address : felt) = _token.read()

    IERC20.transferFrom(contract_address=token_address, sender=caller, recipient=this, amount=amount)

    let (current_balance) = _balances.read(account=caller)

    # This won't overflow because the transfer already validate the total amount of tokens owned by this contract
    let (new_balance, _) = uint256_add(current_balance, amount)

    _balances.write(account=caller, value=new_balance)
    
    return()
end

@external
func withdraw_credit{
    syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(amount : Uint256):
    alloc_locals

    let (caller : felt) = get_caller_address() 

    # Check if the caller has enough balance
    let (caller_balance : Uint256) = _balances.read(account=caller)
    let (caller_locked_balance : Uint256) = _lockedBalancesOf.read(account=caller)

    let (caller_unlocked_balance) = uint256_sub(caller_balance, caller_locked_balance)
    
    let (enough_amount : felt) = uint256_le(amount, caller_unlocked_balance)  
    with_attr error_message("NOT_ENOUGH_BALANCE"):
        assert enough_amount = TRUE
    end

    # Update user's balance
    let (new_balance : Uint256) = uint256_sub(caller_balance, amount)
    _balances.write(account=caller, value=new_balance)

    # Send tokens to user
    let (token_address : felt) = _token.read()
    IERC20.transfer(contract_address=token_address, recipient=caller, amount=amount)

    return()
end

@external
func raise_bid{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(auction_id : felt, amount : Uint256):
    alloc_locals

    only_open_auction(auction_id)

    let (caller) = get_caller_address()


    # Check if user has enough credit
    let (current_balance) = _balances.read(account=caller)
    let (locked_balance) = _lockedBalancesOf.read(account=caller)
    let (unlocked_balance) = uint256_sub(current_balance, locked_balance)
    let (enough_balance) = uint256_le(amount, unlocked_balance)

    assert enough_balance = 1

    # Update user's locked balanced
    let (new_balance, overflow) = uint256_add(locked_balance, amount)
    _lockedBalancesOf.write(account=caller, value=new_balance)
    assert overflow = 0

    # Update auction account balance
    let (current_balance) = _auctionBalances.read(auction_id=auction_id, account=caller)
    let (new_balance, overflow) = uint256_add(current_balance, amount)
    assert overflow = 0
    _auctionBalances.write(auction_id=auction_id, account=caller, value=new_balance)


    let (winning_bid) = _winning_bid.read(auction_id)
    let (is_new_winning_big) = uint256_lt(winning_bid, new_balance)


    if is_new_winning_big == 1:
        _winning_bid.write(auction_id=auction_id, value=new_balance)
        _current_winner.write(auction_id=auction_id, value=caller)
        tempvar syscall_ptr = syscall_ptr
        tempvar pedersen_ptr = pedersen_ptr
        tempvar range_check_ptr = range_check_ptr
    else :
        tempvar syscall_ptr = syscall_ptr
        tempvar pedersen_ptr = pedersen_ptr
        tempvar range_check_ptr = range_check_ptr
    end

    return()
end

@external 
func unlock_funds{
    syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(auction_id : felt, amount : Uint256):
    alloc_locals

    only_open_auction(auction_id)
    not_winning_bidder(auction_id) 

    let (caller : felt) = get_caller_address() 

    # Check if the caller has enough balance to avoid overflow
    let (caller_balance : Uint256) = _auctionBalances.read(auction_id=auction_id, account=caller)
    let (enough_amount : felt) = uint256_le(amount, caller_balance)  
    with_attr error_message("NOT_ENOUGH_BALANCE"):
        assert enough_amount = TRUE
    end

    # Update auction account balance
    let (new_balance : Uint256) = uint256_sub(caller_balance, amount)
    _auctionBalances.write(auction_id=auction_id, account=caller, value=new_balance)

    # Update user's locked balance
    let (locked_balance) = _lockedBalancesOf.read(account=caller)
    let (new_balance) = uint256_sub(locked_balance, amount)
    _lockedBalancesOf.write(account=caller, value=new_balance)

    return()
end

func only_open_auction{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(auction_id : felt):
   
    let (current_time) = get_block_timestamp()
    let (end_time) = _end_time.read(auction_id)

    with_attr error_message("AUCTION_DOES_NOT_EXIST"):
        assert_not_zero(end_time)
    end
    with_attr error_message("AUCTION_ENDED"):
        assert_lt(current_time, end_time)
    end

    return()
end

func not_winning_bidder{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }(auction_id : felt):
    let (caller) = get_caller_address()  
    let (current_winner_) = _current_winner.read(auction_id)

    let no_equals = caller - current_winner_
    assert_not_zero(no_equals)

    return()
end

func only_owner{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr
    }():
    let (owner) = _owner.read()
    let(caller) = get_caller_address()

    assert caller = owner

    return()
end



