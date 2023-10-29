// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC20Upgradeable } from "../../token/ERC20/ERC20Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC20DecimalsMockUpgradeable is Initializable, ERC20Upgradeable {
    uint8 private _decimals;

    function __ERC20DecimalsMock_init(uint8 decimals_) internal onlyInitializing {
        __ERC20DecimalsMock_init_unchained(decimals_);
    }

    function __ERC20DecimalsMock_init_unchained(uint8 decimals_) internal onlyInitializing {
        _decimals = decimals_;
    }

    function decimals() public view override returns (uint8) {
        return _decimals;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}
