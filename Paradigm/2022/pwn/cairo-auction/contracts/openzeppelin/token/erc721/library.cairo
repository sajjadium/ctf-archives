# SPDX-License-Identifier: MIT
# OpenZeppelin Cairo Contracts v0.1.0 (token/erc721/library.cairo)

%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin, SignatureBuiltin
from starkware.cairo.common.math import assert_not_zero, assert_not_equal
from starkware.cairo.common.alloc import alloc
from starkware.starknet.common.syscalls import get_caller_address
from starkware.cairo.common.uint256 import Uint256, uint256_check

from openzeppelin.security.safemath import (
    uint256_checked_add,
    uint256_checked_sub_le
)

from openzeppelin.introspection.ERC165 import ERC165_register_interface

from openzeppelin.token.erc721.interfaces.IERC721_Receiver import IERC721_Receiver

from openzeppelin.introspection.IERC165 import IERC165

from openzeppelin.utils.constants import TRUE, FALSE

#
# Events
#

@event
func Transfer(from_: felt, to: felt, tokenId: Uint256):
end

@event
func Approval(owner: felt, approved: felt, tokenId: Uint256):
end

@event
func ApprovalForAll(owner: felt, operator: felt, approved: felt):
end

#
# Storage
#

@storage_var
func ERC721_name_() -> (name: felt):
end

@storage_var
func ERC721_symbol_() -> (symbol: felt):
end

@storage_var
func ERC721_owners(token_id: Uint256) -> (owner: felt):
end

@storage_var
func ERC721_balances(account: felt) -> (balance: Uint256):
end

@storage_var
func ERC721_token_approvals(token_id: Uint256) -> (res: felt):
end

@storage_var
func ERC721_operator_approvals(owner: felt, operator: felt) -> (res: felt):
end

@storage_var
func ERC721_token_uri(token_id: Uint256) -> (token_uri: felt):
end

#
# Constructor
#

func ERC721_initializer{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }(
        name: felt,
        symbol: felt,
    ):
    ERC721_name_.write(name)
    ERC721_symbol_.write(symbol)
    # register IERC721
    ERC165_register_interface(0x80ac58cd)
    # register IERC721_Metadata
    ERC165_register_interface(0x5b5e139f)
    return ()
end

#
# Getters
#

func ERC721_name{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }() -> (name: felt):
    let (name) = ERC721_name_.read()
    return (name)
end

func ERC721_symbol{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }() -> (symbol: felt):
    let (symbol) = ERC721_symbol_.read()
    return (symbol)
end

func ERC721_balanceOf{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }(owner: felt) -> (balance: Uint256):
    with_attr error_message("ERC721: balance query for the zero address"):
        assert_not_zero(owner)
    end
    let (balance: Uint256) = ERC721_balances.read(owner)
    return (balance)
end

