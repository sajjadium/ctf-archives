// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import { AddressUpgradeable } from "../utils/AddressUpgradeable.sol";
import "../proxy/utils/Initializable.sol";

/**
 * @dev A mock to expose `Address`'s functions with function pointers.
 */
contract AddressFnPointerMockUpgradeable is Initializable {
    function __AddressFnPointerMock_init() internal onlyInitializing {
    }

    function __AddressFnPointerMock_init_unchained() internal onlyInitializing {
    }
    error CustomRevert();

    function functionCall(address target, bytes memory data) external returns (bytes memory) {
        return AddressUpgradeable.functionCall(target, data, _customRevert);
    }

    function functionCallWithValue(address target, bytes memory data, uint256 value) external returns (bytes memory) {
        return AddressUpgradeable.functionCallWithValue(target, data, value, _customRevert);
    }

    function functionStaticCall(address target, bytes memory data) external view returns (bytes memory) {
        return AddressUpgradeable.functionStaticCall(target, data, _customRevert);
    }

    function functionDelegateCall(address target, bytes memory data) external returns (bytes memory) {
        return AddressUpgradeable.functionDelegateCall(target, data, _customRevert);
    }

    function verifyCallResultFromTarget(
        address target,
        bool success,
        bytes memory returndata
    ) external view returns (bytes memory) {
        return AddressUpgradeable.verifyCallResultFromTarget(target, success, returndata, _customRevert);
    }

    function verifyCallResult(bool success, bytes memory returndata) external view returns (bytes memory) {
        return AddressUpgradeable.verifyCallResult(success, returndata, _customRevert);
    }

    function verifyCallResultVoid(bool success, bytes memory returndata) external view returns (bytes memory) {
        return AddressUpgradeable.verifyCallResult(success, returndata, _customRevertVoid);
    }

    function _customRevert() internal pure {
        revert CustomRevert();
    }

    function _customRevertVoid() internal pure {}

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
