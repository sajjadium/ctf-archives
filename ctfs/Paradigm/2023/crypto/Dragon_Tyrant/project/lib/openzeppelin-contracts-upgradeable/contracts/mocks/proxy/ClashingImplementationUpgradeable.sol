// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;
import "../../proxy/utils/Initializable.sol";

/**
 * @dev Implementation contract with a payable changeAdmin(address) function made to clash with
 * TransparentUpgradeableProxy's to test correct functioning of the Transparent Proxy feature.
 */
contract ClashingImplementationUpgradeable is Initializable {
    function __ClashingImplementation_init() internal onlyInitializing {
    }

    function __ClashingImplementation_init_unchained() internal onlyInitializing {
    }
    event ClashingImplementationCall();

    function upgradeToAndCall(address, bytes calldata) external payable {
        emit ClashingImplementationCall();
    }

    function delegatedFunction() external pure returns (bool) {
        return true;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
