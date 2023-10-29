// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import { ERC20Upgradeable } from "../../token/ERC20/ERC20Upgradeable.sol";
import { AddressUpgradeable } from "../../utils/AddressUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

contract ERC20ReentrantUpgradeable is Initializable, ERC20Upgradeable {
    function __ERC20Reentrant_init() internal onlyInitializing {
        __ERC20_init_unchained("TEST", "TST");
    }

    function __ERC20Reentrant_init_unchained() internal onlyInitializing {
    }
    enum Type {
        No,
        Before,
        After
    }

    Type private _reenterType;
    address private _reenterTarget;
    bytes private _reenterData;

    function scheduleReenter(Type when, address target, bytes calldata data) external {
        _reenterType = when;
        _reenterTarget = target;
        _reenterData = data;
    }

    function functionCall(address target, bytes memory data) public returns (bytes memory) {
        return AddressUpgradeable.functionCall(target, data);
    }

    function _update(address from, address to, uint256 amount) internal override {
        if (_reenterType == Type.Before) {
            _reenterType = Type.No;
            functionCall(_reenterTarget, _reenterData);
        }
        super._update(from, to, amount);
        if (_reenterType == Type.After) {
            _reenterType = Type.No;
            functionCall(_reenterTarget, _reenterData);
        }
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[48] private __gap;
}
