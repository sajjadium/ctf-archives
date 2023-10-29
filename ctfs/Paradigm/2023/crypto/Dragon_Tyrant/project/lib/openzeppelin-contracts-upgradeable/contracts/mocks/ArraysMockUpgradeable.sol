// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ArraysUpgradeable } from "../utils/ArraysUpgradeable.sol";
import "../proxy/utils/Initializable.sol";

contract Uint256ArraysMockUpgradeable is Initializable {
    using ArraysUpgradeable for uint256[];

    uint256[] private _array;

    function __Uint256ArraysMock_init(uint256[] memory array) internal onlyInitializing {
        __Uint256ArraysMock_init_unchained(array);
    }

    function __Uint256ArraysMock_init_unchained(uint256[] memory array) internal onlyInitializing {
        _array = array;
    }

    function findUpperBound(uint256 element) external view returns (uint256) {
        return _array.findUpperBound(element);
    }

    function unsafeAccess(uint256 pos) external view returns (uint256) {
        return _array.unsafeAccess(pos).value;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}

contract AddressArraysMockUpgradeable is Initializable {
    using ArraysUpgradeable for address[];

    address[] private _array;

    function __AddressArraysMock_init(address[] memory array) internal onlyInitializing {
        __AddressArraysMock_init_unchained(array);
    }

    function __AddressArraysMock_init_unchained(address[] memory array) internal onlyInitializing {
        _array = array;
    }

    function unsafeAccess(uint256 pos) external view returns (address) {
        return _array.unsafeAccess(pos).value;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}

contract Bytes32ArraysMockUpgradeable is Initializable {
    using ArraysUpgradeable for bytes32[];

    bytes32[] private _array;

    function __Bytes32ArraysMock_init(bytes32[] memory array) internal onlyInitializing {
        __Bytes32ArraysMock_init_unchained(array);
    }

    function __Bytes32ArraysMock_init_unchained(bytes32[] memory array) internal onlyInitializing {
        _array = array;
    }

    function unsafeAccess(uint256 pos) external view returns (bytes32) {
        return _array.unsafeAccess(pos).value;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}
