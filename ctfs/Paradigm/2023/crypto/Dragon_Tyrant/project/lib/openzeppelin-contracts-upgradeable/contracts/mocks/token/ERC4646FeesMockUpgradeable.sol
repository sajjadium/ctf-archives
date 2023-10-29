// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC4626FeesUpgradeable } from "../docs/ERC4626FeesUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC4626FeesMockUpgradeable is Initializable, ERC4626FeesUpgradeable {
    uint256 private _entryFeeBasePointValue;
    address private _entryFeeRecipientValue;
    uint256 private _exitFeeBasePointValue;
    address private _exitFeeRecipientValue;

    function __ERC4626FeesMock_init(
        uint256 entryFeeBasePoint,
        address entryFeeRecipient,
        uint256 exitFeeBasePoint,
        address exitFeeRecipient
    ) internal onlyInitializing {
        __ERC4626FeesMock_init_unchained(entryFeeBasePoint, entryFeeRecipient, exitFeeBasePoint, exitFeeRecipient);
    }

    function __ERC4626FeesMock_init_unchained(
        uint256 entryFeeBasePoint,
        address entryFeeRecipient,
        uint256 exitFeeBasePoint,
        address exitFeeRecipient
    ) internal onlyInitializing {
        _entryFeeBasePointValue = entryFeeBasePoint;
        _entryFeeRecipientValue = entryFeeRecipient;
        _exitFeeBasePointValue = exitFeeBasePoint;
        _exitFeeRecipientValue = exitFeeRecipient;
    }

    function _entryFeeBasePoint() internal view virtual override returns (uint256) {
        return _entryFeeBasePointValue;
    }

    function _entryFeeRecipient() internal view virtual override returns (address) {
        return _entryFeeRecipientValue;
    }

    function _exitFeeBasePoint() internal view virtual override returns (uint256) {
        return _exitFeeBasePointValue;
    }

    function _exitFeeRecipient() internal view virtual override returns (address) {
        return _exitFeeRecipientValue;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[46] private __gap;
}
