// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import { IBeaconUpgradeable } from "../proxy/beacon/IBeaconUpgradeable.sol";
import "../proxy/utils/Initializable.sol";

contract UpgradeableBeaconMockUpgradeable is Initializable, IBeaconUpgradeable {
    address public implementation;

    function __UpgradeableBeaconMock_init(address impl) internal onlyInitializing {
        __UpgradeableBeaconMock_init_unchained(impl);
    }

    function __UpgradeableBeaconMock_init_unchained(address impl) internal onlyInitializing {
        implementation = impl;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}
