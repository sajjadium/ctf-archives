// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { UUPSUpgradeable } from "../../proxy/utils/UUPSUpgradeable.sol";
import { ERC1967UtilsUpgradeable } from "../../proxy/ERC1967/ERC1967UtilsUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

contract NonUpgradeableMockUpgradeable is Initializable {
    function __NonUpgradeableMock_init() internal onlyInitializing {
    }

    function __NonUpgradeableMock_init_unchained() internal onlyInitializing {
    }
    uint256 internal _counter;

    function current() external view returns (uint256) {
        return _counter;
    }

    function increment() external {
        ++_counter;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}

contract UUPSUpgradeableMockUpgradeable is Initializable, NonUpgradeableMockUpgradeable, UUPSUpgradeable {
    function __UUPSUpgradeableMock_init() internal onlyInitializing {
    }

    function __UUPSUpgradeableMock_init_unchained() internal onlyInitializing {
    }
    // Not having any checks in this function is dangerous! Do not do this outside tests!
    function _authorizeUpgrade(address) internal override {}

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}

contract UUPSUpgradeableUnsafeMockUpgradeable is Initializable, UUPSUpgradeableMockUpgradeable {
    function __UUPSUpgradeableUnsafeMock_init() internal onlyInitializing {
    }

    function __UUPSUpgradeableUnsafeMock_init_unchained() internal onlyInitializing {
    }
    function upgradeToAndCall(address newImplementation, bytes memory data) public payable override {
        ERC1967UtilsUpgradeable.upgradeToAndCall(newImplementation, data);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}

contract UUPSUnsupportedProxiableUUIDUpgradeable is Initializable, UUPSUpgradeableMockUpgradeable {
    function __UUPSUnsupportedProxiableUUID_init() internal onlyInitializing {
    }

    function __UUPSUnsupportedProxiableUUID_init_unchained() internal onlyInitializing {
    }
    function proxiableUUID() external pure override returns (bytes32) {
        return keccak256("invalid UUID");
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
