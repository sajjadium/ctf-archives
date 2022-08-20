%lang starknet

from starkware.starknet.common.syscalls import storage_read, storage_write, get_caller_address

# Helpers for auth users to interact with contract's storage 
@view
func auth_read_storage{
        syscall_ptr : felt*,
    }(auth_account : felt, address : felt) -> (value : felt):
    let (caller) = get_caller_address()

    assert caller = auth_account

    let (value) = storage_read(address=address)

    return (value=value)
end

@external
func auth_write_storage{
        syscall_ptr : felt*,
    }(auth_account : felt, address : felt, value : felt):
    let (caller) = get_caller_address()

    assert caller = auth_account

    storage_write(address=address, value=value)
    return()
end
