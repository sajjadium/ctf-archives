%lang starknet

from starkware.cairo.common.math import assert_not_zero
from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.starknet.common.syscalls import library_call_l1_handler, library_call
from utils import auth_read_storage

@storage_var
func owner() -> (owner : felt):
end

@storage_var
func implementation() -> (class_hash: felt):
end

@constructor
func constructor{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(class_hash: felt):

    # Ensure that a contract is not deployed with ZERO implementation 
    assert_not_zero(class_hash)
    implementation.write(class_hash)

    return()
end

# Allow owner to read all the contract's state
@view
func read_state{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }(address : felt) -> (value : felt):
    let (owner_account) = owner.read()
    let (value) = auth_read_storage(owner_account, address)
    return (value)
end


# Fallback functions

@external
@raw_input
@raw_output
func __default__{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(
        selector: felt,
        calldata_size: felt,
        calldata: felt*
    ) -> (
        retdata_size: felt,
        retdata: felt*
    ):
    let (class_hash) = implementation.read()
    let (retdata_size: felt, retdata: felt*) = library_call(
        class_hash=class_hash,
        function_selector=selector,
        calldata_size=calldata_size,
        calldata=calldata
    )

    return (retdata_size=retdata_size, retdata=retdata)
end

@l1_handler
@raw_input
func __l1_default__{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(
        selector: felt,
        calldata_size: felt,
        calldata: felt*
    ):

    let (class_hash) = implementation.read()
    library_call_l1_handler(
        class_hash=class_hash,
        function_selector=selector,
        calldata_size=calldata_size,
        calldata=calldata
    )

    return ()
end

