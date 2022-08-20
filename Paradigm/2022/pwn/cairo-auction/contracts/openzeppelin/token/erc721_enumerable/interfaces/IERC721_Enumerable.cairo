# SPDX-License-Identifier: MIT
# OpenZeppelin Cairo Contracts v0.1.0 (token/erc721_enumerable/interfaces/IERC721_Enumerable.cairo)

%lang starknet

from starkware.cairo.common.uint256 import Uint256

from openzeppelin.token.erc721.interfaces.IERC721 import IERC721

@contract_interface
namespace IERC721_Enumerable:
    func totalSupply() -> (totalSupply: Uint256):
    end

    func tokenByIndex(index: Uint256) -> (tokenId: Uint256):
    end

    func tokenOfOwnerByIndex(owner: felt, index: Uint256) -> (tokenId: Uint256):
    end
end
