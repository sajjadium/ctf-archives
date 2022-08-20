# SPDX-License-Identifier: MIT
# OpenZeppelin Cairo Contracts v0.1.0 (security/pausable.cairo)

%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.starknet.common.syscalls import get_caller_address

from openzeppelin.utils.constants import TRUE, FALSE

@storage_var
func Pausable_paused() -> (paused: felt):
end

func Pausable_when_not_paused{
        syscall_ptr : felt*, 
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }():
    let (is_paused) = Pausable_paused.read()
    with_attr error_message("Pausable: contract is paused"):
        assert is_paused = FALSE
    end
    return ()
end

func Pausable_when_paused{
        syscall_ptr : felt*, 
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }():
    let (is_paused) = Pausable_paused.read()
    with_attr error_message("Pausable: contract is not paused"):
        assert is_paused = TRUE
    end
    return ()
end

func Pausable_pause{
        syscall_ptr : felt*, 
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }():
    Pausable_when_not_paused()
    Pausable_paused.write(TRUE)
    return ()
end

func Pausable_unpause{
        syscall_ptr : felt*, 
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }():
    Pausable_when_paused()
    Pausable_paused.write(FALSE)
    return ()
end
