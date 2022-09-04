# Declare this file as a StarkNet contract.
%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

@view
func get_flag{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
}(t:felt) -> (res : felt):
    if t == /* CENSORED */:
        return (res=0x42414c534e7b6f032fa620b5c520ff47733c3723ebc79890c26af4 + t*t)
    else:
        return(res=0)
    end
end
