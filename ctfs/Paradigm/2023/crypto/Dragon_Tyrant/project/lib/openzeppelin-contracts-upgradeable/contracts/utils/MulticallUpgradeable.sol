// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.9.0) (utils/Multicall.sol)

pragma solidity ^0.8.19;

import { AddressUpgradeable } from "./AddressUpgradeable.sol";
import "../proxy/utils/Initializable.sol";

/**
 * @dev Provides a function to batch together multiple calls in a single external call.
 */
abstract contract MulticallUpgradeable is Initializable {
    function __Multicall_init() internal onlyInitializing {
    }

    function __Multicall_init_unchained() internal onlyInitializing {
    }
    /**
     * @dev Receives and executes a batch of function calls on this contract.
     * @custom:oz-upgrades-unsafe-allow-reachable delegatecall
     */
    function multicall(bytes[] calldata data) external virtual returns (bytes[] memory results) {
        results = new bytes[](data.length);
        for (uint256 i = 0; i < data.length; i++) {
            results[i] = AddressUpgradeable.functionDelegateCall(address(this), data[i]);
        }
        return results;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
