# SPDX-License-Identifier: MIT
# OpenZeppelin Cairo Contracts v0.1.0 (introspection/ERC165.cairo)

%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin, SignatureBuiltin
from starkware.cairo.common.math import assert_not_equal

from openzeppelin.utils.constants import TRUE

@storage_var
func ERC165_supported_interfaces(interface_id: felt) -> (is_supported: felt):
end 

func ERC165_supports_interface{
        syscall_ptr: felt*, 
        pedersen_ptr: HashBuiltin*, 
        range_check_ptr
    } (interface_id: felt) -> (success: felt):
    # 165
    if interface_id == 0x01ffc9a7:
        return (TRUE)
    end

    # Checks interface registry
    let (is_supported) = ERC165_supported_interfaces.read(interface_id)
    return (is_supported)
end

func ERC165_register_interface{
        syscall_ptr: felt*, 
        pedersen_ptr: HashBuiltin*, 
        range_check_ptr
    } (interface_id: felt):
    with_attr error_message("ERC165: invalid interface id"):
        assert_not_equal(interface_id, 0xffffffff)
    end
    ERC165_supported_interfaces.write(interface_id, TRUE)
    return ()
end
