# SPDX-License-Identifier: MIT
# OpenZeppelin Cairo Contracts v0.1.0 (security/initializable.cairo)

%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

from openzeppelin.utils.constants import TRUE, FALSE

@storage_var
func _initialized() -> (res: felt):
end

@external
func initialized{ 
        syscall_ptr : felt*, 
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }() -> (res: felt):
    let (res) = _initialized.read()
    return (res=res)
end

@external
func initialize{
        syscall_ptr : felt*, 
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }():
    let (initialized) = _initialized.read()
    with_attr error_message("Initializable: contract already initialized"):
        assert initialized = FALSE
    end
    _initialized.write(TRUE)
    return ()
end
