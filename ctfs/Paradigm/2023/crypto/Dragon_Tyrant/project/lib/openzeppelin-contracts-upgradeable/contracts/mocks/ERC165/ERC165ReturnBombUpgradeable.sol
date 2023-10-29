// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { IERC165Upgradeable } from "../../utils/introspection/IERC165Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

contract ERC165ReturnBombMockUpgradeable is Initializable, IERC165Upgradeable {
    function __ERC165ReturnBombMock_init() internal onlyInitializing {
    }

    function __ERC165ReturnBombMock_init_unchained() internal onlyInitializing {
    }
    function supportsInterface(bytes4 interfaceId) public pure override returns (bool) {
        if (interfaceId == type(IERC165Upgradeable).interfaceId) {
            assembly {
                mstore(0, 1)
            }
        }
        assembly {
            return(0, 101500)
        }
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