func ERC721_ownerOf{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(token_id: Uint256) -> (owner: felt):
    with_attr error_message("ERC721: token_id is not a valid Uint256"):
        uint256_check(token_id)
    end
    let (owner) = ERC721_owners.read(token_id)
    with_attr error_message("ERC721: owner query for nonexistent token"):
        assert_not_zero(owner)
    end
    return (owner)
end

func ERC721_getApproved{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(token_id: Uint256) -> (approved: felt):
    with_attr error_message("ERC721: token_id is not a valid Uint256"):
        uint256_check(token_id)
    end
    let (exists) = _exists(token_id)
    with_attr error_message("ERC721: approved query for nonexistent token"):
        assert exists = TRUE
    end

    let (approved) = ERC721_token_approvals.read(token_id)
    return (approved)
end

func ERC721_isApprovedForAll{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(owner: felt, operator: felt) -> (is_approved: felt):
    let (is_approved) = ERC721_operator_approvals.read(owner=owner, operator=operator)
    return (is_approved)
end

func ERC721_tokenURI{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(token_id: Uint256) -> (token_uri: felt):
    let (exists) = _exists(token_id)
    with_attr error_message("ERC721_Metadata: URI query for nonexistent token"):
        assert exists = TRUE
    end

    # if tokenURI is not set, it will return 0
    let (token_uri) = ERC721_token_uri.read(token_id)
    return (token_uri)
end

#
# Externals
#

func ERC721_approve{
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    }(to: felt, token_id: Uint256):
    with_attr error_mesage("ERC721: token_id is not a valid Uint256"):
        uint256_check(token_id)
    end

    # Checks caller is not zero address
    let (caller) = get_caller_address()
    with_attr error_message("ERC721: cannot approve from the zero address"):
        assert_not_zero(caller)
    end

    # Ensures 'owner' does not equal 'to'
    let (owner) = ERC721_owners.read(token_id)
    with_attr error_message("ERC721: approval to current owner"):
        assert_not_equal(owner, to)
    end

    # Checks that either caller equals owner or
    # caller isApprovedForAll on behalf of owner
    if caller == owner:
        _approve(to, token_id)
        return ()
    else:
        let (is_approved) = ERC721_operator_approvals.read(owner, caller)
        with_attr error_message("ERC721: approve caller is not owner nor approved for all"):
            assert_not_zero(is_approved)
        end
        _approve(to, token_id)
        return ()
    end
end

func ERC721_setApprovalForAll{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(operator: felt, approved: felt):
    # Ensures caller is neither zero address nor operator
    let (caller) = get_caller_address()
    with_attr error_message("ERC721: either the caller or operator is the zero address"):
        assert_not_zero(caller * operator)
    end
    # note this pattern as we'll frequently use it:
    #   instead of making an `assert_not_zero` call for each address
    #   we can always briefly write `assert_not_zero(a0 * a1 * ... * aN)`.
    #   This is because these addresses are field elements,
    #   meaning that a*0==0 for all a in the field,
    #   and a*b==0 implies that at least one of a,b are zero in the field
    with_attr error_message("ERC721: approve to caller"):
        assert_not_equal(caller, operator)
    end

    # Make sure `approved` is a boolean (0 or 1)
    with_attr error_message("ERC721: approved is not a Cairo boolean"):
        assert approved * (1 - approved) = 0
    end

    ERC721_operator_approvals.write(owner=caller, operator=operator, value=approved)
    ApprovalForAll.emit(caller, operator, approved)
    return ()
end

func ERC721_transferFrom{
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    }(from_: felt, to: felt, token_id: Uint256):
    alloc_locals
    with_attr error_message("ERC721: token_id is not a valid Uint256"):
        uint256_check(token_id)
    end
    let (caller) = get_caller_address()
    let (is_approved) = _is_approved_or_owner(caller, token_id)
    with_attr error_message("ERC721: either is not approved or the caller is the zero address"):
        assert_not_zero(caller * is_approved)
    end
    # Note that if either `is_approved` or `caller` equals `0`,
    # then this method should fail.
    # The `caller` address and `is_approved` boolean are both field elements
    # meaning that a*0==0 for all a in the field,
    # therefore a*b==0 implies that at least one of a,b is zero in the field

    _transfer(from_, to, token_id)
    return ()
end

func ERC721_safeTransferFrom{
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    }(
        from_: felt,
        to: felt,
        token_id: Uint256,
        data_len: felt,
        data: felt*
    ):
    alloc_locals
    with_attr error_message("ERC721: token_id is not a valid Uint256"):
        uint256_check(token_id)
    end
    let (caller) = get_caller_address()
    let (is_approved) = _is_approved_or_owner(caller, token_id)
    with_attr error_message("ERC721: either is not approved or the caller is the zero address"):
        assert_not_zero(caller * is_approved)
    end
    # Note that if either `is_approved` or `caller` equals `0`,
    # then this method should fail.
    # The `caller` address and `is_approved` boolean are both field elements
    # meaning that a*0==0 for all a in the field,
    # therefore a*b==0 implies that at least one of a,b is zero in the field

    _safe_transfer(from_, to, token_id, data_len, data)
    return ()
end

func ERC721_mint{
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    }(to: felt, token_id: Uint256):
    with_attr error_message("ERC721: token_id is not a valid Uint256"):
        uint256_check(token_id)
    end
    with_attr error_message("ERC721: cannot mint to the zero address"):
        assert_not_zero(to)
    end

    # Ensures token_id is unique
    let (exists) = _exists(token_id)
    with_attr error_message("ERC721: token already minted"):
        assert exists = FALSE
    end

    let (balance: Uint256) = ERC721_balances.read(to)
    let (new_balance: Uint256) = uint256_checked_add(balance, Uint256(1, 0))
    ERC721_balances.write(to, new_balance)
    ERC721_owners.write(token_id, to)
    Transfer.emit(0, to, token_id)
    return ()
end

func ERC721_burn{
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    }(token_id: Uint256):
    alloc_locals
    with_attr error_message("ERC721: token_id is not a valid Uint256"):
        uint256_check(token_id)
    end
    let (owner) = ERC721_ownerOf(token_id)

    # Clear approvals
    _approve(0, token_id)

    # Decrease owner balance
    let (balance: Uint256) = ERC721_balances.read(owner)
    let (new_balance: Uint256) = uint256_checked_sub_le(balance, Uint256(1, 0))
    ERC721_balances.write(owner, new_balance)

    # Delete owner
    ERC721_owners.write(token_id, 0)
    Transfer.emit(owner, 0, token_id)
    return ()
end

func ERC721_safeMint{
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    }(
        to: felt,
        token_id: Uint256,
        data_len: felt,
        data: felt*
    ):
    with_attr error_message("ERC721: token_id is not a valid Uint256"):
        uint256_check(token_id)
    end
    ERC721_mint(to, token_id)

    let (success) = _check_onERC721Received(
        0,
        to,
        token_id,
        data_len,
        data
    )
    with_attr error_message("ERC721: transfer to non ERC721Receiver implementer"):
        assert_not_zero(success)
    end
    return ()
end

func ERC721_only_token_owner{
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    }(token_id: Uint256):
    uint256_check(token_id)
    let (caller) = get_caller_address()
    let (owner) = ERC721_ownerOf(token_id)
    # Note `ERC721_ownerOf` checks that the owner is not the zero address
    with_attr error_message("ERC721: caller is not the token owner"):
        assert caller = owner
    end
    return ()
end

func ERC721_setTokenURI{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(token_id: Uint256, token_uri: felt):
    uint256_check(token_id)
    let (exists) = _exists(token_id)
    with_attr error_message("ERC721_Metadata: set token URI for nonexistent token"):
        assert exists = TRUE
    end

    ERC721_token_uri.write(token_id, token_uri)
    return ()
end

#
# Internals
#

func _approve{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(to: felt, token_id: Uint256):
    ERC721_token_approvals.write(token_id, to)
    let (owner) = ERC721_ownerOf(token_id)
    Approval.emit(owner, to, token_id)
    return ()
end

func _is_approved_or_owner{
        pedersen_ptr: HashBuiltin*,
        syscall_ptr: felt*,
        range_check_ptr
    }(spender: felt, token_id: Uint256) -> (res: felt):
    alloc_locals

    let (exists) = _exists(token_id)
    with_attr error_message("ERC721: token id does not exist"):
        assert exists = TRUE
    end

    let (owner) = ERC721_ownerOf(token_id)
    if owner == spender:
        return (TRUE)
    end

    let (approved_addr) = ERC721_getApproved(token_id)
    if approved_addr == spender:
        return (TRUE)
    end

    let (is_operator) = ERC721_isApprovedForAll(owner, spender)
    if is_operator == TRUE:
        return (TRUE)
    end

    return (FALSE)
end

func _exists{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(token_id: Uint256) -> (res: felt):
    let (res) = ERC721_owners.read(token_id)

    if res == 0:
        return (FALSE)
    else:
        return (TRUE)
    end
end

func _transfer{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(from_: felt, to: felt, token_id: Uint256):
    # ownerOf ensures 'from_' is not the zero address
    let (_ownerOf) = ERC721_ownerOf(token_id)
    with_attr error_message("ERC721: transfer from incorrect owner"):
        assert _ownerOf = from_
    end

    with_attr error_message("ERC721: cannot transfer to the zero address"):
        assert_not_zero(to)
    end

    # Clear approvals
    _approve(0, token_id)

    # Decrease owner balance
    let (owner_bal) = ERC721_balances.read(from_)
    let (new_balance: Uint256) = uint256_checked_sub_le(owner_bal, Uint256(1, 0))
    ERC721_balances.write(from_, new_balance)

    # Increase receiver balance
    let (receiver_bal) = ERC721_balances.read(to)
    let (new_balance: Uint256) = uint256_checked_add(receiver_bal, Uint256(1, 0))
    ERC721_balances.write(to, new_balance)

    # Update token_id owner
    ERC721_owners.write(token_id, to)
    Transfer.emit(from_, to, token_id)
    return ()
end

func _safe_transfer{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(
        from_: felt,
        to: felt,
        token_id: Uint256,
        data_len: felt,
        data: felt*
    ):
    _transfer(from_, to, token_id)

    let (success) = _check_onERC721Received(from_, to, token_id, data_len, data)
    with_attr error_message("ERC721: transfer to non ERC721Receiver implementer"):
        assert_not_zero(success)
    end
    return ()
end

func _check_onERC721Received{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(
        from_: felt,
        to: felt,
        token_id: Uint256,
        data_len: felt,
        data: felt*
    ) -> (success: felt):
    let (caller) = get_caller_address()
    # ERC721_RECEIVER_ID = 0x150b7a02
    let (is_supported) = IERC165.supportsInterface(to, 0x150b7a02)
    if is_supported == TRUE:
        let (selector) = IERC721_Receiver.onERC721Received(
            to,
            caller,
            from_,
            token_id,
            data_len,
            data
        )

        # ERC721_RECEIVER_ID
        with_attr error_message("ERC721: transfer to non ERC721Receiver implementer"):
            assert selector = 0x150b7a02
        end
        return (TRUE)
    end

    # IAccount_ID = 0xf10dbd44
    let (is_account) = IERC165.supportsInterface(to, 0xf10dbd44)
    return (is_account)
end
