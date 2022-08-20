# SPDX-License-Identifier: MIT
# OpenZeppelin Cairo Contracts v0.1.0 (token/erc721/interfaces/IERC721_Receiver.cairo)

%lang starknet

from starkware.cairo.common.uint256 import Uint256

@contract_interface
namespace IERC721_Receiver:
    func onERC721Received(
        operator: felt,
        from_: felt,
        tokenId: Uint256,
        data_len: felt,
        data: felt*
    ) -> (selector: felt): 
    end
end
