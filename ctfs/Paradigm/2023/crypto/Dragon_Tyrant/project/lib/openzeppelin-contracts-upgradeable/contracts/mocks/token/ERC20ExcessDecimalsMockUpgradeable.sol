// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;
import "../../proxy/utils/Initializable.sol";

contract ERC20ExcessDecimalsMockUpgradeable is Initializable {
    function __ERC20ExcessDecimalsMock_init() internal onlyInitializing {
    }

    function __ERC20ExcessDecimalsMock_init_unchained() internal onlyInitializing {
    }
    function decimals() public pure returns (uint256) {
        return type(uint256).max;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
