// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC4626Upgradeable } from "../../token/ERC20/extensions/ERC4626Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC4626LimitsMockUpgradeable is Initializable, ERC4626Upgradeable {
    uint256 _maxDeposit;
    uint256 _maxMint;

    function __ERC4626LimitsMock_init() internal onlyInitializing {
        __ERC4626LimitsMock_init_unchained();
    }

    function __ERC4626LimitsMock_init_unchained() internal onlyInitializing {
        _maxDeposit = 100 ether;
        _maxMint = 100 ether;
    }

    function maxDeposit(address) public view override returns (uint256) {
        return _maxDeposit;
    }

    function maxMint(address) public view override returns (uint256) {
        return _maxMint;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[48] private __gap;
}
