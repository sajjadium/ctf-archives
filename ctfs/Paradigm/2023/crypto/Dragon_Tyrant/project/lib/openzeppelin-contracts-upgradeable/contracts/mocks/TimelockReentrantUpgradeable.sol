// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import { AddressUpgradeable } from "../utils/AddressUpgradeable.sol";
import "../proxy/utils/Initializable.sol";

contract TimelockReentrantUpgradeable is Initializable {
    function __TimelockReentrant_init() internal onlyInitializing {
    }

    function __TimelockReentrant_init_unchained() internal onlyInitializing {
    }
    address private _reenterTarget;
    bytes private _reenterData;
    bool _reentered;

    function disableReentrancy() external {
        _reentered = true;
    }

    function enableRentrancy(address target, bytes calldata data) external {
        _reenterTarget = target;
        _reenterData = data;
    }

    function reenter() external {
        if (!_reentered) {
            _reentered = true;
            AddressUpgradeable.functionCall(_reenterTarget, _reenterData);
        }
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[47] private __gap;
}
