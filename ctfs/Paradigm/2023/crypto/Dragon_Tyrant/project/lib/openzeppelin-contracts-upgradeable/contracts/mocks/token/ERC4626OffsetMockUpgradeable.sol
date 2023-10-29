// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC4626Upgradeable } from "../../token/ERC20/extensions/ERC4626Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC4626OffsetMockUpgradeable is Initializable, ERC4626Upgradeable {
    uint8 private _offset;

    function __ERC4626OffsetMock_init(uint8 offset_) internal onlyInitializing {
        __ERC4626OffsetMock_init_unchained(offset_);
    }

    function __ERC4626OffsetMock_init_unchained(uint8 offset_) internal onlyInitializing {
        _offset = offset_;
    }

    function _decimalsOffset() internal view virtual override returns (uint8) {
        return _offset;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}
