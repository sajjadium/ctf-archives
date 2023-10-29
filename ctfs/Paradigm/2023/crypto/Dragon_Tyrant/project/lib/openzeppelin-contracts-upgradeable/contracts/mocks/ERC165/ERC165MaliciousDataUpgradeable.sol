// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;
import "../../proxy/utils/Initializable.sol";

contract ERC165MaliciousDataUpgradeable is Initializable {
    function __ERC165MaliciousData_init() internal onlyInitializing {
    }

    function __ERC165MaliciousData_init_unchained() internal onlyInitializing {
    }
    function supportsInterface(bytes4) public pure returns (bool) {
        assembly {
            mstore(0, 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
            return(0, 32)
        }
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
